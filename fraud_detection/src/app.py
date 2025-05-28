
import sys
import os

# AI stuff sadly not working because problems with openai library
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
common_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/common'))
sys.path.insert(0, common_grpc_path)

order_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/order_data'))
sys.path.insert(1, order_grpc_path)

fraud_detection_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/fraud_detection'))
sys.path.insert(2, fraud_detection_grpc_path)

import common_pb2 as common
import common_pb2_grpc as common_grpc

import order_pb2 as order
import order_pb2_grpc as order_grpc

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudDetectionServiceServicer
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServicer):
    def __init__(self, svc_idx=1, total_svcs=3):
        self.userDB = {
            'John Doe': {
                'contact': 'john.doe@example.com',
                'cc': {
                    'number': '4111111111111111',
                    'expirationDate': '12/25',
                    'cvv': '123'
                }
            }
        }
        self.svc_idx = svc_idx
        self.total_svcs = total_svcs
        self.orders = {}

    def InitOrder(self, request: order.OrderData, context):
        print("InitOrder received request:", request.order_data.id)
        order_data = request.order_data

        response = fraud_detection.InitFraudResponse()

        self.orders[order_data.id] = {"data": order_data, "vc": [0] * self.total_svcs}
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

    # Create an RPC function to check fraud
    def LookforFraud(self, request: fraud_detection.FraudRequest, context):
        logging.info("starting fraud detection")

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
        user_data = order.userdata
        cc_data = order.carddata
        # Create a FraudResponse object
        response = fraud_detection.FraudResponse()

        def check_card_fraud():
            self.merge_and_increment(vector, incoming_vector)
            logging.info(f"[a] Vector clock after check_user_data_fraud: {vector}")
            # if cc_data.number in self.userDB[user_data.name]['cc']['number'] and cc_data.expirationDate in \
            #         self.userDB[user_data.name]['cc']['expirationDate'] and cc_data.cvv in \
            #         self.userDB[user_data.name]['cc']['cvv']:
            #     # Return a fraud response
            #     response.fraud = False
            #     print("No fraud detected")
            # else:
            #     # Return a fraud response
            #     response.fraud = True
            #     print("Possible fraud detected")
            return False

        def check_user_data_fraud():
            self.merge_and_increment(vector, vector)
            logging.info(f"[a] Vector clock after check_user_data_fraud: {vector}")

            # Check if the user is in the userDB
            if user_data.name in self.userDB:
                # print(f"User {user_data.name} found in userDB, comparing credit card data...")
                response.fraud = "OK"
            # else:
                # Ask Chatgpt if the user is a fraud
                # print(f"User not found in userDB, screening with AI...")
            answer = "NO"  # Default to NO for now

            # prompt = f"Does this transaction look like fraud? Respond with only 'YES' or 'NO'.\n\nTransaction Data:\n{user_data, cc_data}"
            # response = openai.ChatCompletion.create(
            #    model="gpt-4",
            #    messages=[{"role": "user", "content": prompt}],
            #    temperature=0  # Ensures deterministic responses
            # )
            # answer = response["choices"][0]["message"]["content"].strip().upper()
            if answer == "YES":
                # Return a fraud response
                response.fraud = "FAIL"
                print("AI has detected possible fraud")
            else:
                # Return a fraud response
                response.fraud = "OK"
                print("No fraud detected, adding user to userDB")
                # Add the user to the userDB
            return False

        card_fraud = check_card_fraud()
        user_data_fraud = check_user_data_fraud()

        if card_fraud and user_data_fraud:
            response.fraud = "FAIL"
            response.vector_clock.clock[:] = vector
            return response
        else:
            response.fraud = "OK"
            response.vector_clock.clock[:] = vector
            return response
        # Return the response object


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add FraudDetectionService
    fraud_detection_grpc.add_FraudDetectionServicer_to_server(FraudDetectionService(), server)
    # Add HelloService
    # fraud_detection_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
