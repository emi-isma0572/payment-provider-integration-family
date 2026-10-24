from dataclasses import dataclass

from .payment_authorizer import PaymentAuthorizer
from .refund_processor import RefundProcessor
from .webhook_verifier import WebhookVerifier


@dataclass(frozen=True)
class PaymentProvider:
    authorizer: PaymentAuthorizer
    refunds: RefundProcessor
    webhooks: WebhookVerifier