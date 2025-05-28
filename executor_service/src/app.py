import logging
import sys
import os
import socket
import time
# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

common_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/common'))
sys.path.insert(0, common_grpc_path)

order_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/order_data'))
sys.path.insert(1, order_grpc_path)

executor_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/executor'))
sys.path.insert(2, executor_grpc_path)

database_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(3, database_grpc_path)

payment_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(4, payment_grpc_path)

import common_pb2 as common
import common_pb2_grpc as common_grpc

import executor_pb2 as executor
import executor_pb2_grpc as executor_grpc

import grpc
from concurrent import futures
import threading
import uuid

import order_pb2 as order_queue
import order_pb2_grpc as order_queue_grpc

import database_pb2 as database
import database_pb2_grpc as database_grpc

import payment_pb2 as payment
import payment_pb2_grpc as payment_grpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Service name is required for most backends
resource = Resource.create(attributes={
    SERVICE_NAME: "executor_service",
})

tracerProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="observability:3000"))
tracerProvider.add_span_processor(processor)
trace.set_tracer_provider(tracerProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:3000", insecure=True)
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

tracer = trace.get_tracer(__name__)


class OrderExecutorService(executor_grpc.OrderExecutorServicer):
    def __init__(self):
        self._lock = threading.Lock()
        self.leader_id = None
        self.instance_id = os.environ.get("INSTANCE_ID", socket.gethostname())  # Unique ID for this instance
        self.peers = self.discover_peers()
        self.election_in_progress = False

        threading.Thread(target=self.run_leader_election, daemon=True).start()
        threading.Thread(target=self.process_order, daemon=True).start()

    def get_own_ip(self):
        hostname = socket.gethostname()
        return hostname

    def discover_peers(self):
        try:
            addr_info = socket.getaddrinfo("order_executor",50055, proto= socket.IPPROTO_TCP)
            peers = set()
            for info in addr_info:
                ip = info[4][0]
                if ip != self.get_own_ip():
                    peers.add(ip)
            return list(peers)
        except Exception as e:
            print(f"[{self.instance_id[:8]}] Peer discovery failed: {e}")
            return []

    def ElectLeader(self, request, context):
        # Leader election by Bully Algorithm
        with self._lock:
            if self.leader_id is None or request.instance_id > self.leader_id:
                self.leader_id = request.instance_id
                is_leader = (self.instance_id == self.leader_id)
            else:
                is_leader = (self.instance_id == self.leader_id)
            print(f"[{self.instance_id[:8]}] Received election request from {request.instance_id[:8]} - My leader: {self.leader_id[:8]}, Am I leader? {is_leader}")
            return executor.LeaderElectionResponse(leader_id=self.leader_id, is_leader=is_leader)

    def run_leader_election(self):
        while True:
            try:
                highest_id = self.instance_id
                for peer in self.peers:
                    with grpc.insecure_channel(f"{peer}:50055") as channel:
                        stub = executor_grpc.OrderExecutorStub(channel)
                        response = stub.ElectLeader(executor.LeaderElectionRequest(instance_id=self.instance_id))
                        print(response)
                        if response.leader_id > highest_id:
                            highest_id = response.leader_id
                with self._lock:
                    self.leader_id = highest_id
                    if self.leader_id == self.instance_id:
                        logging.warning(f"[{self.instance_id[:8]}] I am the LEADER.")
                    # else:
                    #     logging.warning(f"[{self.instance_id[:8]}] Current leader is {self.leader_id[:8]}")

            except Exception as e:
                logging.critical(f"[{self.instance_id[:8]}] Leader election error: {e}")
            time.sleep(100)


    def process_order(self):
        while True:
            with tracer.start_as_current_span("process_order") as span:
                time.sleep(10)
                # Ensure only the leader can dequeue
                if self.instance_id != self.leader_id:
                    continue
                else: # Return an empty order
                    with grpc.insecure_channel('queue_service:50054') as channel:
                        stub = order_queue_grpc.OrderQueueStub(channel)
                        response = stub.Dequeue(order_queue.DequeueRequest())
                        span.set_attribute("order.id", getattr(response.order_data, "id", "none"))
                        time.sleep(2)
                        if response.order_data.id:
                            with self._lock:
                                # 1. Prepare participants for 2PC
                                participants = []
                                db_channel = grpc.insecure_channel('database_head:50057')
                                db_stub = database_grpc.BooksDatabaseStub(db_channel)
                                participants.append(db_stub)
                                payment_channel = grpc.insecure_channel('payment:50056')
                                payment_stub = payment_grpc.PaymentServiceStub(payment_channel)
                                participants.append(payment_stub)
                                # 2. Run 2PC
                                if self.two_phase_commit(participants): #response.order_data.id, 
                                    # 3. Only do the actual decrement if 2PC succeeded
                                    for book in response.order_data.books:
                                        print(f"Processing book: {book.name}, Amount: {book.amount}")
                                        # Read current stock from the tail
                                        with grpc.insecure_channel('database_tail:50057') as db_channel:
                                            db_stub = database_grpc.BooksDatabaseStub(db_channel)
                                            read_resp = db_stub.Read(database.ReadRequest(title=book.name))
                                            old_stock = read_resp.stock
                                        # Write (decrement) to the head
                                        with grpc.insecure_channel('database_head:50057') as db_channel:
                                            db_stub = database_grpc.BooksDatabaseStub(db_channel)
                                            for _ in range(book.amount):
                                                dec_resp = db_stub.DecrementStock(database.DecrementStockRequest(title=book.name))
                                                if dec_resp.success:
                                                    logging.info(f"Decremented stock for {book.name}: {old_stock} -> {old_stock - book.amount}")
                                                else:
                                                    logging.error(f"Failed to decrement stock for {book.name} (possibly out of stock)")
                                else:
                                    logging.error("2PC failed, not processing order.")

    def two_phase_commit(self, participants): # order_id,
        ready_votes = []
        for service in participants:
            try:
                response = service.Prepare(common.PrepareRequest())
                ready_votes.append(response.ready)
            except Exception as e:
                logging.error(f"Failed to prepare order with {service}: {e}")
                ready_votes.append(False)
        if all(ready_votes):
            for service in participants:
                try:
                    service.Commit(common.CommitRequest())
                except Exception as e:
                    logging.error(f"Failed to commit order to {service}: {e}")
                    return
            print("All services committed")
            return True
        else:
            for service in participants:
                try:
                    service.Abort(common.AbortRequest())
                except Exception as e:
                    logging.error(f"Failed to abort order with {service}: {e}")
                    return
            print("Transaction aborted")



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = OrderExecutorService()
    executor_grpc.add_OrderExecutorServicer_to_server(service, server)
    port = "50055"
    server.add_insecure_port("[::]:"+port)
    server.start()
    print(f"[{service.instance_id[:8]}] Order Executor Service started. Listening on port 50055")
    server.wait_for_termination()
if __name__ == '__main__':
    serve()