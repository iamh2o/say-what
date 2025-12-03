#!/usr/bin/env python3
"""
Demo script showing framework capabilities without requiring API keys.

This creates a mock platform for demonstration purposes.
"""

from typing import Optional
from say_what.platforms.base import AIPlatform
from say_what.benchmarks import StandardBenchmark
from say_what.evaluators import KeywordEvaluator
from say_what.runner import BenchmarkRunner
from say_what.analyzer import ResultAnalyzer


class MockAIPlatform(AIPlatform):
    """Mock AI platform for testing without API keys."""
    
    def __init__(self, name: str, performance_level: float = 0.8):
        """Initialize mock platform.
        
        Args:
            name: Platform name
            performance_level: Quality level (0.0 to 1.0)
        """
        super().__init__(api_key="mock_key", model=f"{name}-model")
        self.platform_name = name
        self.performance_level = performance_level
        
        # Mock responses that would score well
        self.mock_responses = {
            "logic": "No, we cannot conclude that some roses fade quickly, because the premise only states that some flowers fade quickly, not that all flowers do. This is a logical fallacy.",
            "reasoning": "If all but 9 die, then 9 sheep are left. The phrase 'all but 9' means all except 9.",
            "math": "The next number is 42. This is a sequence of n(n+1) where n increases: 1(2)=2, 2(3)=6, 3(4)=12, 4(5)=20, 5(6)=30, 6(7)=42.",
            "language": "Changing emphasis changes meaning: 'I didn't say...' (someone else did), 'I didn't SAY...' (I implied it), etc. Stress patterns create different implications.",
            "knowledge": "The capital of Australia is Canberra.",
            "problem_solving": "Fill the 5-gallon jug, pour into 3-gallon jug (2 gallons left in 5-gallon). Empty 3-gallon. Pour the 2 gallons into 3-gallon. Fill 5-gallon again. Pour into 3-gallon until full (1 gallon). Now 4 gallons remain in the 5-gallon jug.",
            "coding": "The time complexity of binary search is O(log n) because it divides the search space in half with each iteration.",
            "creative": "Three creative uses for a paperclip: 1) Unlock a simple lock, 2) Create a makeshift zipper pull, 3) Use as a bookmark or page marker.",
            "analytical": "This is a classic ethical dilemma weighing utilitarian versus deontological ethics. Utilitarian reasoning suggests maximizing overall good. Deontological ethics considers the moral rule against harming innocents. Both perspectives offer valid considerations.",
        }
    
    def get_platform_name(self) -> str:
        return self.platform_name
    
    def get_model_name(self) -> str:
        return self.model
    
    def query(self, prompt: str, **kwargs) -> str:
        """Return mock response based on question category."""
        # Simulate different performance levels
        import random
        
        # Find best matching category
        for category, response in self.mock_responses.items():
            if random.random() < self.performance_level:
                return response
        
        return "This is a generic response that may not score well."


def main():
    """Run demo with mock platforms."""
    print("=" * 70)
    print("SAY-WHAT FRAMEWORK DEMO")
    print("=" * 70)
    print("\nThis demo uses mock AI platforms to demonstrate functionality.")
    print("In production, you would use real platforms with API keys.\n")
    
    # Create mock platforms with different performance levels
    platforms = [
        MockAIPlatform("MockAI-Premium", performance_level=0.9),
        MockAIPlatform("MockAI-Standard", performance_level=0.7),
        MockAIPlatform("MockAI-Basic", performance_level=0.5),
    ]
    
    # Initialize benchmark and evaluator
    benchmark = StandardBenchmark()
    evaluator = KeywordEvaluator()
    
    print(f"Benchmark: {benchmark.get_name()} v{benchmark.get_version()}")
    print(f"Questions: {len(benchmark.get_questions())}")
    print(f"Platforms: {len(platforms)}\n")
    
    # Run benchmark
    runner = BenchmarkRunner(
        platforms=platforms,
        benchmark=benchmark,
        evaluator=evaluator,
        results_dir="./demo_results"
    )
    
    print("Running benchmark...\n")
    results = runner.run(verbose=False)
    
    # Show results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70 + "\n")
    
    for pr in sorted(results.platform_results, 
                     key=lambda x: x.overall_score, 
                     reverse=True):
        print(f"{pr.platform_name:20s} {pr.overall_score:6.1%}  ({pr.model_name})")
        
        # Show category breakdown
        category_scores = {}
        for tr in pr.test_results:
            cat = tr.question_id.split('_')[0]
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(tr.score)
        
        for cat, scores in sorted(category_scores.items()):
            avg_score = sum(scores) / len(scores)
            print(f"  {cat:20s} {avg_score:6.1%}")
        print()
    
    # Simulate running it again with degraded performance
    print("\n" + "=" * 70)
    print("SIMULATING SECOND RUN (with degraded performance)")
    print("=" * 70 + "\n")
    
    # Run again with lower performance
    degraded_platforms = [
        MockAIPlatform("MockAI-Premium", performance_level=0.7),  # Degraded from 0.9
        MockAIPlatform("MockAI-Standard", performance_level=0.6),  # Degraded from 0.7
        MockAIPlatform("MockAI-Basic", performance_level=0.4),     # Degraded from 0.5
    ]
    
    runner2 = BenchmarkRunner(
        platforms=degraded_platforms,
        benchmark=benchmark,
        evaluator=evaluator,
        results_dir="./demo_results"
    )
    
    results2 = runner2.run(verbose=False)
    
    # Analyze trends
    print("\n" + "=" * 70)
    print("TREND ANALYSIS")
    print("=" * 70 + "\n")
    
    analyzer = ResultAnalyzer(results_dir="./demo_results")
    
    for platform_name in ["MockAI-Premium", "MockAI-Standard", "MockAI-Basic"]:
        degradation = analyzer.detect_degradation(platform_name, threshold=0.05)
        
        if degradation.get('num_runs', 0) >= 2:
            print(f"{platform_name}:")
            print(f"  First run:  {degradation['first_score']:.1%}")
            print(f"  Latest run: {degradation['last_score']:.1%}")
            print(f"  Change:     {degradation['score_change']:+.1%} ({degradation['percent_change']:+.1f}%)")
            print(f"  Status:     {'⚠️  DEGRADED' if degradation['degraded'] else '✅ OK'}")
            print()
    
    print("\n" + "=" * 70)
    print("Demo complete! Check ./demo_results/ for saved data.")
    print("=" * 70)


if __name__ == '__main__':
    main()
