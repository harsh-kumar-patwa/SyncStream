from kafka import KafkaProducer, KafkaConsumer
from config import KAFKA_SERVER,KAFKA_TOPIC
import json

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def send_event(event_type, data):
    producer.send(KAFKA_TOPIC, {'type': event_type, 'data': data})
    producer.flush()

def get_consumer():
    return consumer