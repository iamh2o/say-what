"""Standard benchmark with diverse questions to test AI capabilities."""

from typing import List
from .base import Benchmark, Question


class StandardBenchmark(Benchmark):
    """Standard benchmark suite with questions across multiple domains."""
    
    def get_name(self) -> str:
        """Return the name of this benchmark."""
        return "Standard Intelligence Benchmark"
    
    def get_version(self) -> str:
        """Return the version of this benchmark."""
        return "1.0"
    
    def get_questions(self) -> List[Question]:
        """Return the list of questions in this benchmark."""
        return [
            # Reasoning and Logic
            Question(
                question_id="logic_001",
                prompt="If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
                category="logic",
                expected_elements=["cannot conclude", "some flowers", "not all flowers", "logical fallacy"]
            ),
            Question(
                question_id="reasoning_001",
                prompt="A farmer has 17 sheep, and all but 9 die. How many sheep are left?",
                category="reasoning",
                expected_elements=["9", "nine", "all but 9"]
            ),
            
            # Mathematics
            Question(
                question_id="math_001",
                prompt="What is the next number in this sequence: 2, 6, 12, 20, 30, ?",
                category="math",
                expected_elements=["42", "n(n+1)", "triangular"]
            ),
            Question(
                question_id="math_002",
                prompt="If a clock shows 3:15, what is the angle between the hour and minute hands?",
                category="math",
                expected_elements=["7.5", "degrees", "7 1/2"]
            ),
            
            # Language and Understanding
            Question(
                question_id="language_001",
                prompt="What is the difference in meaning between 'I didn't say he stole the money' with emphasis on different words?",
                category="language",
                expected_elements=["emphasis", "different meanings", "stress", "implication"]
            ),
            Question(
                question_id="language_002",
                prompt="Correct this sentence: 'The data is being analyzed by the team and they is finding interesting patterns.'",
                category="language",
                expected_elements=["they are", "subject-verb agreement", "are finding"]
            ),
            
            # Common Knowledge
            Question(
                question_id="knowledge_001",
                prompt="What is the capital of Australia?",
                category="knowledge",
                expected_elements=["Canberra"]
            ),
            Question(
                question_id="knowledge_002",
                prompt="Who wrote the novel '1984'?",
                category="knowledge",
                expected_elements=["George Orwell", "Orwell"]
            ),
            
            # Problem Solving
            Question(
                question_id="problem_001",
                prompt="You have a 3-gallon jug and a 5-gallon jug. How can you measure exactly 4 gallons?",
                category="problem_solving",
                expected_elements=["fill", "pour", "3-gallon", "5-gallon", "steps"]
            ),
            
            # Coding/Algorithm Understanding
            Question(
                question_id="coding_001",
                prompt="What is the time complexity of binary search on a sorted array of n elements?",
                category="coding",
                expected_elements=["O(log n)", "logarithmic", "log n"]
            ),
            
            # Creative Thinking
            Question(
                question_id="creative_001",
                prompt="Provide three creative uses for a paperclip besides holding papers together.",
                category="creative",
                expected_elements=["three", "uses", "creative", "different"]
            ),
            
            # Analytical Thinking
            Question(
                question_id="analytical_001",
                prompt="If you could save 1000 people by sacrificing 1 innocent person, should you do it? Explain your reasoning.",
                category="analytical",
                expected_elements=["ethics", "utilitarian", "deontological", "reasoning", "considerations"]
            ),
        ]
