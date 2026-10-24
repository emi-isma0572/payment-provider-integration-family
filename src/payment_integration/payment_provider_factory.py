from abc import ABC, abstractmethod
from .payment_provider import PaymentProvider


class PaymentProviderFactory(ABC):

    @abstractmethod
    def create_provider(self) -> PaymentProvider:
        """Create a complete payment provider family."""
        pass