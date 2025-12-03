"""OpenAI platform connector."""

import os
from typing import Optional
from .base import AIPlatform


class OpenAIPlatform(AIPlatform):
    """Connector for OpenAI (ChatGPT) AI platform."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize OpenAI platform connector.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (defaults to gpt-4-turbo-preview)
        """
        super().__init__(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            model=model or "gpt-4-turbo-preview"
        )
    
    def get_platform_name(self) -> str:
        """Return the name of the platform."""
        return "openai"
    
    def get_model_name(self) -> str:
        """Return the name of the model being used."""
        return self.model
    
    def query(self, prompt: str, **kwargs) -> str:
        """Send a query to OpenAI and return the response.
        
        Args:
            prompt: The question/prompt to send
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
            
        Returns:
            OpenAI's response as a string
            
        Raises:
            Exception: If the query fails
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        if not self.is_available():
            raise ValueError("OpenAI API key not set")
        
        client = OpenAI(api_key=self.api_key)
        
        max_tokens = kwargs.get("max_tokens", 1024)
        temperature = kwargs.get("temperature", 1.0)
        
        response = client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
