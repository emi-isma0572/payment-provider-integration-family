from .payment_provider_factory import PaymentProviderFactory


class CheckoutService:

    def __init__(self, provider_factory: PaymentProviderFactory):
        self._provider = provider_factory.create_provider()

    def authorize_payment(self, amount: float) -> str:
        return self._provider.authorizer.authorize(amount)

    def refund_payment(self, amount: float) -> str:
        return self._provider.refunds.refund(amount)

    def verify_webhook(self, signature: str) -> bool:
        return self._provider.webhooks.verify(signature)