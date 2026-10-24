import pytest

from payment_integration.adyen_payment_factory import AdyenPaymentFactory
from payment_integration.mercado_pago_payment_factory import MercadoPagoPaymentFactory
from payment_integration.payment_authorizer import PaymentAuthorizer
from payment_integration.payment_provider_factory import PaymentProviderFactory
from payment_integration.refund_processor import RefundProcessor
from payment_integration.stripe_payment_factory import StripePaymentFactory
from payment_integration.webhook_verifier import WebhookVerifier

FAMILIES = [
    (StripePaymentFactory, "stripe"),
    (AdyenPaymentFactory, "adyen"),
    (MercadoPagoPaymentFactory, "mercado_pago"),
]


@pytest.mark.parametrize("factory_class, prefix", FAMILIES)
def test_factory_fulfils_the_abstract_factory_contract(factory_class, prefix):
    factory = factory_class()

    assert isinstance(factory, PaymentProviderFactory)
    assert isinstance(factory.create_authorizer(), PaymentAuthorizer)
    assert isinstance(factory.create_refund_processor(), RefundProcessor)
    assert isinstance(factory.create_webhook_verifier(), WebhookVerifier)


@pytest.mark.parametrize("factory_class, prefix", FAMILIES)
def test_every_product_of_a_factory_belongs_to_the_same_family(factory_class, prefix):
    factory = factory_class()

    assert factory.create_authorizer().authorize(1).startswith(f"{prefix}:")
    assert factory.create_refund_processor().refund(1).startswith(f"{prefix}:")


@pytest.mark.parametrize("factory_class", [f for f, _ in FAMILIES])
def test_webhook_verifiers_reject_other_families_signatures(factory_class):
    verifier = factory_class().create_webhook_verifier()
    valid = [s for s in ("stripe-valid", "adyen-valid", "mercado-pago-valid") if verifier.verify(s)]

    assert len(valid) == 1


def test_contracts_cannot_be_instantiated_directly():
    for contract in (PaymentProviderFactory, PaymentAuthorizer, RefundProcessor, WebhookVerifier):
        with pytest.raises(TypeError):
            contract()
