import pytest

from payment_integration.adyen_payment_factory import AdyenPaymentFactory
from payment_integration.mercado_pago_payment_factory import MercadoPagoPaymentFactory
from payment_integration.payment_authorizer import PaymentAuthorizer
from payment_integration.payment_provider import PaymentProvider
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
    provider = factory.create_provider()

    assert isinstance(factory, PaymentProviderFactory)
    assert isinstance(provider, PaymentProvider)
    assert isinstance(provider.authorizer, PaymentAuthorizer)
    assert isinstance(provider.refunds, RefundProcessor)
    assert isinstance(provider.webhooks, WebhookVerifier)


@pytest.mark.parametrize("factory_class, prefix", FAMILIES)
def test_every_product_of_a_factory_belongs_to_the_same_family(factory_class, prefix):
    provider = factory_class().create_provider()

    assert provider.authorizer.authorize(1).startswith(f"{prefix}:")
    assert provider.refunds.refund(1).startswith(f"{prefix}:")


@pytest.mark.parametrize("factory_class", [f for f, _ in FAMILIES])
def test_webhook_verifiers_reject_other_families_signatures(factory_class):
    verifier = factory_class().create_provider().webhooks
    valid = [s for s in ("stripe-valid", "adyen-valid", "mercado-pago-valid") if verifier.verify(s)]

    assert len(valid) == 1


def test_each_call_creates_a_new_family_instance():
    factory = StripePaymentFactory()

    assert factory.create_provider() is not factory.create_provider()


def test_provider_family_cannot_be_changed_after_creation():
    provider = AdyenPaymentFactory().create_provider()

    with pytest.raises(Exception):
        provider.webhooks = StripePaymentFactory().create_provider().webhooks


def test_contracts_cannot_be_instantiated_directly():
    for contract in (PaymentProviderFactory, PaymentAuthorizer, RefundProcessor, WebhookVerifier):
        with pytest.raises(TypeError):
            contract()
