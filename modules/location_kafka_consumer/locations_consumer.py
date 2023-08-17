from kafka import KafkaConsumer
import json
import os
from sqlalchemy import create_engine

TOPIC_NAME = 'locations'

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

print(f"Connnecting to DB at {DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}  ..")
conn = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True).connect()

print("Connected to DB.")

consumer = KafkaConsumer(TOPIC_NAME,bootstrap_servers =KAFKA_SERVER)
for message in consumer:
    
    location = json.loads(message.value.decode("utf-8").replace("'",'"'))

    print(location)

    table_insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(location["person_id"], location["latitude"], location["longitude"])
    print(table_insert)
    conn.execute(table_insert)

    print ("received locations:\n{}".format(location))
    