from abc import ABC, abstractmethod

from .payment_authorizer import PaymentAuthorizer
from .refund_processor import RefundProcessor
from .webhook_verifier import WebhookVerifier


class PaymentProviderFactory(ABC):
    """Abstract Factory: the single creation boundary for one complete provider family.

    Every concrete factory must return products that belong to the SAME provider,
    so Checkout can never mix, e.g., a Stripe authorizer with an Adyen verifier.
    """

    @abstractmethod
    def create_authorizer(self) -> PaymentAuthorizer:
        """Create the authorization product of this family."""

    @abstractmethod
    def create_refund_processor(self) -> RefundProcessor:
        """Create the refund product of this family."""

    @abstractmethod
    def create_webhook_verifier(self) -> WebhookVerifier:
        """Create the webhook-verification product of this family."""
