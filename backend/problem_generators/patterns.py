# problem_generators/patterns.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class PatternsProblemGenerator(BaseProblemGenerator):
    """Generator for pattern problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["abab_patterns"],
            INTERMEDIATE: ["abab_patterns", "extending_patterns"],
            ADVANCED: ["extending_patterns", "creating_patterns"]
        }
        
        # Pattern elements
        self.pattern_elements = {
            "shapes": ["circle", "square", "triangle", "star", "heart"],
            "colors": ["red", "blue", "green", "yellow", "purple"],
            "letters": ["A", "B", "C", "D", "E"],
            "numbers": ["1", "2", "3", "4", "5"]
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a pattern problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "abab_patterns":
            return self._generate_abab_patterns_problem(difficulty)
        elif selected_subcategory == "extending_patterns":
            return self._generate_extending_patterns_problem(difficulty)
        elif selected_subcategory == "creating_patterns":
            return self._generate_creating_patterns_problem(difficulty)
        else:
            raise ValueError(f"Unsupported patterns subcategory: {selected_subcategory}")
    
    def _generate_abab_patterns_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem with ABAB type patterns"""
        # Choose pattern type
        element_type = random.choice(list(self.pattern_elements.keys()))
        elements = self.pattern_elements[element_type]
        
        # Generate a pattern
        if difficulty == BEGINNER:
            # Simple AB pattern
            pattern_elements = [elements[0], elements[1]]
            pattern_length = 6
        else:
            # ABC or AABB pattern
            pattern_type = random.choice(["ABC", "AABB"])
            
            if pattern_type == "ABC":
                pattern_elements = [elements[0], elements[1], elements[2]]
                pattern_length = 6
            else:  # AABB
                pattern_elements = [elements[0], elements[0], elements[1], elements[1]]
                pattern_length = 8
        
        # Generate the full pattern
        pattern = []
        for i in range(pattern_length):
            pattern.append(pattern_elements[i % len(pattern_elements)])
        
        # For the question, remove the last element
        question_pattern = pattern[:-1]
        answer = pattern[-1]
        
        return {
            "pattern": question_pattern,
            "element_type": element_type,
            "answer": answer,
            "type": "abab_patterns",
            "display_type": "pattern"
        }
    
    def _generate_extending_patterns_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem extending numeric patterns"""
        # For number patterns, create arithmetic sequences
        
        if difficulty == INTERMEDIATE:
            # Simple arithmetic sequence (add/subtract constant)
            start = random.randint(1, 20)
            step = random.choice([1, 2, 5, 10])
            operation = random.choice(["+", "-"])
            length = 5
        else:  # ADVANCED
            # More complex sequences
            start = random.randint(1, 50)
            step = random.choice([2, 3, 5, 10, 25])
            operation = random.choice(["+", "-", "*"])
            length = 5
        
        # Generate the pattern
        pattern = [start]
        for i in range(1, length):
            if operation == "+":
                pattern.append(pattern[i-1] + step)
            elif operation == "-":
                pattern.append(pattern[i-1] - step)
            else:  # "*"
                pattern.append(pattern[i-1] * step)
        
        # The answer is the next element
        if operation == "+":
            answer = pattern[-1] + step
        elif operation == "-":
            answer = pattern[-1] - step
        else:  # "*"
            answer = pattern[-1] * step
        
        return {
            "pattern": pattern,
            "operation": operation,
            "step": step,
            "answer": str(answer),
            "type": "extending_patterns",
            "display_type": "number_pattern"
        }
    
    def _generate_creating_patterns_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem with a pattern that has multiple missing elements"""
        # For advanced pattern creation, we'll use arithmetic sequences with multiple gaps
        
        # Generate pattern parameters
        start = random.randint(1, 50)
        step = random.choice([2, 3, 5, 10])
        operation = random.choice(["+", "-"])
        length = 8
        
        # Generate the complete pattern
        complete_pattern = [start]
        for i in range(1, length):
            if operation == "+":
                complete_pattern.append(complete_pattern[i-1] + step)
            else:  # "-"
                complete_pattern.append(complete_pattern[i-1] - step)
        
        # Create gaps in the pattern (2-3 gaps)
        pattern_with_gaps = complete_pattern.copy()
        num_gaps = random.randint(2, 3)
        gap_positions = random.sample(range(1, length), num_gaps)  # Don't remove the first element
        
        missing_values = []
        for pos in sorted(gap_positions):
            missing_values.append(pattern_with_gaps[pos])
            pattern_with_gaps[pos] = None
        
        return {
            "pattern": pattern_with_gaps,
            "operation": operation,
            "step": step,
            "missing_values": missing_values,
            "answer": ", ".join(map(str, missing_values)),
            "type": "creating_patterns",
            "display_type": "number_pattern_gaps"
        }