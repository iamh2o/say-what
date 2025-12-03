#!/usr/bin/env python3
"""Command-line interface for say-what."""

import argparse
import sys
from dotenv import load_dotenv

from .platforms import ClaudePlatform, OpenAIPlatform, GrokPlatform
from .benchmarks import StandardBenchmark
from .evaluators import KeywordEvaluator
from .runner import BenchmarkRunner
from .analyzer import ResultAnalyzer


def run_benchmark(args):
    """Run a new benchmark."""
    load_dotenv()
    
    # Initialize platforms based on arguments
    platforms = []
    
    if not args.platform or 'claude' in args.platform:
        platforms.append(ClaudePlatform())
    
    if not args.platform or 'openai' in args.platform:
        platforms.append(OpenAIPlatform())
    
    if not args.platform or 'grok' in args.platform:
        platforms.append(GrokPlatform())
    
    if not platforms:
        print("Error: No platforms specified or available.")
        return 1
    
    # Initialize benchmark and evaluator
    benchmark = StandardBenchmark()
    evaluator = KeywordEvaluator()
    
    # Run the benchmark
    runner = BenchmarkRunner(
        platforms=platforms,
        benchmark=benchmark,
        evaluator=evaluator,
        results_dir=args.results_dir
    )
    
    print(f"\nRunning {benchmark.get_name()} v{benchmark.get_version()}")
    print(f"Testing {len(platforms)} platform(s)")
    print()
    
    runner.run(verbose=not args.quiet)
    
    return 0


def show_report(args):
    """Show analysis report."""
    analyzer = ResultAnalyzer(results_dir=args.results_dir)
    report = analyzer.generate_report()
    print(report)
    return 0


def compare_platforms(args):
    """Compare platforms from latest or specific run."""
    analyzer = ResultAnalyzer(results_dir=args.results_dir)
    comparison = analyzer.compare_platforms(run_id=args.run_id)
    
    if "error" in comparison:
        print(f"Error: {comparison['error']}")
        return 1
    
    print("\n" + "=" * 70)
    print("PLATFORM COMPARISON")
    print("=" * 70)
    print(f"\nRun ID: {comparison['run_id']}")
    print(f"Timestamp: {comparison['timestamp']}")
    print("\nRankings:")
    
    for i, platform in enumerate(comparison['platforms'], 1):
        print(f"{i}. {platform['platform']} ({platform['model']})")
        print(f"   Score: {platform['overall_score']:.2%} ({platform['num_tests']} tests)")
    
    return 0


def check_degradation(args):
    """Check if a platform has degraded."""
    analyzer = ResultAnalyzer(results_dir=args.results_dir)
    
    platforms = args.platform or ['claude', 'openai', 'grok']
    
    for platform_name in platforms:
        result = analyzer.detect_degradation(platform_name, threshold=args.threshold)
        
        print(f"\n{platform_name.upper()}:")
        if result.get('reason'):
            print(f"  {result['reason']}")
        else:
            print(f"  Status: {'⚠️  DEGRADED' if result['degraded'] else '✅ OK'}")
            print(f"  First score: {result['first_score']:.2%}")
            print(f"  Last score:  {result['last_score']:.2%}")
            print(f"  Change:      {result['score_change']:+.2%} ({result['percent_change']:+.1f}%)")
            print(f"  Trend:       {result['trend']}")
            print(f"  Runs:        {result['num_runs']}")
    
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Say What? - Monitor AI intelligence over time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run benchmark on all platforms
  %(prog)s run
  
  # Run benchmark on specific platforms
  %(prog)s run --platform claude openai
  
  # Show analysis report
  %(prog)s report
  
  # Compare platforms
  %(prog)s compare
  
  # Check for degradation
  %(prog)s check --platform claude
        """
    )
    
    parser.add_argument(
        '--results-dir',
        default='./results',
        help='Directory for storing results (default: ./results)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run benchmark')
    run_parser.add_argument(
        '--platform',
        nargs='+',
        choices=['claude', 'openai', 'grok'],
        help='Specific platform(s) to test (default: all available)'
    )
    run_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress verbose output'
    )
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Show analysis report')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare platforms')
    compare_parser.add_argument(
        '--run-id',
        help='Specific run ID to compare (default: latest)'
    )
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check for degradation')
    check_parser.add_argument(
        '--platform',
        nargs='+',
        choices=['claude', 'openai', 'grok'],
        help='Platform(s) to check (default: all)'
    )
    check_parser.add_argument(
        '--threshold',
        type=float,
        default=0.05,
        help='Degradation threshold (default: 0.05 = 5%%)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    commands = {
        'run': run_benchmark,
        'report': show_report,
        'compare': compare_platforms,
        'check': check_degradation
    }
    
    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
