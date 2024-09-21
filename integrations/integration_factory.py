from .stripe_integration import StripeIntegration
import logging
logger = logging.getLogger(__name__)

# Integration factory is to make the product extensible for more sevice like Salesforce
class IntegrationFactory:
    @staticmethod
    def get_integration(integration_type):
        if integration_type == 'stripe':
            return StripeIntegration()
        else:
            logger.error(f"Unsupported integration type: {integration_type}")
            raise ValueError(f"Unsupported integration type: {integration_type}")