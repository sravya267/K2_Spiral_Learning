# problem_generators/skip_counting.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class SkipCountingProblemGenerator(BaseProblemGenerator):
    """Generator for skip counting problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["by_ones_twos"],
            INTERMEDIATE: ["by_ones_twos", "by_fives_tens"],
            ADVANCED: ["by_fives_tens", "by_hundreds"]
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a skip counting problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "by_ones_twos":
            return self._generate_by_ones_twos_problem()
        elif selected_subcategory == "by_fives_tens":
            return self._generate_by_fives_tens_problem()
        elif selected_subcategory == "by_hundreds":
            return self._generate_by_hundreds_problem()
        else:
            raise ValueError(f"Unsupported skip counting subcategory: {selected_subcategory}")
    
    def _generate_by_ones_twos_problem(self) -> Dict[str, Any]:
        """Generate a problem counting by ones or twos"""
        # Choose skip count value
        skip = random.choice([1, 2])
        
        # Generate sequence
        start = random.randint(1, 10)
        length = 6
        sequence = [start + i * skip for i in range(length)]
        
        # Choose position for missing number
        missing_idx = random.randint(1, length - 1)  # Don't use first position
        missing_value = sequence[missing_idx]
        
        # Create the sequence with the missing value
        display_sequence = sequence.copy()
        display_sequence[missing_idx] = None
        
        return {
            "sequence": display_sequence,
            "skip_value": skip,
            "answer": str(missing_value),
            "type": "by_ones_twos",
            "display_type": "sequence"
        }
    
    def _generate_by_fives_tens_problem(self) -> Dict[str, Any]:
        """Generate a problem counting by fives or tens"""
        # Choose skip count value
        skip = random.choice([5, 10])
        
        # Generate sequence
        start = random.randint(0, 50)
        length = 6
        sequence = [start + i * skip for i in range(length)]
        
        # Choose position for missing number
        missing_idx = random.randint(1, length - 1)  # Don't use first position
        missing_value = sequence[missing_idx]
        
        # Create the sequence with the missing value
        display_sequence = sequence.copy()
        display_sequence[missing_idx] = None
        
        return {
            "sequence": display_sequence,
            "skip_value": skip,
            "answer": str(missing_value),
            "type": "by_fives_tens",
            "display_type": "sequence"
        }
    
    def _generate_by_hundreds_problem(self) -> Dict[str, Any]:
        """Generate a problem counting by hundreds"""
        # Skip value is 100
        skip = 100
        
        # Generate sequence
        start = random.randint(0, 500)
        length = 5
        sequence = [start + i * skip for i in range(length)]
        
        # Choose position for missing number
        missing_idx = random.randint(1, length - 1)  # Don't use first position
        missing_value = sequence[missing_idx]
        
        # Create the sequence with the missing value
        display_sequence = sequence.copy()
        display_sequence[missing_idx] = None
        
        return {
            "sequence": display_sequence,
            "skip_value": skip,
            "answer": str(missing_value),
            "type": "by_hundreds",
            "display_type": "sequence"
        }