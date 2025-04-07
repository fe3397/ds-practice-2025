import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
suggestion_service_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestion_service'))
sys.path.insert(0, suggestion_service_grpc_path)
import suggestion_service_pb2 as suggestion_service
import suggestion_service_pb2_grpc as suggestion_service_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class SuggestionService(suggestion_service_grpc.SuggestionServicer):
    def __init__(self):
        self.suggestions = {
            "1": ["The Great Gatsby", "To Kill a Mockingbird", "1984"],
            "2": ["The Catcher in the Rye", "The Grapes of Wrath"],
        }
    # Create an RPC function to say hello
    def MakeSuggestion(self, request, context):
        book_1 = request.book_1
        book_2 = request.book_2
        print("Received request for", book_1, "and", book_2, "making suggestions.")
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