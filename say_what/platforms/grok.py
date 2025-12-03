"""Grok (xAI) platform connector."""

import os
from typing import Optional
from .base import AIPlatform


class GrokPlatform(AIPlatform):
    """Connector for Grok (xAI) AI platform."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize Grok platform connector.
        
        Args:
            api_key: Grok API key (defaults to GROK_API_KEY env var)
            model: Model to use (defaults to grok-beta)
        """
        super().__init__(
            api_key=api_key or os.getenv("GROK_API_KEY"),
            model=model or "grok-beta"
        )
    
    def get_platform_name(self) -> str:
        """Return the name of the platform."""
        return "grok"
    
    def get_model_name(self) -> str:
        """Return the name of the model being used."""
        return self.model
    
    def query(self, prompt: str, **kwargs) -> str:
        """Send a query to Grok and return the response.
        
        Args:
            prompt: The question/prompt to send
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
            
        Returns:
            Grok's response as a string
            
        Raises:
            Exception: If the query fails
        """
        try:
            import requests
        except ImportError:
            raise ImportError("requests package not installed. Run: pip install requests")
        
        if not self.is_available():
            raise ValueError("Grok API key not set")
        
        # Note: Grok uses OpenAI-compatible API
        # Base URL for xAI API
        base_url = "https://api.x.ai/v1"
        
        max_tokens = kwargs.get("max_tokens", 1024)
        temperature = kwargs.get("temperature", 1.0)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result["choices"][0]["message"]["content"]
