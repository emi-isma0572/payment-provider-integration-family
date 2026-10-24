import pytest

from payment_integration.adyen_payment_factory import AdyenPaymentFactory
from payment_integration.checkout_service import CheckoutService
from payment_integration.mercado_pago_payment_factory import MercadoPagoPaymentFactory
from payment_integration.payment_authorizer import PaymentAuthorizer
from payment_integration.payment_provider_factory import PaymentProviderFactory
from payment_integration.refund_processor import RefundProcessor
from payment_integration.stripe_payment_factory import StripePaymentFactory
from payment_integration.webhook_verifier import WebhookVerifier


# --- Test doubles: a fake family proves Checkout only needs the contracts ---

class FakeAuthorizer(PaymentAuthorizer):
    def authorize(self, amount: float) -> str:
        return f"fake:authorized:{amount:.2f}"


class FakeRefundProcessor(RefundProcessor):
    def refund(self, amount: float) -> str:
        return f"fake:refunded:{amount:.2f}"


class FakeWebhookVerifier(WebhookVerifier):
    def verify(self, signature: str) -> bool:
        return signature == "fake-valid"


class FakePaymentFactory(PaymentProviderFactory):
    def __init__(self):
        self.calls = []

    def create_authorizer(self) -> PaymentAuthorizer:
        self.calls.append("authorizer")
        return FakeAuthorizer()

    def create_refund_processor(self) -> RefundProcessor:
        self.calls.append("refund_processor")
        return FakeRefundProcessor()

    def create_webhook_verifier(self) -> WebhookVerifier:
        self.calls.append("webhook_verifier")
        return FakeWebhookVerifier()


# --- Existing behaviour preserved ---

def test_stripe_family_is_selected_together():
    checkout = CheckoutService(StripePaymentFactory())

    assert checkout.authorize_payment(125.50) == "stripe:authorized:125.50"
    assert checkout.refund_payment(25.00) == "stripe:refunded:25.00"
    assert checkout.verify_webhook("stripe-valid") is True
    assert checkout.verify_webhook("adyen-valid") is False


def test_adyen_family_is_selected_together():
    checkout = CheckoutService(AdyenPaymentFactory())

    assert checkout.authorize_payment(125.50) == "adyen:authorized:125.50"
    assert checkout.refund_payment(25.00) == "adyen:refunded:25.00"
    assert checkout.verify_webhook("adyen-valid") is True
    assert checkout.verify_webhook("stripe-valid") is False


# --- New family ---

def test_mercado_pago_family_is_selected_together():
    checkout = CheckoutService(MercadoPagoPaymentFactory())

    assert checkout.authorize_payment(125.50) == "mercado_pago:authorized:125.50"
    assert checkout.refund_payment(25.00) == "mercado_pago:refunded:25.00"
    assert checkout.verify_webhook("mercado-pago-valid") is True
    assert checkout.verify_webhook("stripe-valid") is False


# --- Checkout depends only on abstractions ---

def test_checkout_works_with_any_family_through_the_contract():
    factory = FakePaymentFactory()
    checkout = CheckoutService(factory)

    assert factory.calls == ["authorizer", "refund_processor", "webhook_verifier"]
    assert checkout.authorize_payment(10) == "fake:authorized:10.00"
    assert checkout.refund_payment(5) == "fake:refunded:5.00"
    assert checkout.verify_webhook("fake-valid") is True


def test_checkout_only_imports_abstractions():
    import ast
    from pathlib import Path

    import payment_integration.checkout_service as module

    tree = ast.parse(Path(module.__file__).read_text())
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert imported == {"payment_provider_factory"}
