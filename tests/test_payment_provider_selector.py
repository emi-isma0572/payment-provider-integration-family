import pytest

from payment_integration.adyen_payment_factory import AdyenPaymentFactory
from payment_integration.checkout_service import CheckoutService
from payment_integration.mercado_pago_payment_factory import MercadoPagoPaymentFactory
from payment_integration.payment_provider_selector import PaymentProviderSelector
from payment_integration.stripe_payment_factory import StripePaymentFactory


@pytest.mark.parametrize(
    "name, factory_class",
    [
        ("stripe", StripePaymentFactory),
        ("adyen", AdyenPaymentFactory),
        ("mercado_pago", MercadoPagoPaymentFactory),
    ],
)
def test_selector_returns_the_matching_family(name, factory_class):
    assert isinstance(PaymentProviderSelector().factory_for(name), factory_class)


def test_unsupported_provider_is_rejected():
    with pytest.raises(ValueError, match="Unsupported provider"):
        PaymentProviderSelector().factory_for("paypal")


def test_selector_and_checkout_wire_together_end_to_end():
    factory = PaymentProviderSelector().factory_for("mercado_pago")
    checkout = CheckoutService(factory)

    assert checkout.authorize_payment(99.9) == "mercado_pago:authorized:99.90"


def test_selector_accepts_injected_factories():
    selector = PaymentProviderSelector({"only_stripe": StripePaymentFactory()})

    assert selector.supported_providers() == ["only_stripe"]
    with pytest.raises(ValueError):
        selector.factory_for("adyen")
