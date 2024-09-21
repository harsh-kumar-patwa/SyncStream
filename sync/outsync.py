from utils.kafka_client import get_consumer
from integrations.stripe_integration import StripeIntegration
from database.operations import update_customer

stripe_integration = StripeIntegration()

# Sending action to external system 
def send_update_to_external_system(event):
    if event['type']=='create':
        stripe_id = stripe_integration.create_customer(event['data']['name'], event['data']['email'])
        update_customer(event['data']['id'], stripe_id=stripe_id)

    elif event['type'] == 'update':
        customer_id = event['data'].pop('id')
        stripe_id = event['data'].pop('stripe_id', None)
        if stripe_id:
            stripe_integration.update_customer(stripe_id, **event['data'])
        else:
            print(f"No Stripe ID found for customer {customer_id}")

    elif event['type'] == 'delete':
        stripe_id = event['data'].get('stripe_id')
        if stripe_id:
            stripe_integration.delete_customer(stripe_id)
        else:
            print(f"No Stripe ID found for customer {event['data'].get('id')}")

def start_outsync():
    consumer= get_consumer();
    for message in consumer:
        send_update_to_external_system(message.value)
        