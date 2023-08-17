import grpc
import location_pb2
import location_pb2_grpc
import random
"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)
persons_ids = [1,5,6,8,9]

# Update this with desired payload
location = location_pb2.LocationMessage(
            person_id= str(random.choice(persons_ids)),
            creation_time= "2020-08-18T10:37:06",
            latitude= "-122.290524",
            longitude="37.553441",
)

response = stub.Create(location)
