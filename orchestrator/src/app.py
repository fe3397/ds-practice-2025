import sys
import os
from concurrent import futures

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

fraud_detection_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/suggestion_service'))
sys.path.insert(0, fraud_detection_grpc_path)
import suggestion_service_pb2 as suggestion_service
import suggestion_service_pb2_grpc as suggestion_service_grpc

fraud_detection_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/fraud_detection'))
sys.path.insert(1, fraud_detection_grpc_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

transaction_verification_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/transaction_verification'))
sys.path.insert(2, transaction_verification_grpc_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

from transaction_verification_pb2 import OrderData, UserData, CardData, UserAdress, Book

import grpc
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_verification(order_data):
    with grpc.insecure_channel('transaction_verification:50052'):
        stub = transaction_verification_grpc.VerificationServiceStub(channel)



def init_fraud_detection(order_data):
    with grpc.insecure_channel('transaction_verification:50052'):
        stub = fraud_detection_grpc.FraudDetectionStub(channel)

def init_suggestion(order_data):
    with grpc.insecure_channel('suggestion_service:50053') as channel:
        stub = suggestion_service_grpc.SuggestionStub(channel)



def suggest(book1, book2):
  # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('suggestion_service:50053') as channel:
        # Create a stub object.
        stub = suggestion_service_grpc.SuggestionStub(channel)
        # Call the service through the stub object.
        response = stub.MakeSuggestion(suggestion_service.SuggestionRequest(book_1=book1, book_2=book2))
        # Return the response.
        return response

def checkFraud(user, cc):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_grpc.FraudDetectionStub(channel)
        # Call the service through the stub object.
        response = stub.LookforFraud(fraud_detection.FraudRequest(user=user, cc=cc))
    return response.fraud

def verify(order_data):

    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        response = stub.VerifyTransaction(transaction_verification.VerificationRequest(order_data = order_data))
    return response.response

def order(request):
    order = OrderData(
        id = str(uuid.uuid4().int % (10 ** 3)),
        userdata = UserData(
            name = request['user']['name'],
            contact = request['user']['contact']
        ),
        carddata = CardData(
            card_number = request['creditCard']['number'],
            expiration = request['creditCard']['expirationDate'],
            cvv = request['creditCard']['cvv']
        ),
        useradress = UserAdress(
            street = request['billingAddress']['street'],
            city = request['billingAddress']['city'],
            state = request['billingAddress']['state'],
            zip = request['billingAddress']['zip'],
            country = request['billingAddress']['country']
        ),
        books = [
            Book(name = item['name'], amount = int(item['quantity']))
            for item in request['items']
        ]
    )
    return order 

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app, resources={r'/*': {'origins': '*'}})
# Launch Threads
executor = futures.ThreadPoolExecutor(max_workers=10)

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = greet(name='orchestrator')
    #request_data = json.loads(request.data)
    #response = checkFraud(fraud_detection.FraudRequest(user=request_data.user, cc=request_data.creditCard))
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Get request object data to json
    request_data = json.loads(request.data)
    print("Request Data:", request_data.get('items'))
    suggestions = suggest(request_data.get('items')[0]['name'], request_data.get('items')[1]['name'])
    # Check for fraud
    is_fraud = checkFraud(request_data.get('user'), request_data.get('creditCard'))

    if is_fraud:
        order_status_response = {
            'orderId': '12345',
            'status': 'Your transaction was flagged as potentially fraudulent. Please contact support.',
            'suggestedBooks': [
                {'bookId': '123', 'title': 'The Best Book', 'author': 'Author 1'},
                {'bookId': '456', 'title': 'The Second Best Book', 'author': 'Author 2'}
            ]
        }
    else:
    # Dummy response following the provided YAML specification for the bookstore
        order_status_response = {
            'orderId': '12345',
            'status': 'Order Approved',
            'suggestedBooks': [
                {'bookId': '123', 'title': suggestions.sug_book_1, 'author': 'Author 1'},
                {'bookId': '456', 'title': suggestions.sug_book_2, 'author': 'Author 2'}
            ]
        }
    verification_response = verify(order(request_data))
    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
