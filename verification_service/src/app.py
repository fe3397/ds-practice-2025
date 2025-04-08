import sys
import os 

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
transaction_verification_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))

common_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/common'))
order_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_data'))

sys.path.insert(0, transaction_verification_grpc_path)
sys.path.insert(1, common_grpc_path)
sys.path.insert(2, order_grpc_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import order_pb2 as order
import order_pb2_grpc as order_grpc

import common_pb2 as common
import common_pb2_grpc as common_grpc

import grpc
from concurrent import futures
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionVerificationService(transaction_verification_grpc.VerificationServiceServicer):

    def __init__(self, svc_idx=0, total_svcs=3):
        self.svc_idx = svc_idx
        self.total_svcs = total_svcs
        self.orders = {}


    def InitOrder(self, request: order.OrderData , context):
        self.orders[request.id] = {"data": data, "vc": [0]*self.total_svcs}

    def merge_and_increment(self, local_vc, incoming_vc):
        for i in range(self.total_svcs):
            local_vc[i] = max(local_vc[i], incoming_vc[i])
        local_vc[self.svc_idx] += 1

    def VerifyTransaction (order_id):
        logging.info("starting transaction verification")
        response = transaction_verification.VerificationResponse()

        cache = self.orders.get(order_id)

        if not cache:
            context.abort(grpc.StatusCode.NOT_FOUND, "Order not found")

        order = cache["data"]
        vector = cache["vc"]
        cardnumber = order.carddata.card_number
        cvv = order.carddata.cvv
        exp_date = order.carddata.expiration
        books = order.books
        def verify_items():
            self.merge_and_increment(vector, vector)
            logging.info(f"[a] Vector clock after VerifyItems: {vector}")
            return bool(books)

        def verify_user_data():
            self.merge_and_increment(vector, vector)
            logging.info(f"[a] Vector clock after VerifyUserData: {vector}")
            return all([
                cardnumber,
                cvv,
                exp_date
            ])
        def verify_card_format():
            self.merge_and_increment(vector, vector)
            logging.info(f"[a] Vector clock after VerifyCardFormat: {vector}")
            
            reg_card = re.match(r"^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$", cardnumber)
            logging.info("card number valid")
            reg_cvv = re.match(r"^[0-9]{3,4}$", cvv)
            logging.info("cvv valid")
            reg_exp = re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", exp_date) 
            logging.info("expiration date valid")
            if reg_card is not None and reg_cvv is not None and reg_exp is not None:
                response.response = "OK"
                response.vector_clock = common_pb2.VectorClock(vector_clock=vector)
                logging.info("verification successful")
            else:
                response.response = "ERROR"
                logging.error("verification unsuccessful")
            return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add VerificationService
    transaction_verification_grpc.add_VerificationServiceServicer_to_server(TransactionVerificationService(), server)
    # Listen on port 50052
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
