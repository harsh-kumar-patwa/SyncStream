import stripe
from .base_integration import Integration
from config import INTEGRATIONS

# Stripe integration class implementation
class StripeIntegration(Integration):
    def __init__(self):
        stripe.api_key = INTEGRATIONS['stripe']['api_key']
        
    def create_customer(self, name, email):
        customer = stripe.Customer.create(name=name, email=email)
        return customer.id

    def update_customer(self, stripe_id, **kwargs):
        stripe.Customer.modify(stripe_id, **kwargs)

    def delete_customer(self, stripe_id):
        stripe_id=str(stripe_id)
        stripe.Customer.delete(stripe_id)