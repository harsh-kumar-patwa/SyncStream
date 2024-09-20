from flask import Flask
from api.routes import api
from sync.outsync import start_outsync
from database.db import initialise_db
from utils.kafka_client import get_kafka_producer, get_kafka_consumer
import threading
import logging  
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(api)

def kafka_health_check():
    logger.info("Checking Kafka connection...")
    try:
        producer = get_kafka_producer()
        consumer = get_kafka_consumer()
        logger.info("Successfully connected to Kafka")
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        raise

if __name__ == '__main__':
    try:
        logger.info("Setting up database...")
        initialise_db()
        
        logger.info("Performing Kafka health check...")
        kafka_health_check()
        
        logger.info("Starting Kafka consumer thread...")
        threading.Thread(target=start_outsync, daemon=True).start()
        
        logger.info("Starting Flask app...")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"An error occurred during startup: {e}")
        raise