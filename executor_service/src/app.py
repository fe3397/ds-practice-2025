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

import executor_pb2 as executor
import executor_pb2_grpc as executor_grpc

import grpc
from concurrent import futures
import threading
import uuid

import order_pb2 as order_queue
import order_pb2_grpc as order_queue_grpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            time.sleep(10)
            # Ensure only the leader can dequeue
            if self.instance_id != self.leader_id:
                continue
            else: # Return an empty order
                with grpc.insecure_channel('queue_service:50054') as channel:
                    stub = order_queue_grpc.OrderQueueStub(channel)
                    response = stub.Dequeue(order_queue.DequeueRequest())
                    time.sleep(2)
                    if response.id:
                        with self._lock:
                            logging.info(f"Order {response.id} is being executed...")
                    # else:
                    #     logging.info("No orders in the queue.")




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