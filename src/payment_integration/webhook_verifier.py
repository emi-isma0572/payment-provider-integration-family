from abc import ABC, abstractmethod


class WebhookVerifier(ABC):
    """Product role: checks that an incoming webhook really comes from the provider."""

    @abstractmethod
    def verify(self, signature: str) -> bool:
        """Return True only if the signature is valid for this provider."""
