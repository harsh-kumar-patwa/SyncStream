from database.operations import create_customer,update_customer, delete_customer,get_customer_by_external_id,get_customer_by_email
import logging

logger = logging.getLogger(__name__)

def sync_from_stripe(event):
    event_type = event['type']
    event_data = event['data']['object']

    logger.info(f"Processing Stripe event: {event_type}")

    try:
        if event_type == 'customer.created':
            name = event_data.get('name', '')
            email = event_data.get('email', '')
            stripe_id = event_data.get('id')

            if not stripe_id or not email:
                logger.error("Stripe customer ID or email is missing from the event data")
                return

            existing_customer, _ = get_customer_by_email(email)
            
            if existing_customer:
                updated_customer, error = update_customer(
                    existing_customer['id'],
                    stripe_id=stripe_id
                )
                if error:
                    logger.error(f"Error updating existing customer with Stripe ID: {error}")
                else:
                    logger.info(f"Updated existing customer (ID: {existing_customer['id']}) with Stripe ID: {stripe_id}")
            else:
                customer_id, error = create_customer(
                    name=name,
                    email=email,
                    stripe_id=stripe_id
                )
                if error:
                    logger.error(f"Error creating customer from Stripe: {error}")
                else:
                    logger.info(f"Created customer with ID {customer_id} from Stripe event")
        
        elif event_type == 'customer.updated':
            stripe_id = event_data.get('id')
            if not stripe_id:
                logger.error("Stripe customer ID is missing from the event data")
                return

            customer, error = get_customer_by_external_id('stripe_id', stripe_id)
            if customer:
                name = event_data.get('name', customer['name'])
                email = event_data.get('email', customer['email'])
                
                updated_customer, error = update_customer(
                    customer['id'],
                    name=name,
                    email=email
                )
                if error:
                    logger.error(f"Error updating customer from Stripe: {error}")
                else:
                    logger.info(f"Updated customer with ID {customer['id']} from Stripe event")
            else:
                logger.warning(f"Customer with Stripe ID {stripe_id} not found in local database")
        
        elif event_type == 'customer.deleted':
            stripe_id = event_data.get('id')
            if not stripe_id:
                logger.error("Stripe customer ID is missing from the event data")
                return

            customer, error = get_customer_by_external_id('stripe_id', stripe_id)
            if customer:
                deleted_id, error = delete_customer(customer['id'])
                if error:
                    logger.error(f"Error deleting customer from local database: {error}")
                else:
                    logger.info(f"Deleted customer with ID {customer['id']} from local database")
            else:
                logger.info(f"Customer with Stripe ID {stripe_id} not found in local database. It may have been already deleted.")
        
        else:
            logger.info(f"Unhandled event type: {event_type}")

    except Exception as e:
        logger.exception(f"Error processing Stripe event {event_type}: {str(e)}")
        raise