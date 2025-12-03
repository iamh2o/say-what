"""Keyword-based evaluator."""

from typing import Dict, Any
from .base import Evaluator
from ..benchmarks.base import Question


class KeywordEvaluator(Evaluator):
    """Evaluates responses based on presence of expected keywords/phrases."""
    
    def get_name(self) -> str:
        """Return the name of this evaluator."""
        return "KeywordEvaluator"
    
    def evaluate(self, question: Question, answer: str) -> tuple[float, Dict[str, Any]]:
        """Evaluate an answer based on keyword presence.
        
        Args:
            question: The question that was asked
            answer: The AI's response
            
        Returns:
            Tuple of (score, metrics)
        """
        if not answer:
            return 0.0, {"error": "Empty answer", "found_elements": []}
        
        answer_lower = answer.lower()
        expected = question.expected_elements
        
        if not expected:
            # No expected elements, give partial credit for providing an answer
            return 0.5, {"no_expected_elements": True, "answer_length": len(answer)}
        
        found = []
        for element in expected:
            if element.lower() in answer_lower:
                found.append(element)
        
        score = len(found) / len(expected) if expected else 0.0
        
        # Bonus points for comprehensive answers
        if len(answer) > 50 and score > 0:
            score = min(1.0, score + 0.1)
        
        metrics = {
            "expected_elements": len(expected),
            "found_elements": found,
            "found_count": len(found),
            "answer_length": len(answer),
            "raw_score": len(found) / len(expected) if expected else 0.0
        }
        
        return score, metrics
