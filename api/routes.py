from flask import Blueprint, request, jsonify
from database.operations import create_customer,update_customer,delete_customer
from utils.kafka_client import send_event 
from sync.insync import sync_from_stripe
from config import STRIPE_WEBHOOK_SECRET
import stripe

api = Blueprint('api',__name__)

@api.route('/customers',methods=['POST'])
def add_customer():
    data=request.json
    customer_id = create_customer(data['name'],data['email'])
    #After sending the updates to the kafka client we will return
    send_event('create',{'id':customer_id,'name':data['name'],'email':data['email']})
    return jsonify({'id':customer_id}),201

@api.route('/customers/<int:customer_id>',methods=['PUT'])
def modify_customer(customer_id):
    data = request.json
    customer_id_after_update = update_customer(customer_id, **data)
    if customer_id_after_update:
        #After sending the updates to the kafka client we will return
        send_event('update',{'id':customer_id_after_update,**data})
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Customer not found'}), 404

@api.route('/customers/<int:customer_id>', methods=['DELETE'])
def remove_customer(customer_id):
    id_after_delete = delete_customer(customer_id)
    if id_after_delete:
         #After sending the updates to the kafka client we will return
        send_event('delete', {'id': id_after_delete})
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Customer not found'}), 404

@api.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sign_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sign_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
    
    sync_from_stripe(event)
    return jsonify(success=True)



