from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a model response for the given prompt."""
        pass