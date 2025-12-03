"""Base class for answer evaluators."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from ..benchmarks.base import Question


class Evaluator(ABC):
    """Abstract base class for evaluating AI responses."""
    
    @abstractmethod
    def evaluate(self, question: Question, answer: str) -> Tuple[float, Dict[str, Any]]:
        """Evaluate an AI's answer to a question.
        
        Args:
            question: The question that was asked
            answer: The AI's response
            
        Returns:
            Tuple of (score, metrics) where:
                - score is a float between 0.0 and 1.0
                - metrics is a dict with additional evaluation details
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this evaluator.
        
        Returns:
            Evaluator name
        """
        pass
