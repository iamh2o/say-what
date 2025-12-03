"""Composite evaluator that combines multiple evaluation strategies."""

from typing import Dict, Any, List
from .base import Evaluator
from ..benchmarks.base import Question


class CompositeEvaluator(Evaluator):
    """Combines multiple evaluators with weighted averaging."""
    
    def __init__(self, evaluators: List[tuple[Evaluator, float]]):
        """Initialize composite evaluator.
        
        Args:
            evaluators: List of (evaluator, weight) tuples
        """
        self.evaluators = evaluators
        total_weight = sum(weight for _, weight in evaluators)
        # Normalize weights
        self.evaluators = [(ev, w/total_weight) for ev, w in evaluators]
    
    def get_name(self) -> str:
        """Return the name of this evaluator."""
        return "CompositeEvaluator"
    
    def evaluate(self, question: Question, answer: str) -> tuple[float, Dict[str, Any]]:
        """Evaluate using all sub-evaluators and combine scores.
        
        Args:
            question: The question that was asked
            answer: The AI's response
            
        Returns:
            Tuple of (weighted_score, combined_metrics)
        """
        total_score = 0.0
        all_metrics = {}
        
        for evaluator, weight in self.evaluators:
            score, metrics = evaluator.evaluate(question, answer)
            total_score += score * weight
            all_metrics[evaluator.get_name()] = {
                "score": score,
                "weight": weight,
                "metrics": metrics
            }
        
        return total_score, all_metrics
