"""Main test runner for benchmarking AI platforms."""

import json
import os
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import uuid

from .models import TestResult, PlatformResult, BenchmarkRun
from .platforms.base import AIPlatform
from .benchmarks.base import Benchmark
from .evaluators.base import Evaluator


class BenchmarkRunner:
    """Runs benchmarks across multiple AI platforms."""
    
    def __init__(self, 
                 platforms: List[AIPlatform],
                 benchmark: Benchmark,
                 evaluator: Evaluator,
                 results_dir: str = "./results"):
        """Initialize the benchmark runner.
        
        Args:
            platforms: List of AI platforms to test
            benchmark: Benchmark test suite to run
            evaluator: Evaluator for scoring responses
            results_dir: Directory to store results
        """
        self.platforms = platforms
        self.benchmark = benchmark
        self.evaluator = evaluator
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self, verbose: bool = True) -> BenchmarkRun:
        """Run the benchmark across all platforms.
        
        Args:
            verbose: Whether to print progress
            
        Returns:
            BenchmarkRun with all results
        """
        run_id = str(uuid.uuid4())
        platform_results = []
        
        questions = self.benchmark.get_questions()
        
        for platform in self.platforms:
            if not platform.is_available():
                if verbose:
                    print(f"⚠️  Skipping {platform.get_platform_name()} - not available (API key missing)")
                continue
            
            if verbose:
                print(f"\n{'='*60}")
                print(f"Testing: {platform.get_platform_name()} ({platform.get_model_name()})")
                print(f"{'='*60}")
            
            test_results = []
            
            for i, question in enumerate(questions, 1):
                if verbose:
                    print(f"\n[{i}/{len(questions)}] {question.category}: {question.question_id}")
                    print(f"Q: {question.prompt[:80]}..." if len(question.prompt) > 80 else f"Q: {question.prompt}")
                
                try:
                    # Query the platform
                    answer = platform.query(question.prompt)
                    
                    # Evaluate the answer
                    score, metrics = self.evaluator.evaluate(question, answer)
                    
                    test_result = TestResult(
                        question_id=question.question_id,
                        question=question.prompt,
                        answer=answer,
                        score=score,
                        metrics=metrics
                    )
                    
                    if verbose:
                        print(f"A: {answer[:100]}..." if len(answer) > 100 else f"A: {answer}")
                        print(f"Score: {score:.2f}")
                    
                except Exception as e:
                    if verbose:
                        print(f"❌ Error: {str(e)}")
                    
                    test_result = TestResult(
                        question_id=question.question_id,
                        question=question.prompt,
                        answer="",
                        score=0.0,
                        error=str(e)
                    )
                
                test_results.append(test_result)
            
            # Calculate overall score
            overall_score = sum(r.score for r in test_results) / len(test_results) if test_results else 0.0
            
            platform_result = PlatformResult(
                platform_name=platform.get_platform_name(),
                model_name=platform.get_model_name(),
                test_results=test_results,
                overall_score=overall_score,
                metadata={
                    "benchmark": self.benchmark.get_name(),
                    "benchmark_version": self.benchmark.get_version(),
                    "evaluator": self.evaluator.get_name()
                }
            )
            
            platform_results.append(platform_result)
            
            if verbose:
                print(f"\n{'='*60}")
                print(f"Overall Score: {overall_score:.2%}")
                print(f"{'='*60}")
        
        benchmark_run = BenchmarkRun(
            run_id=run_id,
            platform_results=platform_results,
            benchmark_version=self.benchmark.get_version()
        )
        
        # Save results
        self._save_results(benchmark_run)
        
        return benchmark_run
    
    def _save_results(self, benchmark_run: BenchmarkRun):
        """Save benchmark results to disk.
        
        Args:
            benchmark_run: The benchmark run to save
        """
        timestamp = benchmark_run.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_{timestamp}_{benchmark_run.run_id[:8]}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(benchmark_run.model_dump(), f, indent=2, default=str)
        
        print(f"\n✅ Results saved to: {filepath}")
