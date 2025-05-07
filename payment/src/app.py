import sys
import os
import grpc
from concurrent import futures

# AI stuff sadly not working because problems with openai library
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
payment_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/payment'))
sys.path.insert(0, payment_grpc_path)

import payment_pb2 as payment
import payment_pb2_grpc as payment_grpc

class PaymentService(payment_grpc.PaymentServiceServicer):
    def __init__(self):
        self.prepared = False
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
    
    def prepare(self, request, context):
        self.prepared = True
        self.log_state("PREPARED")
        return payment.PrepareResponse(ready=True)
    
    def Commit(self, request, context):
        if self.prepared:
            print("Payment committed")
            self.prepared = False
            self.log_state("COMMITTED")
        return payment.CommitResponse(success=True)
    
    def Abort(self, request, context):
        self.prepared = False
        print("Payment aborted")
        self.log_state("ABORTED")
        return payment.AbortResponse(aborted=True)
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add Suggestions
    payment_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
    # Listen on port 50055
    port = "50056"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()