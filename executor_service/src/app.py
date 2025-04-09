import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
executor_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/executor'))
sys.path.insert(0, executor_grpc_path)
import executor_pb2 as executor
import executor_pb2_grpc as executor_grpc

import grpc
from concurrent import futures
import threading
import uuid
order_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_data'))
sys.path.insert(0, order_grpc_path)
import order_pb2 as order_queue
import order_pb2_grpc as order_queue_grpc

class OrderExecutorService(executor_grpc.OrderExecutorServicer):
    def __init__(self):
        self._lock = threading.Lock()
        self.leader_id = None
        self.instance_id = str(uuid.uuid4())  # Unique ID for this instance

    def DequeueOrder(self, request, context):
        # Ensure only the leader can dequeue
        if self.instance_id != self.leader_id:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Only the leader can dequeue orders.")
            return order_queue.OrderData()  # Return an empty order

        with grpc.insecure_channel('queue_service:50054') as channel:
            stub = order_queue_grpc.OrderQueueStub(channel)
            response = stub.Dequeue(order_queue.DequeueRequest())
            if response.id:
                print(f"Order {response.id} is being executed...")
            else:
                print("No orders in the queue.")
            return response

    def ElectLeader(self, request, context):
        # Leader election by Bully Algorithm
        with self._lock:
            if self.leader_id is None or request.instance_id > self.leader_id:
                self.leader_id = request.instance_id
                is_leader = (self.instance_id == self.leader_id)
            else:
                is_leader = False
            print(f"Leader Election: Instance {request.instance_id} is leader: {is_leader}")
            return executor.LeaderElectionResponse(leader_id=self.leader_id, is_leader=is_leader)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    executor_grpc.add_OrderExecutorServicer_to_server(OrderExecutorService(), server)
    port = "50055"
    server.add_insecure_port("[::]:"+port)
    server.start()
    print("Order Executor Service started. Listening on port 50055")
    server.wait_for_termination()
if __name__ == '__main__':
    serve()