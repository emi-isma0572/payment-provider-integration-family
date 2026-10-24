from .payment_provider_factory import PaymentProviderFactory


class CheckoutService:
    """Checkout business logic.

    Depends only on the abstract factory and the abstract product roles.
    It never names Stripe, Adyen, Mercado Pago or any other concrete class:
    the provider family is injected from outside (dependency injection).
    """

    def __init__(self, provider_factory: PaymentProviderFactory):
        self._authorizer = provider_factory.create_authorizer()
        self._refunds = provider_factory.create_refund_processor()
        self._webhooks = provider_factory.create_webhook_verifier()

    def authorize_payment(self, amount: float) -> str:
        return self._authorizer.authorize(amount)

    def refund_payment(self, amount: float) -> str:
        return self._refunds.refund(amount)

    def verify_webhook(self, signature: str) -> bool:
        return self._webhooks.verify(signature)
