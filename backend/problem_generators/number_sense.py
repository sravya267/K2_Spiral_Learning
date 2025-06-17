# problem_generators/number_sense.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class NumberSenseProblemGenerator(BaseProblemGenerator):
    """Generator for number sense problems"""
    
    def __init__(self):
        super().__init__()
        
        # Single list of all available subcategories (removed subitizing)
        self.subcategories = ["comparison", "ordering", "before_after", "missing_numbers"]
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a number sense problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        selected_subcategory = self.select_subcategory(self.subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "comparison":
            return self._generate_comparison_problem(difficulty)
        elif selected_subcategory == "ordering":
            return self._generate_ordering_problem(difficulty)
        elif selected_subcategory == "before_after":
            return self._generate_before_after_problem(difficulty)
        elif selected_subcategory == "missing_numbers":
            return self._generate_missing_numbers_problem(difficulty)
        else:
            raise ValueError(f"Unsupported number sense subcategory: {selected_subcategory}")
    
    def _generate_comparison_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a number comparison problem"""
        if difficulty == BEGINNER:
            # For beginner, use 0-20 range
            num1 = random.randint(0, 20)
            num2 = random.randint(0, 20)
        elif difficulty == INTERMEDIATE:
            # For intermediate, use 10-100 range
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
        else:  # ADVANCED
            # For advanced, use 100-999 range
            num1 = random.randint(100, 999)
            num2 = random.randint(100, 999)
        
        if num1 < num2:
            comparison = "<"
        elif num1 > num2:
            comparison = ">"
        else:
            comparison = "="
        
        return {
            "first_number": num1,
            "second_number": num2,
            "answer": comparison,
            "type": "comparison",
            "display_type": "horizontal"
        }
    
    def _generate_ordering_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a number ordering problem"""
        count = 3 if difficulty == BEGINNER else (4 if difficulty == INTERMEDIATE else 5)
        
        # Generate the numbers based on difficulty
        if difficulty == BEGINNER:
            # For beginner, use 0-20 range
            numbers = [random.randint(0, 20) for _ in range(count)]
        elif difficulty == INTERMEDIATE:
            # For intermediate, use 10-100 range
            numbers = [random.randint(10, 100) for _ in range(count)]
        else:  # ADVANCED
            # For advanced, use 100-999 range
            numbers = [random.randint(100, 999) for _ in range(count)]
        
        # Find the sorted order
        ordered = sorted(numbers)
        
        return {
            "numbers": numbers,
            "answer": ", ".join(map(str, ordered)),
            "type": "ordering",
            "display_type": "list"
        }
    
    def _generate_before_after_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a before/after problem"""
        # Get number based on difficulty
        if difficulty == BEGINNER:
            # For beginner, use 1-19 range (to avoid issues at boundaries)
            num = random.randint(1, 19)
        elif difficulty == INTERMEDIATE:
            # For intermediate, use 11-99 range
            num = random.randint(11, 99)
        else:  # ADVANCED
            # For advanced, use 101-998 range
            num = random.randint(101, 998)
        
        # Choose between "before" or "after"
        question_type = random.choice(["before", "after"])
        
        answer = num - 1 if question_type == "before" else num + 1
        
        return {
            "number": num,
            "question_type": question_type,
            "answer": str(answer),
            "type": "before_after",
            "display_type": "number_line"
        }
    
    def _generate_missing_numbers_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem with a missing number in a sequence"""
        # Determine sequence parameters based on difficulty
        if difficulty == BEGINNER:
            start = random.randint(0, 10)
            step = 1
            length = 5
        elif difficulty == INTERMEDIATE:
            start = random.randint(10, 50)
            step = random.choice([2, 5, 10])
            length = 5
        else:  # ADVANCED
            start = random.randint(100, 500)
            step = random.choice([5, 10, 25, 50, 100])
            length = 6
        
        # Generate the sequence
        sequence = [start + i * step for i in range(length)]
        
        # Choose a position for the missing number
        missing_idx = random.randint(0, length - 1)
        missing_value = sequence[missing_idx]
        
        # Create a copy of the sequence with the missing value set to None
        display_sequence = sequence.copy()
        display_sequence[missing_idx] = None
        
        return {
            "sequence": display_sequence,
            "answer": str(missing_value),
            "type": "missing_numbers",
            "display_type": "sequence"
        }


