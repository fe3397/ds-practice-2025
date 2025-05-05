import sys
import os
from concurrent import futures

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

fraud_detection_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/fraud_detection'))
sys.path.insert(3, fraud_detection_grpc_path)

transaction_verification_grpc_path = os.path.abspath(
    os.path.join(os.path.dirname(FILE), '../../utils/pb/transaction_verification'))
sys.path.insert(4, transaction_verification_grpc_path)

import common_pb2 as common
import common_pb2_grpc as common_grpc

import order_pb2
import order_pb2_grpc as order_grpc

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import suggestion_service_pb2 as suggestion_service
import suggestion_service_pb2_grpc as suggestion_service_grpc

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_verification(order_data):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        response = stub.InitOrder(transaction_verification.InitOrderRequest(order_data=order_data))
    return response


def init_fraud_detection(order_data):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_grpc.FraudDetectionStub(channel)
        response = stub.InitOrder(fraud_detection.InitFraudRequest(order_data=order_data))
    return response


def init_suggestion(order_data):
    with grpc.insecure_channel('suggestion_service:50053') as channel:
        stub = suggestion_service_grpc.SuggestionStub(channel)
        response = stub.InitOrder(suggestion_service.InitSuggestionRequest(order_data=order_data))
    return response


def suggest(order_id, vector_clock):
    req = suggestion_service.SuggestionRequest()
    req.order_id = order_id
    req.vector_clock.clock.extend(vector_clock)
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('suggestion_service:50053') as channel:
        # Create a stub object.
        stub = suggestion_service_grpc.SuggestionStub(channel)
        # Call the service through the stub object.
        response = stub.MakeSuggestion(req)
        # Return the response.
        return response


def checkFraud(order_id, vector_clock):
    req = fraud_detection.FraudRequest()
    req.order_id = order_id
    req.vector_clock.clock.extend(vector_clock)
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_grpc.FraudDetectionStub(channel)
        # Call the service through the stub object.
        response = stub.LookforFraud(req)
    return response.fraud, response.vector_clock


def verify(order_id, vector_clock):
    req = transaction_verification.VerificationRequest()
    req.order_id = order_id
    req.vector_clock.clock.extend(vector_clock)

    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        response = stub.VerifyTransaction(req)
    return response.response, response.vector_clock


def order(request):
    order = order_pb2.OrderData(
        id=str(uuid.uuid4().int % (10 ** 3)),
        userdata=order_pb2.UserData(
            name=request['user']['name'],
            contact=request['user']['contact']
        ),
        carddata=order_pb2.CardData(
            card_number=request['creditCard']['number'],
            expiration=request['creditCard']['expirationDate'],
            cvv=request['creditCard']['cvv']
        ),
        useradress=order_pb2.UserAdress(
            street=request['billingAddress']['street'],
            city=request['billingAddress']['city'],
            state=request['billingAddress']['state'],
            zip=request['billingAddress']['zip'],
            country=request['billingAddress']['country']
        ),
        books=[
            order_pb2.Book(name=item['name'], amount=int(item['quantity']))
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
    response = "greet(name='orchestrator')"
    # request_data = json.loads(request.data)
    # response = checkFraud(fraud_detection.FraudRequest(user=request_data.user, cc=request_data.creditCard))
    # Return the response.
    return response


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Get request object data to json
    request_data = json.loads(request.data)
    order_data = order(request_data)
    init_verif = init_verification(order_data)
    logging.info(f"Order verification init {init_verif}")
    init_fraud = init_fraud_detection(order_data)
    logging.info(f"Order fraud detection init {init_verif}")
    init_sug = init_suggestion(order_data)
    logging.info(f"Order suggestion init {init_verif}")

    response_verify = verify(order_data.id, [0, 0, 0])
    logging.info(f"Verification vector clock: {response_verify[1].clock}")

    response_fraud = checkFraud(order_data.id, list(response_verify[1].clock))
    logging.info(f"Fraud detection vector clock: {response_fraud[1].clock}")

    response_sugg = suggest(order_data.id, list(response_fraud[1].clock))
    logging.info(f"Suggestion vector clock")

    # Check for fraud
    #
    # if is_fraud:
    #     order_status_response = {
    #         'orderId': '12345',
    #         'status': 'Your transaction was flagged as potentially fraudulent. Please contact support.',
    #         'suggestedBooks': [
    #             {'bookId': '123', 'title': 'The Best Book', 'author': 'Author 1'},
    #             {'bookId': '456', 'title': 'The Second Best Book', 'author': 'Author 2'}
    #         ]
    #     }
    # else:
    #     # Dummy response following the provided YAML specification for the bookstore
    #     order_status_response = {
    #         'orderId': '12345',
    #         'status': 'Order Approved',
    #         'suggestedBooks': [
    #             {'bookId': '123', 'title': "suggestions.sug_book_1", 'author': 'Author 1'},
    #             {'bookId': '456', 'title': "suggestions.sug_book_2", 'author': 'Author 2'}
    #         ]
    #     }
    # verification_response = verify(request_data)
    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
