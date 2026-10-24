from .payment_provider_factory import PaymentProviderFactory
from .payment_provider import PaymentProvider
from .stripe_authorizer import StripeAuthorizer
from .stripe_refund_processor import StripeRefundProcessor
from .stripe_webhook_verifier import StripeWebhookVerifier


class StripePaymentFactory(PaymentProviderFactory):

    def create_provider(self) -> PaymentProvider:
        return PaymentProvider(
            authorizer=StripeAuthorizer(),
            refunds=StripeRefundProcessor(),
            webhooks=StripeWebhookVerifier(),
        )