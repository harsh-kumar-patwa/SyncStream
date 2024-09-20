import stripe
from .base_integration import Integration
from config import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

class StripeIntegration(Integration):
    def create_customer(self, name, email):
        customer = stripe.Customer.create(name=name, email=email)
        return customer.id

    def update_customer(self, stripe_id, **kwargs):
        stripe.Customer.modify(stripe_id, **kwargs)

    def delete_customer(self, stripe_id):
        stripe_id=str(stripe_id)
        stripe.Customer.delete(stripe_id)