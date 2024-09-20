from utils.kafka_client import get_consumer
from integrations.stripe_integration import StripeIntegration
from database.operations import update_customer

stripe_integration = StripeIntegration()

def send_update_to_external_system(event):
    if event['type']=='create':
        stripe_id = stripe_integration.create_customer(event['data']['name'], event['data']['email'])
        print(stripe_id+"\n")
        update_customer(event['data']['id'],stripe_id=stripe_id)
    elif event['type']=='update':
        stripe_integration.update_customer(event['data']['stripe_id'], **event['data'])
    elif event['type']=='delete':
        stripe_integration.delete_customer(event['data']['id'])

def start_outsync():
    consumer= get_consumer();
    for message in consumer:
        send_update_to_external_system(message.value)
        