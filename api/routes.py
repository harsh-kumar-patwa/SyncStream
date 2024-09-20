from flask import Blueprint, request, jsonify
from database.operations import create_customer,update_customer,delete_customer

api = Blueprint('api',__name__)

@api.route('/customers',methods=['POST'])
def add_customer():
    data=request.json
    customer_id = create_customer(data['name'],data['email'])
    #After sending the updates to the kafka client we will return
    return jsonify({'id':customer_id}),201

@api.route('/customers/<int:customer_id>',methods=['PUT'])
def modify_customer(customer_id):
    data = request.json
    updated_id = update_customer(customer_id, **data)
    if updated_id:
        #After sending the updates to the kafka client we will return
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Customer not found'}), 404

@api.route('/customers/<int:customer_id>', methods=['DELETE'])
def remove_customer(customer_id):
    deleted_id = delete_customer(customer_id)
    if deleted_id:
         #After sending the updates to the kafka client we will return
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Customer not found'}), 404




