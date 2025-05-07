import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

common_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/common'))
sys.path.insert(0, common_grpc_path)

queue_service_grpc_path = os.path.abspath(os.path.join(os.path.dirname(FILE), '../../utils/pb/order_data'))
sys.path.insert(1, queue_service_grpc_path)

import order_pb2 as order_queue
import order_pb2_grpc as order_queue_grpc

import grpc
from concurrent import futures
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrderQueueService(order_queue_grpc.OrderQueueServicer):
    def __init__(self):
        self._lock = threading.Lock()
        self.order_queue = []

    def Enqueue(self, request: order_queue.EnqueueRequest, context):
        print("Received order data:")
        with self._lock:
            premium_user = True #request.userdata.premium_user
            if premium_user:
                logging.info("Premium user detected. Adding to the front of the queue.")
                self.order_queue.insert(0, request)
            else:
                logging.info("Regular user detected. Adding to the end of the queue.")
                self.order_queue.append(request)
            logging.info(f"Order {request.id} added to the queue.")
        return order_queue.EnqueueResponse(success=True)

    def Dequeue(self, request, context):
        if self.order_queue:
            order = self.order_queue.pop()
            logging.info(f"Order {order.id} dequeued from the queue.")
            return order
        else:
            logging.info("No orders in the queue.")
            return order_queue.OrderData()
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_grpc.add_OrderQueueServicer_to_server(OrderQueueService(), server)
    port = "50054"
    server.add_insecure_port("[::]:"+port)
    server.start()
    print("Server started. Listening on port 50054")
    server.wait_for_termination()
if __name__ == '__main__':
    serve()