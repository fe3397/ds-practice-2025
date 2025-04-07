import sys
import os

#AI stuff sadly not working because problems with openai library
#import openai
#openai.api_key = os.getenv("OPENAI_API_KEY")

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
fraud_detection_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, fraud_detection_grpc_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudDetectionServiceServicer
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServicer):
    def __init__(self):
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
    # Create an RPC function to check fraud
    def LookforFraud(self, request, context):
        user_data = request.user
        cc_data = request.cc
        # Create a FraudResponse object
        response = fraud_detection.FraudResponse()

        # Check if the user is in the userDB
        if user_data.name in self.userDB:
            print(f"User {user_data.name} found in userDB, comparing credit card data...")
            # Check if the credit card is in the userDB
            if cc_data.number in self.userDB[user_data.name]['cc']['number'] and cc_data.expirationDate in self.userDB[user_data.name]['cc']['expirationDate'] and cc_data.cvv in self.userDB[user_data.name]['cc']['cvv']:
                # Return a fraud response
                response.fraud = False
                print("No fraud detected")
            else:
                # Return a fraud response
                response.fraud = True
                print("Possible fraud detected")
        else:
            # Ask Chatgpt if the user is a fraud
            print(f"User not found in userDB, screening with AI...")
            answer = "NO" # Default to NO for now
            
            #prompt = f"Does this transaction look like fraud? Respond with only 'YES' or 'NO'.\n\nTransaction Data:\n{user_data, cc_data}"
            #response = openai.ChatCompletion.create(
            #    model="gpt-4",
            #    messages=[{"role": "user", "content": prompt}],
            #    temperature=0  # Ensures deterministic responses
            #)
            #answer = response["choices"][0]["message"]["content"].strip().upper()
            if answer == "YES":
                # Return a fraud response
                response.fraud = True
                print("AI has detected possible fraud")
            else:
                # Return a fraud response
                response.fraud = False
                print("No fraud detected, adding user to userDB")
                # Add the user to the userDB
                self.userDB[user_data.name] = {
                    'contact': user_data.contact,
                    'cc': {
                        'number': cc_data.number,
                        'expirationDate': cc_data.expirationDate,
                        'cvv': cc_data.cvv
                    }
                }
        # Return the response object
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add FraudDetectionService
    fraud_detection_grpc.add_FraudDetectionServicer_to_server(FraudDetectionService(), server)
    # Add HelloService
    #fraud_detection_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
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