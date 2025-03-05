import sys
import os 

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
transaction_verification_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, transaction_verification_grpc_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionVerificationService(transaction_verification_grpc.VerificationServiceServicer):
    def VerifyTransaction (self, request, context):
        logging.info("starting transaction verification")
        response = transaction_verification.VerificationResponse()

        order = request.order_data
        cardnumber = order.carddata.card_number
        cvv = order.carddata.cvv
        exp_date = order.carddata.expiration

        reg_card = re.match(r"^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$", cardnumber)
        logging.info("card number valid")
        reg_cvv = re.match(r"^[0-9]{3,4}$", cvv)
        logging.info("cvv valid")
        reg_exp = re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", exp_date) 
        logging.info("expiration date valid")
        if reg_card is not None and reg_cvv is not None and reg_exp is not None:
            response.response = "OK"
            logging.info("verification successful")
        else:
            response.response = "ERROR"
            loggin.error("verification unsuccessful")
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
