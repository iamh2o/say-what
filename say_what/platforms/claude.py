"""Claude (Anthropic) platform connector."""

import os
from typing import Optional
from .base import AIPlatform


class ClaudePlatform(AIPlatform):
    """Connector for Claude (Anthropic) AI platform."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize Claude platform connector.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use (defaults to claude-3-5-sonnet-20241022)
        """
        super().__init__(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
            model=model or "claude-3-5-sonnet-20241022"
        )
    
    def get_platform_name(self) -> str:
        """Return the name of the platform."""
        return "claude"
    
    def get_model_name(self) -> str:
        """Return the name of the model being used."""
        return self.model
    
    def query(self, prompt: str, **kwargs) -> str:
        """Send a query to Claude and return the response.
        
        Args:
            prompt: The question/prompt to send
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
            
        Returns:
            Claude's response as a string
            
        Raises:
            Exception: If the query fails
        """
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        
        if not self.is_available():
            raise ValueError("Claude API key not set")
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        max_tokens = kwargs.get("max_tokens", 1024)
        temperature = kwargs.get("temperature", 1.0)
        
        message = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
