from abc import ABC, abstractmethod


class PaymentAuthorizer(ABC):
    """Product role: reserves (authorizes) an amount with a payment provider."""

    @abstractmethod
    def authorize(self, amount: float) -> str:
        """Authorize the amount and return a provider confirmation reference."""
