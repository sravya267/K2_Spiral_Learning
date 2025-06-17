# problem_generators/subtraction.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class SubtractionProblemGenerator(BaseProblemGenerator):
    """Generator for subtraction problems"""
    
    def __init__(self):
        super().__init__()
        
        # Single list of all available subcategories (including the new random numbers category)
        self.subcategories = ["subtract_zero", "subtract_one", "same_number_subtraction", "near_doubles_subtraction", "subtract_random_numbers"]
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a subtraction problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        selected_subcategory = self.select_subcategory(self.subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "subtract_zero":
            return self._generate_subtract_zero_problem(difficulty)
        elif selected_subcategory == "subtract_one":
            return self._generate_subtract_one_problem(difficulty)
        elif selected_subcategory == "same_number_subtraction":
            return self._generate_same_number_problem(difficulty)
        elif selected_subcategory == "near_doubles_subtraction":
            return self._generate_near_doubles_problem(difficulty)
        elif selected_subcategory == "subtract_random_numbers":
            return self._generate_random_numbers_problem(difficulty)
        else:
            raise ValueError(f"Unsupported subtraction subcategory: {selected_subcategory}")
    
    def _generate_subtract_zero_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a subtraction problem where the second number is zero"""
        num = self.generate_random_number(difficulty)
        
        return {
            "first_number": num,
            "second_number": 0,
            "answer": str(num),
            "type": "subtraction",
            "display_type": "vertical"
        }
    
    def _generate_subtract_one_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a subtraction problem where the second number is one"""
        # Ensure num > 1 so the result is positive
        min_val, max_val = self.number_ranges[difficulty]
        num = random.randint(max(min_val + 1, 2), max_val)
        
        return {
            "first_number": num,
            "second_number": 1,
            "answer": str(num - 1),
            "type": "subtraction",
            "display_type": "vertical"
        }
    
    def _generate_same_number_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a subtraction problem where both numbers are the same"""
        num = self.generate_random_number(difficulty)
        
        return {
            "first_number": num,
            "second_number": num,
            "answer": "0",
            "type": "subtraction",
            "display_type": "vertical"
        }
    
    def _generate_near_doubles_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a near-doubles subtraction problem (a - (a-1))"""
        if difficulty == BEGINNER:
            base = random.randint(2, 9)
        elif difficulty == INTERMEDIATE:
            base = random.randint(10, 99)
        else:  # ADVANCED
            base = random.randint(10, 999)
        
        num1 = base
        num2 = base - 1
        
        return {
            "first_number": num1,
            "second_number": num2,
            "answer": "1",
            "type": "subtraction",
            "display_type": "vertical"
        }
    
    def _generate_random_numbers_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a subtraction problem with two random numbers within the difficulty range,
        ensuring the result is a positive number"""
        if difficulty == BEGINNER:
            # For beginner, use numbers 0-20
            num1 = random.randint(1, 20)
            # Ensure num2 is less than or equal to num1
            num2 = random.randint(0, num1)
        elif difficulty == INTERMEDIATE:
            # For intermediate, use numbers 10-100
            num1 = random.randint(10, 100)
            # Ensure num2 is less than or equal to num1
            num2 = random.randint(0, num1)
        else:  # ADVANCED
            # For advanced, use numbers 100-999
            num1 = random.randint(100, 999)
            # Ensure num2 is less than or equal to num1
            num2 = random.randint(0, num1)
        
        return {
            "first_number": num1,
            "second_number": num2,
            "answer": str(num1 - num2),
            "type": "subtraction",
            "display_type": "vertical"
        }