# problem_generators/odd_even.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class OddEvenProblemGenerator(BaseProblemGenerator):
    """Generator for odd and even number problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["identifying"],
            INTERMEDIATE: ["identifying", "sorting"],
            ADVANCED: ["sorting", "problem_solving"]
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate an odd/even problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "identifying":
            return self._generate_identifying_problem(difficulty)
        elif selected_subcategory == "sorting":
            return self._generate_sorting_problem(difficulty)
        elif selected_subcategory == "problem_solving":
            return self._generate_problem_solving_problem(difficulty)
        else:
            raise ValueError(f"Unsupported odd/even subcategory: {selected_subcategory}")
    
    def _generate_identifying_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem identifying odd or even numbers"""
        # Generate a number based on difficulty
        if difficulty == BEGINNER:
            number = random.randint(1, 20)
        else:  # INTERMEDIATE
            number = random.randint(11, 99)
        
        # Determine if it's odd or even
        is_even = (number % 2 == 0)
        
        # Create the question
        question = f"Is {number} odd or even?"
        answer = "even" if is_even else "odd"
        
        return {
            "number": number,
            "is_even": is_even,
            "question": question,
            "answer": answer,
            "type": "identifying",
            "display_type": "text"
        }
    
    def _generate_sorting_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem sorting numbers into odd and even"""
        # Generate a set of numbers based on difficulty
        if difficulty == INTERMEDIATE:
            # 5-8 numbers between 1-50
            count = random.randint(5, 8)
            max_value = 50
        else:  # ADVANCED
            # 6-10 numbers between 1-100
            count = random.randint(6, 10)
            max_value = 100
        
        # Generate the numbers
        numbers = [random.randint(1, max_value) for _ in range(count)]
        
        # Sort into odd and even
        odd_numbers = [num for num in numbers if num % 2 != 0]
        even_numbers = [num for num in numbers if num % 2 == 0]
        
        # Create the question
        question = f"Sort these numbers into odd and even: {', '.join(map(str, numbers))}"
        answer = f"Odd: {', '.join(map(str, odd_numbers))}; Even: {', '.join(map(str, even_numbers))}"
        
        return {
            "numbers": numbers,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "question": question,
            "answer": answer,
            "type": "sorting",
            "display_type": "text"
        }
    
    def _generate_problem_solving_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem solving with odd and even numbers"""
        # Create a more complex problem using odd/even properties
        problem_type = random.choice(["next_even", "next_odd", "sum_property", "product_property"])
        
        if problem_type == "next_even":
            # Find the next even number
            start = random.randint(50, 998)
            # Make sure start is odd so next even is simple
            if start % 2 == 0:
                start += 1
            
            question = f"What is the next even number after {start}?"
            answer = str(start + 1)
        
        elif problem_type == "next_odd":
            # Find the next odd number
            start = random.randint(50, 998)
            # Make sure start is even so next odd is simple
            if start % 2 != 0:
                start += 1
            
            question = f"What is the next odd number after {start}?"
            answer = str(start + 1)
        
        elif problem_type == "sum_property":
            # Determine if a sum will be odd or even
            num1 = random.randint(50, 999)
            num2 = random.randint(50, 999)
            
            is_num1_even = (num1 % 2 == 0)
            is_num2_even = (num2 % 2 == 0)
            
            # Determine the parity of the sum
            if (is_num1_even and is_num2_even) or (not is_num1_even and not is_num2_even):
                sum_parity = "even"
            else:
                sum_parity = "odd"
            
            question = f"Will the sum of {num1} and {num2} be odd or even?"
            answer = sum_parity
        
        else:  # product_property
            # Determine if a product will be odd or even
            num1 = random.randint(50, 999)
            num2 = random.randint(50, 999)
            
            is_num1_even = (num1 % 2 == 0)
            is_num2_even = (num2 % 2 == 0)
            
            # If either number is even, the product is even
            product_parity = "even" if (is_num1_even or is_num2_even) else "odd"
            
            question = f"Will the product of {num1} and {num2} be odd or even?"
            answer = product_parity
        
        return {
            "question": question,
            "answer": answer,
            "type": "problem_solving",
            "display_type": "text"
        }