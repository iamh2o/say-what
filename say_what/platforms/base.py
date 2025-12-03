"""Base class for AI platform connectors."""

from abc import ABC, abstractmethod
from typing import Optional


class AIPlatform(ABC):
    """Abstract base class for AI platform connectors."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the platform connector.
        
        Args:
            api_key: API key for authentication
            model: Specific model to use (platform-specific)
        """
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Return the name of the platform."""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Return the name of the model being used."""
        pass
    
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> str:
        """Send a query to the AI platform and return the response.
        
        Args:
            prompt: The question/prompt to send
            **kwargs: Additional platform-specific parameters
            
        Returns:
            The AI's response as a string
            
        Raises:
            Exception: If the query fails
        """
        pass
    
    def is_available(self) -> bool:
        """Check if the platform is available (has valid credentials).
        
        Returns:
            True if platform can be used, False otherwise
        """
        return self.api_key is not None and len(self.api_key) > 0
