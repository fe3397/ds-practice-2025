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

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


resource = Resource.create(attributes={
    SERVICE_NAME: "queue_service",
})

tracerProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4317", insecure=True))
tracerProvider.add_span_processor(processor)
trace.set_tracer_provider(tracerProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4317", insecure=True)
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

queue_updown_counter = meter.create_up_down_counter(
    "queue_updown_counter",
    description="Current number of orders in the queue"
)

class OrderQueueService(order_queue_grpc.OrderQueueServicer):
    def __init__(self):
        self._lock = threading.Lock()
        self.order_queue = []

    def Enqueue(self, request: order_queue.EnqueueRequest, context):
        queue_updown_counter.add(1, {"queue": "order_queue"})
        with tracer.start_as_current_span("EnqueueOrder") as span:
            print("Received order data:", request.order_data)
            span.set_attribute("order.id", request.order_data.id)
            with self._lock:
                premium_user = True #request.userdata.premium_user
                span.set_attribute("user.premium", premium_user)
                if premium_user:
                    logging.info("Premium user detected. Adding to the front of the queue.")
                    self.order_queue.insert(0, request)
                    span.set_attribute("queue.position", "front")
                else:
                    logging.info("Regular user detected. Adding to the end of the queue.")
                    self.order_queue.append(request)
                    span.set_attribute("queue.position", "end")
                logging.info(f"Order {request.order_data.id} added to the queue.")
            return order_queue.EnqueueResponse(success=True)

    def Dequeue(self, request: order_queue.DequeueRequest, context):
        queue_updown_counter.add(-1, {"queue": "order_queue"})
        if self.order_queue:
            order = self.order_queue.pop()
            #logging.info(f"Order {order.id} dequeued from the queue.")
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