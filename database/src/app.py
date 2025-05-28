import sys
import os
import socket

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
database_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/database'))
sys.path.insert(0, database_grpc_path)

import database_pb2 as database
import database_pb2_grpc as database_grpc

import grpc
from concurrent import futures

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

resource = Resource.create(attributes={
    SERVICE_NAME: "database_service",
})

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4317", insecure=True)
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)


meter = metrics.get_meter(__name__)
decrement_counter = meter.create_counter(
    "db_decrement_counter",
    description="Number of successful stock decrements"
)

increment_counter = meter.create_counter(
    "db_increment_counter",
    description="Number of successful stock increments"
)

class BooksDatabaseService(database_grpc.BooksDatabaseServicer):
    def __init__(self):
        self.store = {"Book A": 1, "Book B": 2}
        self.recover()
        self.instance_id = os.environ.get("INSTANCE_ID", socket.gethostname())  # Unique ID for this instance

    def log_state(self, state):
        self.state = state
        with open("/tmp/participant_state.log", "w") as f:
            f.write(state)

    def recover(self):
        try:
            with open("participant_state.log", "r") as f:
                self.state = f.read().strip()
        except FileNotFoundError:
            self.state = "INIT"

    def Prepare(self, request, context):
        print(f"Database prepared")
        self.log_state("PREPARED")
        return database.PrepareResponse(ready=True)
    
    def Commit(self, request, context):
        print(f"Database committed")
        self.log_state("COMMITTED")
        return database.CommitResponse(success=True)
    
    def Abort(self, request, context):
        print("Database aborted")
        self.log_state("ABORTED")
        return database.AbortResponse(aborted=True)
    
    def Read(self, request, context): #todo always read from tail
        stock = self.store.get(request.title, 0)
        return database.ReadResponse(stock=stock)
    
    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        print(f"Writing {request.title} with stock {request.new_stock}")
        return database.WriteResponse(success=True)
    
    def DecrementStock(self, request, context):
        if request.title in self.store and self.store[request.title] > 0:
            self.store[request.title] -= 1
            return database.DecrementStockResponse(success=True)
        else:
            return database.DecrementStockResponse(success=False)
    
    def IncrementStock(self, request, context):
        if request.title in self.store:
            self.store[request.title] += 1
        else:
            self.store[request.title] = 1
        return database.IncrementStockResponse(success=True)
    
    def get_own_ip(self):
        hostname = socket.gethostname()
        return hostname

class ChainReplica(BooksDatabaseService):
    def __init__(self):
        super().__init__()
        # Determine successor based on self.peers order
        self.peers = ["database_head", "database_mid", "database_tail"]
        self.own_name = os.environ.get("ROLE", "head")
        idx = self.peers.index(self.own_name)
        self.successor_addr = self.peers[idx + 1] if idx < len(self.peers) - 1 else None
        self.successor_stub = None
        if self.successor_addr:
            self.successor_stub = database_grpc.BooksDatabaseStub(
                grpc.insecure_channel(f"{self.successor_addr}:50057")
            )

    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        if self.successor_stub:
            try:
                response = self.successor_stub.Write(request)
                if not response.success:
                    print(f"Failed to write to successor: {self.successor_addr}")
                    return database.WriteResponse(success=False)
            except Exception as e:
                print(f"Failed to write to successor: {e}")
                return database.WriteResponse(success=False)
        return database.WriteResponse(success=True)
    
    def DecrementStock(self, request, context):
        if request.title in self.store and self.store[request.title] > 0:
            self.store[request.title] -= 1
            decrement_counter.add(1, {"book": request.title})
            
            # Propagate to successor
            if self.successor_stub:
                response = self.successor_stub.DecrementStock(request)
                if not response.success:
                    print(f"Failed to decrement stock at successor: {self.successor_addr}")
                    return database.DecrementStockResponse(success=False)
            return database.DecrementStockResponse(success=True)
        else:
            return database.DecrementStockResponse(success=False)

    def IncrementStock(self, request, context):
        if request.title in self.store:
            self.store[request.title] += 1
            increment_counter.add(1, {"book": request.title})
        else:
            self.store[request.title] = 1
        # Propagate to successor
        if self.successor_stub:
            response = self.successor_stub.IncrementStock(request)
            if not response.success:
                print(f"Failed to increment stock at successor: {self.successor_addr}")
                return database.IncrementStockResponse(success=False)
        return database.IncrementStockResponse(success=True)

    def IsHead(self, request, context):
        is_head = self.get_own_ip() == self.peers[0]
        return database.IsHeadResponse(is_head=is_head, ip =self.get_own_ip())
    
    def IsTail(self, request, context):
        is_tail = self.get_own_ip() == self.peers[-1]
        return database.IsTailResponse(is_tail=is_tail, ip =self.get_own_ip())
        
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add Suggestions
    database_grpc.add_BooksDatabaseServicer_to_server(ChainReplica(), server)
    # Listen on port 50057
    port = "50057"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
