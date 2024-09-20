from kafka import KafkaProducer, KafkaConsumer
from config import KAFKA_SERVER,KAFKA_TOPIC
import json
import time

def get_kafka_producer():
    for _ in range(5):  # Try 5 times
        try:
            return KafkaProducer(
                bootstrap_servers=[KAFKA_SERVER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print(f"Failed to connect to Kafka, retrying... Error: {e}")
            time.sleep(5)
    raise Exception("Failed to connect to Kafka after several attempts")

def get_kafka_consumer():
    for _ in range(5):  # Try 5 times
        try:
            return KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=[KAFKA_SERVER],
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
        except Exception as e:
            print(f"Failed to connect to Kafka, retrying... Error: {e}")
            time.sleep(5)
    raise Exception("Failed to connect to Kafka after several attempts")

producer = None
consumer = None

def send_event(event_type, data):
    global producer
    if producer is None:
        producer = get_kafka_producer()
    producer.send(KAFKA_TOPIC, {'type': event_type, 'data': data})
    producer.flush()

def get_consumer():
    global consumer
    if consumer is None:
        consumer = get_kafka_consumer()
    return consumer

# producer = KafkaProducer(
#     bootstrap_servers=[KAFKA_SERVER],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# consumer = KafkaConsumer(
#     KAFKA_TOPIC,
#     bootstrap_servers=[KAFKA_SERVER],
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# # this I will use in routes when any request is received
# def send_event(event_type, data):
#     producer.send(KAFKA_TOPIC, {'type': event_type, 'data': data})
#     producer.flush()

# def get_consumer():
#     return consumer