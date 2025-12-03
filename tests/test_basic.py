"""Basic tests for say-what framework components."""

import pytest
from say_what.benchmarks import StandardBenchmark
from say_what.benchmarks.base import Question
from say_what.evaluators import KeywordEvaluator
from say_what.models import TestResult, PlatformResult


def test_standard_benchmark():
    """Test that StandardBenchmark loads properly."""
    benchmark = StandardBenchmark()
    
    assert benchmark.get_name() == "Standard Intelligence Benchmark"
    assert benchmark.get_version() == "1.0"
    
    questions = benchmark.get_questions()
    assert len(questions) > 0
    assert all(isinstance(q, Question) for q in questions)


def test_keyword_evaluator():
    """Test KeywordEvaluator scoring."""
    evaluator = KeywordEvaluator()
    
    question = Question(
        question_id="test1",
        prompt="What is 2+2?",
        category="math",
        expected_elements=["4", "four"]
    )
    
    # Good answer
    score, metrics = evaluator.evaluate(question, "The answer is 4.")
    assert score > 0.0
    assert "4" in metrics["found_elements"]
    
    # Bad answer
    score, metrics = evaluator.evaluate(question, "I don't know.")
    assert score == 0.0
    assert len(metrics["found_elements"]) == 0


def test_question_creation():
    """Test Question object creation."""
    question = Question(
        question_id="test1",
        prompt="Test question?",
        category="test",
        expected_elements=["answer"],
        metadata={"difficulty": "easy"}
    )
    
    assert question.question_id == "test1"
    assert question.prompt == "Test question?"
    assert question.category == "test"
    assert "answer" in question.expected_elements
    assert question.metadata["difficulty"] == "easy"


def test_models():
    """Test data models."""
    # TestResult
    result = TestResult(
        question_id="q1",
        question="Test?",
        answer="Answer",
        score=0.8
    )
    assert result.score == 0.8
    assert result.question_id == "q1"
    
    # PlatformResult
    platform_result = PlatformResult(
        platform_name="test_platform",
        model_name="test_model",
        test_results=[result],
        overall_score=0.8
    )
    assert platform_result.platform_name == "test_platform"
    assert len(platform_result.test_results) == 1
    assert platform_result.overall_score == 0.8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
