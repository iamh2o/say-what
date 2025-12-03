# say-what

Framework to monitor public facing AI intelligence over time.

## Overview

**say-what** is a Python framework designed to probe and assess AI platforms (Claude, ChatGPT, Grok, etc.) to detect if their intelligence has been "dialed down" over time. It provides:

- 🎯 Standardized benchmark tests across multiple domains (logic, math, language, coding, etc.)
- 🤖 Support for multiple AI platforms (Claude, OpenAI, Grok)
- 📊 Automated scoring and evaluation
- 📈 Trend analysis to detect performance degradation
- 💾 Historical result tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/iamh2o/say-what.git
cd say-what
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Quick Start

### Command Line Interface

Run a benchmark on all available platforms:
```bash
python -m say_what.cli run
```

Run on specific platforms:
```bash
python -m say_what.cli run --platform claude openai
```

Show analysis report:
```bash
python -m say_what.cli report
```

Compare platforms from latest run:
```bash
python -m say_what.cli compare
```

Check for degradation:
```bash
python -m say_what.cli check --platform claude
```

### Programmatic Usage

```python
from dotenv import load_dotenv
from say_what.platforms import ClaudePlatform, OpenAIPlatform
from say_what.benchmarks import StandardBenchmark
from say_what.evaluators import KeywordEvaluator
from say_what.runner import BenchmarkRunner

load_dotenv()

# Set up platforms
platforms = [ClaudePlatform(), OpenAIPlatform()]

# Run benchmark
runner = BenchmarkRunner(
    platforms=platforms,
    benchmark=StandardBenchmark(),
    evaluator=KeywordEvaluator()
)

results = runner.run()
```

See `example.py` for a complete example.

## Architecture

### Components

1. **Platforms** (`say_what/platforms/`): Connectors for different AI services
   - `ClaudePlatform`: Anthropic's Claude
   - `OpenAIPlatform`: OpenAI's GPT models
   - `GrokPlatform`: xAI's Grok

2. **Benchmarks** (`say_what/benchmarks/`): Test suites with questions
   - `StandardBenchmark`: Diverse questions across multiple domains

3. **Evaluators** (`say_what/evaluators/`): Scoring mechanisms
   - `KeywordEvaluator`: Scores based on expected keywords/phrases
   - `CompositeEvaluator`: Combines multiple evaluation strategies

4. **Runner** (`say_what/runner.py`): Executes benchmarks across platforms

5. **Analyzer** (`say_what/analyzer.py`): Analyzes results and detects trends

### Benchmark Categories

The Standard Benchmark includes questions in:
- Logic and reasoning
- Mathematics
- Language understanding
- General knowledge
- Problem solving
- Coding/algorithms
- Creative thinking
- Analytical thinking

## API Keys

You need API keys for the platforms you want to test:

- **Claude**: Get from [Anthropic Console](https://console.anthropic.com/)
- **OpenAI**: Get from [OpenAI Platform](https://platform.openai.com/)
- **Grok**: Get from [xAI Console](https://console.x.ai/)

Add them to `.env`:
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GROK_API_KEY=your_key_here
```

## Results

Results are stored as JSON files in the `results/` directory with timestamps. Each result includes:
- Platform and model information
- Individual question scores
- Overall platform score
- Detailed metrics

## Extending the Framework

### Adding a New Platform

```python
from say_what.platforms.base import AIPlatform

class MyPlatform(AIPlatform):
    def get_platform_name(self) -> str:
        return "my_platform"
    
    def get_model_name(self) -> str:
        return self.model
    
    def query(self, prompt: str, **kwargs) -> str:
        # Implement API call
        pass
```

### Creating Custom Benchmarks

```python
from say_what.benchmarks.base import Benchmark, Question

class MyBenchmark(Benchmark):
    def get_name(self) -> str:
        return "My Custom Benchmark"
    
    def get_version(self) -> str:
        return "1.0"
    
    def get_questions(self):
        return [
            Question(
                question_id="q1",
                prompt="Your question here",
                category="category",
                expected_elements=["keyword1", "keyword2"]
            )
        ]
```

### Custom Evaluators

```python
from say_what.evaluators.base import Evaluator

class MyEvaluator(Evaluator):
    def get_name(self) -> str:
        return "MyEvaluator"
    
    def evaluate(self, question, answer):
        # Your evaluation logic
        score = 0.0  # 0.0 to 1.0
        metrics = {}
        return score, metrics
```

## Use Cases

1. **Monitor AI Platform Changes**: Track if your favorite AI becomes less capable over time
2. **Compare Platforms**: See which AI performs best on different types of tasks
3. **Version Testing**: Test different model versions side-by-side
4. **Quality Assurance**: Ensure AI performance meets your standards
5. **Research**: Study AI behavior and capabilities over time

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This framework was created to address concerns about potential "intelligence degradation" in AI platforms over time, providing an objective way to track and compare AI capabilities.
