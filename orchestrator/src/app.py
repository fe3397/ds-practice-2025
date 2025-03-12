import sys
import os
from concurrent import futures

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
fraud_detection_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
transaction_verification_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, fraud_detection_grpc_path)
sys.path.insert(1, transaction_verification_grpc_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

from transaction_verification_pb2 import OrderData, UserData, CardData, UserAdress, Book

import grpc
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def checkFraud(user, cc):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
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
                {'bookId': '123', 'title': 'The Best Book', 'author': 'Author 1'},
                {'bookId': '456', 'title': 'The Second Best Book', 'author': 'Author 2'}
            ]
        }
    verification_response = verify(order(request_data))
    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
