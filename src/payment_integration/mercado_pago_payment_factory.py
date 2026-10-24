from .payment_provider_factory import PaymentProviderFactory
from .payment_provider import PaymentProvider
from .mercado_pago_authorizer import MercadoPagoAuthorizer
from .mercado_pago_refund_processor import MercadoPagoRefundProcessor
from .mercado_pago_webhook_verifier import MercadoPagoWebhookVerifier


class MercadoPagoPaymentFactory(PaymentProviderFactory):

    def create_provider(self) -> PaymentProvider:
        return PaymentProvider(
            authorizer=MercadoPagoAuthorizer(),
            refunds=MercadoPagoRefundProcessor(),
            webhooks=MercadoPagoWebhookVerifier(),
        )