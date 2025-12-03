"""Base class for benchmark test suites."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Question:
    """A single test question."""
    
    def __init__(self, question_id: str, prompt: str, category: str, 
                 expected_elements: List[str] = None, metadata: Dict[str, Any] = None):
        """Initialize a question.
        
        Args:
            question_id: Unique identifier for the question
            prompt: The question text
            category: Category (e.g., reasoning, math, coding, knowledge)
            expected_elements: Key elements expected in a good answer
            metadata: Additional metadata about the question
        """
        self.question_id = question_id
        self.prompt = prompt
        self.category = category
        self.expected_elements = expected_elements or []
        self.metadata = metadata or {}


class Benchmark(ABC):
    """Abstract base class for benchmark test suites."""
    
    @abstractmethod
    def get_questions(self) -> List[Question]:
        """Return the list of questions in this benchmark.
        
        Returns:
            List of Question objects
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this benchmark.
        
        Returns:
            Benchmark name
        """
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Return the version of this benchmark.
        
        Returns:
            Version string
        """
        pass
