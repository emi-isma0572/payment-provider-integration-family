from abc import ABC, abstractmethod


class RefundProcessor(ABC):
    """Product role: returns money to the customer through a payment provider."""

    @abstractmethod
    def refund(self, amount: float) -> str:
        """Refund the amount and return a provider confirmation reference."""
