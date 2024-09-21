from flask import Flask
from api.routes import api
from sync.outsync import start_outsync
from database.db import initialise_db
from utils.kafka_client import get_kafka_producer, get_kafka_consumer
import threading
import logging  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(api)

def kafka_health_check():
    logger.info("Checking Kafka connection...")
    try:
        producer = get_kafka_producer()
        consumer = get_kafka_consumer()
        logger.info("Successfully connected to Kafka")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        return False

def db_health_check():
    logger.info("Checking database connection...")
    try:
        initialise_db()
        logger.info("Successfully connected to the database")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        return False

if __name__ == '__main__':
    try:
        db_status = db_health_check()
        kafka_status = kafka_health_check()

        if db_status and kafka_status:
            logger.info("All connections established successfully:")
            logger.info("Starting Kafka consumer thread...")
            threading.Thread(target=start_outsync, daemon=True).start()
            logger.info("Starting Flask app...")
            app.run(host='0.0.0.0', port=5000)

        else:
            logger.error("Failed to establish all necessary connections. Aborting startup.")
            
    except Exception as e:
        logger.error(f"An error occurred during startup: {e}")
        raise