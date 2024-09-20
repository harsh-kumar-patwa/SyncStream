from flask import Blueprint, request, jsonify
from database.operations import create_customer

api = Blueprint('api',__name__)

@api.route('/customers',methods=['POST'])
def add_customer():
    data=request.json
    customer_id = create_customer(data['name'],data['email'])
    return jsonify({'id':customer_id}),201