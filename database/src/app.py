import sys
import os

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
database_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/database'))
sys.path.insert(0, database_grpc_path)
import database_pb2 as database
import database_pb2_grpc as database_grpc

import grpc
from concurrent import futures

class BooksDatabaseService(database_grpc.BooksDatabaseServicer):
    def __init__(self):
        self.store = {}
        self.recover()

    def log_state(self, state):
        self.state = state
        with open("participant_state.log", "w") as f:
            f.write(state)

    def recover(self):
        try:
            with open("participant_state.log", "r") as f:
                self.state = f.read().strip()
        except FileNotFoundError:
            self.state = "INIT"

    def Prepare(self, request, context):
        self.log_state("PREPARED")
        return database.PrepareResponse(ready=True)
    
    def Commit(self, request, context):
        self.log_state("COMMITTED")
        return database.CommitResponse(success=True)
    
    def Abort(self, request, context):
        self.log_state("ABORTED")
        return database.AbortResponse(aborted=True)
    
    def Read(self, request, context):
        stock = self.store.get(request.title, 0)
        return database.ReadResponse(stock=stock)
    
    def Write(self, request, context):
        self.store[request.title] = request.new_stock
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
    

class PrimaryReplica(BooksDatabaseService):
    def __init__(self, backup_stubs):
        super().__init__()
        self.backups = backup_stubs

    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        for backup in self.backups:
            try:
                backup.Write(request)
            except Exception as e:
                print(f"Failed to write to backup: {e}")
        return database.WriteResponse(success=True)
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add Suggestions
    database_grpc.add_BooksDatabaseServicer_to_server(BooksDatabaseService(), server)
    # Listen on port 50056
    port = "50057"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
