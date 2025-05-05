import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

common_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/common'))
sys.path.insert(0, common_grpc_path)

order_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/order_data'))
sys.path.insert(1, order_grpc_path)

suggestion_service_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/suggestion_service'))
sys.path.insert(2, suggestion_service_grpc_path)

import common_pb2 as common
import common_pb2_grpc as common_grpc

import order_pb2 as order
import order_pb2_grpc as order_grpc

import suggestion_service_pb2 as suggestion_service
import suggestion_service_pb2_grpc as suggestion_service_grpc

import grpc
from concurrent import futures
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class SuggestionService(suggestion_service_grpc.SuggestionServicer):
    def __init__(self, svc_idx=2, total_svcs=3):
        self.suggestions = {
            "1": ["The Great Gatsby", "To Kill a Mockingbird", "1984"],
            "2": ["The Catcher in the Rye", "The Grapes of Wrath"],
        }
        self.svc_idx = svc_idx
        self.total_svcs = total_svcs
        self.orders = {}
    
    def InitOrder(self, request: suggestion_service.InitSuggestionRequest, context):
        print("InitOrder received request:", request.order_data.id)
        order_data = request.order_data

        response = suggestion_service.InitSuggestionResponse()

        self.orders[order_data.id] = {"data": order_data, "vc": [0]*self.total_svcs}
        if self.orders[order_data.id]["data"]:
            response.status = "OK"
            return response
        else:
            response.status = "FAIL"
            return response

    def merge_and_increment(self, local_vc, incoming_vc):
            for i in range(self.total_svcs):
                local_vc[i] = max(local_vc[i], incoming_vc[i])
            local_vc[self.svc_idx] += 1

    def MakeSuggestion(self, request: suggestion_service.SuggestionRequest, context):
        logging.info("starting book suggestion")

        cache = self.orders.get(request.order_id)

        if not cache:
            context.abort(grpc.StatusCode.NOT_FOUND, "Order not found")

        incoming_vector = list(request.vector_clock.clock)
        if len(incoming_vector) > 0:
            logging.info(f"incoming: {incoming_vector}")
        else:
            incoming_vector = [0] * self.total_svcs

        order = cache["data"]
        vector = cache["vc"]

        book_1 = order.books[0]
        book_2 = order.books[1]

        self.merge_and_increment(vector, incoming_vector)
        logging.info(f"[a] Vector clock after MakeSuggestion: {vector}")

        logging.info(f"Making suggestions for books {book_1} and {book_2}")
        # Create a SuggestionResponse object
        response = suggestion_service.SuggestionResponse()
        # Get suggestions
        if book_1 == 'Book A':
            response.sug_book_1 = 'The Great Gatsby'
        else:
            response.sug_book_1 = 'The Catcher in the Rye'
        if book_2 == 'Book B':
            response.sug_book_2 = 'To Kill a Mockingbird'
        else:
            response.sug_book_2 = 'The Grapes of Wrath'
        print("Suggested books:", response.sug_book_1, "and", response.sug_book_2)
        # Possible AI solution:
        #print("Using AI to suggest books.")
        #prompt = f"Given that I like {book_1} and {book_2}, suggest two more books. Titles only, separated by a comma."
        #response = openai.Completion.create(
        #    model="gpt-4",
        #    messages=[{"role": "user", "content": prompt}],
        #    temperature=0  # Ensures deterministic responses
        #)
        #answer = response.choices[0].message.content
        #suggestions = answer.split(", ")
        #response.sug_book_1 = suggestions[0]
        #response.sug_book_2 = suggestions[1]
        #print("Suggested books:", suggestions)
        response.vector_clock.clock[:] = vector
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add Suggestions
    suggestion_service_grpc.add_SuggestionServicer_to_server(SuggestionService(), server)
    # Listen on port 50053
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
