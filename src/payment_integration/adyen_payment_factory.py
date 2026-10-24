from .payment_provider_factory import PaymentProviderFactory
from .payment_provider import PaymentProvider
from .adyen_authorizer import AdyenAuthorizer
from .adyen_refund_processor import AdyenRefundProcessor
from .adyen_webhook_verifier import AdyenWebhookVerifier


class AdyenPaymentFactory(PaymentProviderFactory):

    def create_provider(self) -> PaymentProvider:
        return PaymentProvider(
            authorizer=AdyenAuthorizer(),
            refunds=AdyenRefundProcessor(),
            webhooks=AdyenWebhookVerifier(),
        )