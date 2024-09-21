from database.operations import create_customer, update_customer, delete_customer, get_customer_by_external_id, get_customer_by_email
from integrations.integration_factory import IntegrationFactory
import logging

logger = logging.getLogger(__name__)

# Sync from External service 
def sync_from_external(integration_type, event):
    integration = IntegrationFactory.get_integration(integration_type)
    event_type = event['type']
    event_data = event['data']['object']

    logger.info(f"Processing {integration_type} event: {event_type}")

    try:
        if event_type == 'customer.created':
            handle_customer_created(integration_type, event_data)
        elif event_type == 'customer.updated':
            handle_customer_updated(integration_type, event_data)
        elif event_type == 'customer.deleted':
            handle_customer_deleted(integration_type, event_data)
        else:
            logger.info(f"Unhandled event type: {event_type}")

    except Exception as e:
        logger.exception(f"Error processing {integration_type} event {event_type}: {str(e)}")
        raise

# Handling customer creation here
def handle_customer_created(integration_type, event_data):
    name = event_data.get('name', '')
    email = event_data.get('email', '')
    external_id = event_data.get('id')

    if not external_id or not email:
        logger.error(f"{integration_type} customer ID or email is missing from the event data")
        return

    existing_customer, _ = get_customer_by_email(email)
    
    if existing_customer:
        updated_customer, error = update_customer(
            existing_customer['id'],
            **{f"{integration_type}_id": external_id}
        )
        if error:
            logger.error(f"Error updating existing customer with {integration_type} ID: {error}")
        else:
            logger.info(f"Updated existing customer (ID: {existing_customer['id']}) with {integration_type} ID: {external_id}")
    else:
        customer_id, error = create_customer(
            name=name,
            email=email,
            **{f"{integration_type}_id": external_id}
        )
        if error:
            logger.error(f"Error creating customer from {integration_type}: {error}")
        else:
            logger.info(f"Created customer with ID {customer_id} from {integration_type} event")

# Handling customer updation heree
def handle_customer_updated(integration_type, event_data):
    external_id = event_data.get('id')
    if not external_id:
        logger.error(f"{integration_type} customer ID is missing from the event data")
        return

    customer, error = get_customer_by_external_id(f'{integration_type}_id', external_id)
    if customer:
        name = event_data.get('name', customer['name'])
        email = event_data.get('email', customer['email'])
        
        updated_customer, error = update_customer(
            customer['id'],
            name=name,
            email=email
        )
        if error:
            logger.error(f"Error updating customer from {integration_type}: {error}")
        else:
            logger.info(f"Updated customer with ID {customer['id']} from {integration_type} event")
    else:
        logger.warning(f"Customer with {integration_type} ID {external_id} not found in local database")

# Handling customer deletion
def handle_customer_deleted(integration_type, event_data):
    external_id = event_data.get('id')
    if not external_id:
        logger.error(f"{integration_type} customer ID is missing from the event data")
        return

    customer, error = get_customer_by_external_id(f'{integration_type}_id', external_id)
    if customer:
        deleted_id, error = delete_customer(customer['id'])
        if error:
            logger.error(f"Error deleting customer from local database: {error}")
        else:
            logger.info(f"Deleted customer with ID {customer['id']} from local database")
    else:
        logger.info(f"Customer with {integration_type} ID {external_id} not found in local database. It may have been already deleted.")