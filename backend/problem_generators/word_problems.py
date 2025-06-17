# problem_generators/word_problems.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class WordProblemGenerator(BaseProblemGenerator):
    """Generator for word problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["one_step"],
            INTERMEDIATE: ["one_step", "two_step"],
            ADVANCED: ["two_step", "multi_step"]
        }
        
        # Common objects for word problems
        self.objects = [
            "apples", "oranges", "toys", "books", "pencils", 
            "stickers", "marbles", "balloons", "cookies", "flowers"
        ]
        
        # Common names for word problems
        self.names = [
            "Sam", "Alex", "Jordan", "Taylor", "Casey", 
            "Riley", "Morgan", "Avery", "Jamie", "Quinn"
        ]
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a word problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "one_step":
            return self._generate_one_step_problem(difficulty)
        elif selected_subcategory == "two_step":
            return self._generate_two_step_problem(difficulty)
        elif selected_subcategory == "multi_step":
            return self._generate_multi_step_problem(difficulty)
        else:
            raise ValueError(f"Unsupported word problem subcategory: {selected_subcategory}")
    
    def _generate_one_step_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a one-step word problem"""
        # Choose operation (addition or subtraction)
        operation = random.choice(["addition", "subtraction"])
        
        # Choose objects and names
        object_type = random.choice(self.objects)
        name1 = random.choice(self.names)
        name2 = random.choice([n for n in self.names if n != name1])
        
        # Generate numbers based on difficulty
        if difficulty == BEGINNER:
            # For beginner, keep numbers under 10
            if operation == "addition":
                num1 = random.randint(1, 5)
                num2 = random.randint(1, 9 - num1)  # Ensure sum < 10
                answer = num1 + num2
                
                text = f"{name1} has {num1} {object_type}. {name2} gives {name1} {num2} more {object_type}. How many {object_type} does {name1} have now?"
            else:  # subtraction
                total = random.randint(5, 9)
                num_taken = random.randint(1, total - 1)  # Ensure result is positive
                answer = total - num_taken
                
                text = f"{name1} has {total} {object_type}. {name1} gives {num_taken} {object_type} to {name2}. How many {object_type} does {name1} have left?"
        
        elif difficulty == INTERMEDIATE:
            # For intermediate, use double-digit numbers
            if operation == "addition":
                num1 = random.randint(10, 50)
                num2 = random.randint(10, 40)
                answer = num1 + num2
                
                text = f"{name1} has {num1} {object_type}. {name2} gives {name1} {num2} more {object_type}. How many {object_type} does {name1} have now?"
            else:  # subtraction
                total = random.randint(30, 90)
                num_taken = random.randint(10, total - 10)  # Ensure result is positive
                answer = total - num_taken
                
                text = f"{name1} has {total} {object_type}. {name1} gives {num_taken} {object_type} to {name2}. How many {object_type} does {name1} have left?"
        
        else:  # ADVANCED
            # For advanced, use triple-digit numbers
            if operation == "addition":
                num1 = random.randint(100, 500)
                num2 = random.randint(100, 400)
                answer = num1 + num2
                
                text = f"{name1} has {num1} {object_type}. {name2} gives {name1} {num2} more {object_type}. How many {object_type} does {name1} have now?"
            else:  # subtraction
                total = random.randint(300, 900)
                num_taken = random.randint(100, total - 100)  # Ensure result is positive
                answer = total - num_taken
                
                text = f"{name1} has {total} {object_type}. {name1} gives {num_taken} {object_type} to {name2}. How many {object_type} does {name1} have left?"
        
        return {
            "text": text,
            "answer": str(answer),
            "type": "one_step",
            "display_type": "text"
        }
    
    def _generate_two_step_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a two-step word problem"""
        # Choose operation pairs
        operation_pair = random.choice([
            ("addition", "addition"),
            ("addition", "subtraction"),
            ("subtraction", "addition")
        ])
        
        # Choose objects and names
        object_type = random.choice(self.objects)
        name1 = random.choice(self.names)
        name2 = random.choice([n for n in self.names if n != name1])
        name3 = random.choice([n for n in self.names if n != name1 and n != name2])
        
        # Generate numbers based on difficulty
        if difficulty == INTERMEDIATE:
            # For intermediate, use double-digit numbers
            if operation_pair == ("addition", "addition"):
                num1 = random.randint(10, 30)
                num2 = random.randint(10, 30)
                num3 = random.randint(10, 30)
                answer = num1 + num2 + num3
                
                text = f"{name1} has {num1} {object_type}. {name2} gives {name1} {num2} more {object_type}. Then {name3} gives {name1} {num3} more {object_type}. How many {object_type} does {name1} have now?"
                
            elif operation_pair == ("addition", "subtraction"):
                num1 = random.randint(10, 30)
                num2 = random.randint(10, 30)
                num3 = random.randint(5, 20)
                answer = num1 + num2 - num3
                
                text = f"{name1} has {num1} {object_type}. {name2} gives {name1} {num2} more {object_type}. Then {name1} gives {num3} {object_type} to {name3}. How many {object_type} does {name1} have now?"
                
            else:  # ("subtraction", "addition")
                num1 = random.randint(30, 50)
                num2 = random.randint(5, 20)
                num3 = random.randint(10, 30)
                answer = num1 - num2 + num3
                
                text = f"{name1} has {num1} {object_type}. {name1} gives {num2} {object_type} to {name2}. Then {name3} gives {name1} {num3} more {object_type}. How many {object_type} does {name1} have now?"
        
        else:  # ADVANCED
            # For advanced, use triple-digit numbers
            if operation_pair == ("addition", "addition"):
                num1 = random.randint(100, 300)
                num2 = random.randint(100, 300)
                num3 = random.randint(100, 300)
                answer = num1 + num2 + num3
                
                text = f"{name1} has {num1} {object_type}. {name2} gives {name1} {num2} more {object_type}. Then {name3} gives {name1} {num3} more {object_type}. How many {object_type} does {name1} have now?"
                
            elif operation_pair == ("addition", "subtraction"):
                num1 = random.randint(100, 300)
                num2 = random.randint(100, 300)
                num3 = random.randint(50, 200)
                answer = num1 + num2 - num3
                
                text = f"{name1} has {num1} {object_type}. {name2} gives {name1} {num2} more {object_type}. Then {name1} gives {num3} {object_type} to {name3}. How many {object_type} does {name1} have now?"
                
            else:  # ("subtraction", "addition")
                num1 = random.randint(300, 500)
                num2 = random.randint(50, 200)
                num3 = random.randint(100, 300)
                answer = num1 - num2 + num3
                
                text = f"{name1} has {num1} {object_type}. {name1} gives {num2} {object_type} to {name2}. Then {name3} gives {name1} {num3} more {object_type}. How many {object_type} does {name1} have now?"
        
        return {
            "text": text,
            "answer": str(answer),
            "type": "two_step",
            "display_type": "text"
        }
    
    def _generate_multi_step_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a multi-step word problem (3+ steps)"""
        # For multi-step problems, we'll use triple-digit numbers
        
        # Choose objects and names
        object_type = random.choice(self.objects)
        name1 = random.choice(self.names)
        name2 = random.choice([n for n in self.names if n != name1])
        name3 = random.choice([n for n in self.names if n != name1 and n != name2])
        name4 = random.choice([n for n in self.names if n != name1 and n != name2 and n != name3])
        
        # Generate a three-step problem with mixed operations
        num1 = random.randint(100, 300)
        num2 = random.randint(50, 150)
        num3 = random.randint(20, 80)
        num4 = random.randint(10, 50)
        
        # Ensure all steps yield positive results
        if num1 - num2 < num3:
            num3 = random.randint(10, num1 - num2 - 10)
        
        answer = num1 - num2 + num3 - num4
        
        text = (
            f"{name1} starts with {num1} {object_type}. "
            f"{name1} gives {num2} {object_type} to {name2}. "
            f"Then {name3} gives {name1} {num3} more {object_type}. "
            f"Finally, {name1} gives {num4} {object_type} to {name4}. "
            f"How many {object_type} does {name1} have now?"
        )
        
        return {
            "text": text,
            "answer": str(answer),
            "type": "multi_step",
            "display_type": "text"
        }