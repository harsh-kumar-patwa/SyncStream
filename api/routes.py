from flask import Blueprint, request, jsonify
from database.operations import create_customer,update_customer,delete_customer,get_customer,get_all_customers
from utils.kafka_client import send_event 
from sync.insync import sync_from_stripe
from config import STRIPE_WEBHOOK_SECRET
import stripe
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
        send_event('update', {'id':customer_id,'stripe_id': updated_customer['stripe_id'], **data})
    except Exception as e:
        logger.error(f"Error sending update event to Kafka: {str(e)}")
        return jsonify({'error':'Customer updated but could not send to Stripe'}), 409
    return jsonify({'success': True, 'customer': updated_customer}), 200


#Delete user request
@api.route('/customers/<int:customer_id>', methods=['DELETE'])
def remove_customer(customer_id):
    stripe_id, error = delete_customer(int(customer_id))
    if error:
        logger.error(f"Error deleting customer {customer_id}: {error}")
        return jsonify({'error': error}), 404 if "not found" in error.lower() else 500

    try:
        send_event('delete', {'id':customer_id,'stripe_id': stripe_id})
    except Exception as e:
        logger.error(f"Error sending delete event to Kafka: {str(e)}")
        return jsonify({'error':'Customer deleted but could not send to Stripe'}), 409
    return jsonify({'success': True,'message':'Deletion successful'}), 200


#Webhook 
@api.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return jsonify({'error': 'Invalid signature'}), 400

    try:
        sync_from_stripe(event)
    except Exception as e:
        logger.exception(f"Error processing Stripe event: {str(e)}")
        return jsonify({'error': 'Error processing event'}), 500

    return jsonify({'success': True}), 200

@api.route('/customers', methods=['GET'])
def get_customers():
    customers, error = get_all_customers()
    if error:
        logger.error(f"Error retrieving customers: {error}")
        return jsonify({'error': error}), 500
    return jsonify({'customers': customers}), 200

@api.route('/customers/<int:customer_id>', methods=['GET'])
def get_single_customer(customer_id):
    customer, error = get_customer(customer_id)
    if error:
        logger.error(f"Error retrieving customer {customer_id}: {error}")
        return jsonify({'error': error}), 404 if "not found" in error.lower() else 500
    return jsonify({'customer': customer}), 200

