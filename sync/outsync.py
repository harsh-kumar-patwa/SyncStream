from utils.kafka_client import get_consumer
from database.operations import update_customer
from integrations.integration_factory import IntegrationFactory
from config import ENABLED_INTEGRATIONS

# Sending action to external system 
def send_update_to_external_system(event):
    for integration_type in ENABLED_INTEGRATIONS:
        integration = IntegrationFactory.get_integration(integration_type)

        if event['type'] == 'create':
            external_id = integration.create_customer(event['data']['name'], event['data']['email'])
            update_customer(event['data']['id'], **{f"{integration_type}_id": external_id})

        elif event['type'] == 'update':
            customer_id = event['data'].pop('id')
            external_id = event['data'].pop(f'{integration_type}_id', None)
            if external_id:
                integration.update_customer(external_id, **event['data'])
            else:
                print(f"No {integration_type} ID found for customer {customer_id}")

        elif event['type'] == 'delete':
            external_id = event['data'].get(f'{integration_type}_id')
            if external_id:
                integration.delete_customer(external_id)
            else:
                print(f"No {integration_type} ID found for customer {event['data'].get('id')}")

# Start the outsyn
def start_outsync():
    consumer= get_consumer();
    for message in consumer:
        send_update_to_external_system(message.value)
        