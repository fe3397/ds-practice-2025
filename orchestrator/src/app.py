import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
fraud_detection_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestion_service'))
sys.path.insert(0, fraud_detection_grpc_path)
import suggestion_service_pb2 as suggestion_service
import suggestion_service_pb2_grpc as suggestion_service_grpc

import grpc

def suggest(book1, book2):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('suggestion_service:50053') as channel:
        # Create a stub object.
        stub = suggestion_service_grpc.SuggestionStub(channel)
        # Call the service through the stub object.
        response = stub.MakeSuggestion(suggestion_service.SuggestionRequest(book_1=book1, book_2=book2))
        # Return the response.
    return response

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS
import json

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app, resources={r'/*': {'origins': '*'}})

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = greet(name='orchestrator')
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Get request object data to json
    request_data = json.loads(request.data)
    # Print request object data
    print("Request Data:", request_data.get('items'))
    suggestions = suggest(request_data.get('items')[0]['name'], request_data.get('items')[1]['name'])

    # Dummy response following the provided YAML specification for the bookstore
    order_status_response = {
        'orderId': '12345',
        'status': 'Order Approved',
        'suggestedBooks': [
            {'bookId': '123', 'title': suggestions.sug_book_1, 'author': 'Author 1'},
            {'bookId': '456', 'title': suggestions.sug_book_2, 'author': 'Author 2'}
        ]
    }

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
