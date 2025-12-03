# Usage Guide

## Getting Started

### 1. Install the package

```bash
pip install -e .
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GROK_API_KEY=xai-...
```

### 3. Run Your First Benchmark

```bash
python -m say_what.cli run
```

This will:
- Test all AI platforms with valid API keys
- Run the standard benchmark (12 questions)
- Save results to `./results/`
- Display scores for each platform

## Command Reference

### Run Benchmarks

Test all platforms:
```bash
python -m say_what.cli run
```

Test specific platforms:
```bash
python -m say_what.cli run --platform claude openai
```

Quiet mode (less output):
```bash
python -m say_what.cli run --quiet
```

Custom results directory:
```bash
python -m say_what.cli run --results-dir ./my_results
```

### View Reports

Show full analysis report:
```bash
python -m say_what.cli report
```

Compare platforms from latest run:
```bash
python -m say_what.cli compare
```

Compare specific run:
```bash
python -m say_what.cli compare --run-id abc123
```

### Check for Degradation

Check all platforms:
```bash
python -m say_what.cli check
```

Check specific platform:
```bash
python -m say_what.cli check --platform claude
```

Custom degradation threshold (default 5%):
```bash
python -m say_what.cli check --threshold 0.1  # 10%
```

## Programmatic Usage

### Basic Example

```python
from dotenv import load_dotenv
from say_what.platforms import ClaudePlatform, OpenAIPlatform
from say_what.benchmarks import StandardBenchmark
from say_what.evaluators import KeywordEvaluator
from say_what.runner import BenchmarkRunner

load_dotenv()

platforms = [ClaudePlatform(), OpenAIPlatform()]
benchmark = StandardBenchmark()
evaluator = KeywordEvaluator()

runner = BenchmarkRunner(platforms, benchmark, evaluator)
results = runner.run(verbose=True)

for pr in results.platform_results:
    print(f"{pr.platform_name}: {pr.overall_score:.2%}")
```

### Analyzing Results

```python
from say_what.analyzer import ResultAnalyzer

analyzer = ResultAnalyzer(results_dir="./results")

# Get trends for a platform
trends = analyzer.get_platform_trends("claude")

# Check for degradation
degradation = analyzer.detect_degradation("claude", threshold=0.05)
if degradation['degraded']:
    print(f"Warning: {degradation['platform']} has degraded!")
    print(f"Change: {degradation['percent_change']:.1f}%")

# Generate full report
report = analyzer.generate_report()
print(report)
```

### Custom Benchmarks

```python
from say_what.benchmarks.base import Benchmark, Question

class MyBenchmark(Benchmark):
    def get_name(self):
        return "My Custom Benchmark"
    
    def get_version(self):
        return "1.0"
    
    def get_questions(self):
        return [
            Question(
                question_id="custom1",
                prompt="What is machine learning?",
                category="knowledge",
                expected_elements=["algorithm", "data", "learn", "pattern"]
            ),
            # Add more questions...
        ]

# Use it
benchmark = MyBenchmark()
runner = BenchmarkRunner(platforms, benchmark, evaluator)
results = runner.run()
```

### Custom Evaluators

```python
from say_what.evaluators.base import Evaluator
import re

class LengthEvaluator(Evaluator):
    """Scores based on answer length."""
    
    def get_name(self):
        return "LengthEvaluator"
    
    def evaluate(self, question, answer):
        # Expect answers between 50-500 chars
        length = len(answer)
        if 50 <= length <= 500:
            score = 1.0
        elif length < 50:
            score = length / 50.0
        else:
            score = max(0.5, 1.0 - (length - 500) / 1000)
        
        metrics = {"length": length}
        return score, metrics
```

### Combining Evaluators

```python
from say_what.evaluators import KeywordEvaluator, CompositeEvaluator

evaluator = CompositeEvaluator([
    (KeywordEvaluator(), 0.7),  # 70% weight
    (LengthEvaluator(), 0.3)     # 30% weight
])
```

## Monitoring Over Time

### Regular Testing Schedule

Set up a cron job or scheduled task:

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/say-what && python -m say_what.cli run --quiet
```

### Automated Alerts

```python
from say_what.analyzer import ResultAnalyzer

analyzer = ResultAnalyzer()
platforms = ["claude", "openai", "grok"]

for platform in platforms:
    result = analyzer.detect_degradation(platform, threshold=0.05)
    if result.get('degraded'):
        # Send alert (email, Slack, etc.)
        print(f"ALERT: {platform} performance degraded by {result['percent_change']:.1f}%")
```

## Tips and Best Practices

1. **Run Regularly**: Schedule benchmarks to run at consistent intervals (daily/weekly)
2. **Track All Platforms**: Monitor multiple platforms to understand relative changes
3. **Keep Results**: Don't delete old results - trends require historical data
4. **Use Consistent Questions**: Don't change benchmark questions to maintain comparability
5. **Version Control**: Track benchmark versions to understand what changed
6. **Set Appropriate Thresholds**: 5% is default, but adjust based on your needs
7. **Consider Rate Limits**: Space out API calls to avoid rate limiting

## Troubleshooting

### "API key not set" error
- Check that `.env` file exists and contains the API key
- Verify the key name matches (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.)
- Ensure `.env` is in the current working directory

### Platform skipped
- Platform is skipped if no API key is configured
- This is normal - you don't need all platforms configured

### Import errors
- Run `pip install -e .` to install the package
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Rate limiting
- Add delays between questions if needed
- Use different API keys for different runs
- Reduce frequency of benchmark runs

## Result File Format

Results are stored as JSON files:

```json
{
  "run_id": "abc123",
  "timestamp": "2024-12-03T12:00:00",
  "benchmark_version": "1.0",
  "platform_results": [
    {
      "platform_name": "claude",
      "model_name": "claude-3-5-sonnet-20241022",
      "overall_score": 0.85,
      "test_results": [
        {
          "question_id": "logic_001",
          "question": "If all roses are flowers...",
          "answer": "No, we cannot conclude...",
          "score": 0.9,
          "metrics": {...}
        }
      ]
    }
  ]
}
```
