#!/usr/bin/env python3
"""
Example usage of the say-what framework.

This script demonstrates how to use the say-what framework programmatically.
"""

from dotenv import load_dotenv
from say_what.platforms import ClaudePlatform, OpenAIPlatform, GrokPlatform
from say_what.benchmarks import StandardBenchmark
from say_what.evaluators import KeywordEvaluator
from say_what.runner import BenchmarkRunner
from say_what.analyzer import ResultAnalyzer


def main():
    """Run a simple benchmark example."""
    # Load environment variables (API keys)
    load_dotenv()
    
    print("Say What? - AI Intelligence Monitoring Example")
    print("=" * 60)
    
    # Initialize platforms
    # Only platforms with valid API keys will be tested
    platforms = [
        ClaudePlatform(),
        OpenAIPlatform(),
        GrokPlatform()
    ]
    
    # Initialize benchmark and evaluator
    benchmark = StandardBenchmark()
    evaluator = KeywordEvaluator()
    
    # Create runner
    runner = BenchmarkRunner(
        platforms=platforms,
        benchmark=benchmark,
        evaluator=evaluator,
        results_dir="./results"
    )
    
    # Run the benchmark
    print(f"\nRunning benchmark: {benchmark.get_name()} v{benchmark.get_version()}")
    print(f"Number of questions: {len(benchmark.get_questions())}")
    print()
    
    benchmark_run = runner.run(verbose=True)
    
    # Analyze results
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    for platform_result in benchmark_run.platform_results:
        print(f"\n{platform_result.platform_name} ({platform_result.model_name}):")
        print(f"  Overall Score: {platform_result.overall_score:.2%}")
        print(f"  Tests Passed: {sum(1 for r in platform_result.test_results if r.score > 0.5)}/{len(platform_result.test_results)}")
    
    # Show trend analysis if we have multiple runs
    analyzer = ResultAnalyzer(results_dir="./results")
    print("\n" + "=" * 60)
    print("TREND ANALYSIS")
    print("=" * 60)
    
    for platform_result in benchmark_run.platform_results:
        degradation = analyzer.detect_degradation(platform_result.platform_name)
        if degradation.get('num_runs', 0) >= 2:
            print(f"\n{platform_result.platform_name}:")
            print(f"  Trend: {degradation['trend']}")
            print(f"  Change: {degradation['percent_change']:+.1f}%")
            if degradation['degraded']:
                print(f"  ⚠️  DEGRADATION DETECTED!")


if __name__ == '__main__':
    main()
