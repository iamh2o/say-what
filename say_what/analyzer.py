"""Analyzer for comparing benchmark results over time."""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


class ResultAnalyzer:
    """Analyzes benchmark results to detect performance trends."""
    
    def __init__(self, results_dir: str = "./results"):
        """Initialize the analyzer.
        
        Args:
            results_dir: Directory containing result JSON files
        """
        self.results_dir = Path(results_dir)
    
    def load_results(self) -> List[Dict[str, Any]]:
        """Load all benchmark results from disk.
        
        Returns:
            List of result dictionaries
        """
        results = []
        
        if not self.results_dir.exists():
            return results
        
        for filepath in sorted(self.results_dir.glob("benchmark_*.json")):
            try:
                with open(filepath, 'r') as f:
                    result = json.load(f)
                    results.append(result)
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")
        
        return results
    
    def get_platform_trends(self, platform_name: str = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get score trends for platforms over time.
        
        Args:
            platform_name: Optional filter for specific platform
            
        Returns:
            Dictionary mapping platform names to list of score data points
        """
        results = self.load_results()
        trends = defaultdict(list)
        
        for result in results:
            timestamp = result.get('timestamp')
            
            for platform_result in result.get('platform_results', []):
                pname = platform_result['platform_name']
                
                if platform_name and pname != platform_name:
                    continue
                
                trends[pname].append({
                    'timestamp': timestamp,
                    'model': platform_result['model_name'],
                    'overall_score': platform_result['overall_score'],
                    'num_tests': len(platform_result['test_results'])
                })
        
        return dict(trends)
    
    def detect_degradation(self, platform_name: str, threshold: float = 0.05) -> Dict[str, Any]:
        """Detect if a platform's performance has degraded.
        
        Args:
            platform_name: Name of the platform to check
            threshold: Minimum score drop to consider degradation (default 5%)
            
        Returns:
            Dictionary with degradation analysis
        """
        trends = self.get_platform_trends(platform_name)
        
        if platform_name not in trends or len(trends[platform_name]) < 2:
            return {
                "platform": platform_name,
                "degraded": False,
                "reason": "Insufficient data for comparison"
            }
        
        data_points = trends[platform_name]
        
        # Compare first and last runs
        first_score = data_points[0]['overall_score']
        last_score = data_points[-1]['overall_score']
        
        score_change = last_score - first_score
        percent_change = (score_change / first_score) * 100 if first_score > 0 else 0
        
        degraded = score_change < -threshold
        
        return {
            "platform": platform_name,
            "degraded": degraded,
            "first_score": first_score,
            "last_score": last_score,
            "score_change": score_change,
            "percent_change": percent_change,
            "num_runs": len(data_points),
            "trend": "declining" if score_change < 0 else "improving"
        }
    
    def generate_report(self) -> str:
        """Generate a text report of all results.
        
        Returns:
            Formatted report string
        """
        results = self.load_results()
        
        if not results:
            return "No benchmark results found."
        
        report = []
        report.append("=" * 70)
        report.append("AI INTELLIGENCE MONITORING REPORT")
        report.append("=" * 70)
        report.append(f"\nTotal benchmark runs: {len(results)}")
        
        # Get all platforms
        all_platforms = set()
        for result in results:
            for pr in result.get('platform_results', []):
                all_platforms.add(pr['platform_name'])
        
        report.append(f"Platforms tested: {', '.join(sorted(all_platforms))}")
        
        # Trends for each platform
        report.append("\n" + "=" * 70)
        report.append("PLATFORM TRENDS")
        report.append("=" * 70)
        
        for platform in sorted(all_platforms):
            trends = self.get_platform_trends(platform)
            
            if platform not in trends:
                continue
            
            data = trends[platform]
            report.append(f"\n{platform.upper()}:")
            report.append(f"  Number of runs: {len(data)}")
            
            if len(data) >= 2:
                first = data[0]
                last = data[-1]
                change = last['overall_score'] - first['overall_score']
                pct_change = (change / first['overall_score']) * 100 if first['overall_score'] > 0 else 0
                
                report.append(f"  First run:  {first['overall_score']:.2%} ({first['timestamp'][:10]})")
                report.append(f"  Latest run: {last['overall_score']:.2%} ({last['timestamp'][:10]})")
                report.append(f"  Change:     {change:+.2%} ({pct_change:+.1f}%)")
                
                # Check for degradation
                degradation = self.detect_degradation(platform)
                if degradation['degraded']:
                    report.append(f"  ⚠️  DEGRADATION DETECTED")
            
            # Show all scores
            report.append(f"  Score history:")
            for d in data:
                report.append(f"    - {d['timestamp'][:19]}: {d['overall_score']:.2%}")
        
        return "\n".join(report)
    
    def compare_platforms(self, run_id: str = None) -> Dict[str, Any]:
        """Compare all platforms from a specific run (or latest).
        
        Args:
            run_id: Specific run ID, or None for latest
            
        Returns:
            Comparison data
        """
        results = self.load_results()
        
        if not results:
            return {"error": "No results found"}
        
        # Use latest if no run_id specified
        if run_id is None:
            target_result = results[-1]
        else:
            target_result = next((r for r in results if r['run_id'] == run_id), None)
            if not target_result:
                return {"error": f"Run {run_id} not found"}
        
        comparison = {
            "run_id": target_result['run_id'],
            "timestamp": target_result['timestamp'],
            "platforms": []
        }
        
        for pr in target_result['platform_results']:
            comparison['platforms'].append({
                "platform": pr['platform_name'],
                "model": pr['model_name'],
                "overall_score": pr['overall_score'],
                "num_tests": len(pr['test_results'])
            })
        
        # Sort by score
        comparison['platforms'].sort(key=lambda x: x['overall_score'], reverse=True)
        
        return comparison
