import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'customer.db')
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
KAFKA_TOPIC = 'customer_events'

INTEGRATIONS = {
    'stripe': {
        'api_key': os.getenv('STRIPE_API_KEY'),
        'webhook_secret': os.getenv('STRIPE_WEBHOOK_SECRET'),
    },
}
ENABLED_INTEGRATIONS=['stripe']