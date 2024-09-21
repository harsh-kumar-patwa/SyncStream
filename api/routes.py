from flask import Blueprint, request, jsonify
from database.operations import create_customer,update_customer,delete_customer,get_customer,get_all_customers
from utils.kafka_client import send_event 
from sync.insync import sync_from_external
from config import ENABLED_INTEGRATIONS
import logging

api = Blueprint('api',__name__)
logger = logging.getLogger(__name__)

# Add user request
@api.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid input. Name and email are required.'}), 400

    customer_id, error = create_customer(data['name'], data['email'])
    
    if error:
        logger.error(f"Error creating customer: {error}")
        return jsonify({'error': error}), 409 if "already exists" in error else 500

    try:
        send_event('create', {'id': customer_id, 'name': data['name'], 'email': data['email']})
    except Exception as e:
        logger.error(f"Error sending create event to Kafka: {str(e)}")

    return jsonify({'id': customer_id,'name': data['name'],'email': data['email']}), 201


#Modify or Update user request
@api.route('/customers/<int:customer_id>', methods=['PUT'])
def modify_customer(customer_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    customer, error = get_customer(customer_id)
    if error:
        return jsonify({'error': error}), 404

    updated_customer, error = update_customer(customer_id, **data)

    if error:
        logger.error(f"Error updating customer {customer_id}: {error}")
        return jsonify({'error': error}), 500

    try:
        event_data = {'id': customer_id, **data}
        for integration in ENABLED_INTEGRATIONS:
            event_data[f'{integration}_id'] = updated_customer.get(f'{integration}_id')
        send_event('update', event_data)
    except Exception as e:
        logger.error(f"Error sending update event to Kafka: {str(e)}")
        return jsonify({'error':'Customer updated but could not send to External System'}), 409
    return jsonify({'success': True, 'customer': updated_customer}), 200


#Delete user request
@api.route('/customers/<int:customer_id>', methods=['DELETE'])
def remove_customer(customer_id):
    customer, error = get_customer(customer_id)
    if error:
        return jsonify({'error': error}), 404

    _, error = delete_customer(customer_id)
    if error:
        logger.error(f"Error deleting customer {customer_id}: {error}")
        return jsonify({'error': error}), 500

    try:
        event_data = {'id': customer_id}
        for integration in ENABLED_INTEGRATIONS:
            event_data[f'{integration}_id'] = customer.get(f'{integration}_id')
        send_event('delete', event_data)
    except Exception as e:
        logger.error(f"Error sending delete event to Kafka: {str(e)}")
        return jsonify({'error': 'Customer deleted but could not send to external systems'}), 409
    return jsonify({'success': True, 'message': 'Deletion successful'}), 200


# Webhook 
@api.route('/webhook/<integration>', methods=['POST'])
def external_webhook(integration):
    if integration not in ENABLED_INTEGRATIONS:
        return jsonify({'error': 'Unsupported integration'}), 400
    
    payload = request.json
    try:
        sync_from_external(integration, payload)
    except Exception as e:
        logger.exception(f"Error processing {integration} webhook: {str(e)}")
        return jsonify({'error': 'Error processing event'}), 500

    return jsonify({'success': True}), 200

# Get method for testing purpose
@api.route('/customers', methods=['GET'])
def get_customers():
    customers, error = get_all_customers()
    if error:
        logger.error(f"Error retrieving customers: {error}")
        return jsonify({'error': error}), 500
    return jsonify({'customers': customers}), 200

# Get single customer
@api.route('/customers/<int:customer_id>', methods=['GET'])
def get_single_customer(customer_id):
    customer, error = get_customer(customer_id)
    if error:
        logger.error(f"Error retrieving customer {customer_id}: {error}")
        return jsonify({'error': error}), 404 if "not found" in error.lower() else 500
    return jsonify({'customer': customer}), 200

