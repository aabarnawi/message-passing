from kafka import KafkaConsumer
import grpc
from concurrent import futures
import location_pb2 , location_pb2_grpc

import time
import os
TOPIC_NAME = 'locations'

from kafka import KafkaProducer

persons_ids = [1,5,6,8,9]
TOPIC_NAME = 'locations'
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        request_value = {
            "person_id": request.person_id,
            "creation_time": request.creation_time,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }
        producer.send(TOPIC_NAME, bytes(str(request_value),"utf-8"))
        producer.flush()
        print("Sent {}".format(request_value))
        return location_pb2.LocationMessage(**request_value)
    

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)