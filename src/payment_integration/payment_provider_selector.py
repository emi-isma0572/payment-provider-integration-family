from typing import Dict, List, Optional

from .adyen_payment_factory import AdyenPaymentFactory
from .mercado_pago_payment_factory import MercadoPagoPaymentFactory
from .payment_provider_factory import PaymentProviderFactory
from .stripe_payment_factory import StripePaymentFactory


class PaymentProviderSelector:
    """Composition root: the ONLY place that knows every concrete provider family.

    It turns a configuration value (e.g. "stripe") into a concrete factory object.
    Adding a new provider means a new family + one entry here; CheckoutService
    does not change.
    """

    def __init__(self, factories: Optional[Dict[str, PaymentProviderFactory]] = None):
        if factories is None:
            factories = {
                "stripe": StripePaymentFactory(),
                "adyen": AdyenPaymentFactory(),
                "mercado_pago": MercadoPagoPaymentFactory(),
            }
        self._factories = dict(factories)

    def factory_for(self, provider: str) -> PaymentProviderFactory:
        try:
            return self._factories[provider]
        except KeyError:
            raise ValueError(f"Unsupported provider: {provider}") from None

    def supported_providers(self) -> List[str]:
        return sorted(self._factories)
