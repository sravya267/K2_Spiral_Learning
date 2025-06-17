# problem_generators/fractions.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class FractionsProblemGenerator(BaseProblemGenerator):
    """Generator for fraction problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["halves_wholes"],
            INTERMEDIATE: ["halves_wholes", "thirds_fourths"],
            ADVANCED: ["thirds_fourths", "comparing_fractions"]
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a fraction problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "halves_wholes":
            return self._generate_halves_wholes_problem()
        elif selected_subcategory == "thirds_fourths":
            return self._generate_thirds_fourths_problem()
        elif selected_subcategory == "comparing_fractions":
            return self._generate_comparing_fractions_problem()
        else:
            raise ValueError(f"Unsupported fractions subcategory: {selected_subcategory}")
    
    def _generate_halves_wholes_problem(self) -> Dict[str, Any]:
        """Generate a problem identifying halves and wholes"""
        # Choose shape type
        shape = random.choice(["circle", "rectangle", "square"])
        
        # Choose fraction (1/2 or 1)
        fraction_type = random.choice(["half", "whole"])
        
        if fraction_type == "half":
            fraction = "1/2"
            shaded = 1
            total = 2
        else:  # whole
            fraction = "1"
            shaded = 1
            total = 1
        
        return {
            "shape": shape,
            "fraction": fraction,
            "shaded_parts": shaded,
            "total_parts": total,
            "answer": fraction,
            "type": "halves_wholes",
            "display_type": "fraction"
        }
    
    def _generate_thirds_fourths_problem(self) -> Dict[str, Any]:
        """Generate a problem identifying thirds and fourths"""
        # Choose shape type
        shape = random.choice(["circle", "square"])
        
        # Choose fraction type (1/3, 2/3, 1/4, 2/4 (1/2), 3/4)
        if random.choice([True, False]):
            # Thirds
            denominator = 3
            numerator = random.randint(1, 2)
        else:
            # Fourths
            denominator = 4
            numerator = random.randint(1, 3)
        
        fraction = f"{numerator}/{denominator}"
        
        return {
            "shape": shape,
            "fraction": fraction,
            "shaded_parts": numerator,
            "total_parts": denominator,
            "answer": fraction,
            "type": "thirds_fourths",
            "display_type": "fraction"
        }
    
    def _generate_comparing_fractions_problem(self) -> Dict[str, Any]:
        """Generate a problem comparing fractions"""
        # Choose two fractions to compare
        
        # For easier comparison, use one of these patterns:
        # 1. Same denominator, different numerator (e.g., 2/5 vs 3/5)
        # 2. Same numerator, different denominator (e.g., 1/2 vs 1/4)
        # 3. One is clearly a unit fraction and one is not (e.g., 1/3 vs 2/3)
        
        pattern = random.choice([1, 2, 3])
        
        if pattern == 1:
            # Same denominator, different numerator
            denominator = random.choice([2, 3, 4, 5, 6, 8, 10])
            numerator1 = random.randint(1, denominator - 1)
            numerator2 = random.choice([n for n in range(1, denominator) if n != numerator1])
            
            fraction1 = f"{numerator1}/{denominator}"
            fraction2 = f"{numerator2}/{denominator}"
            
        elif pattern == 2:
            # Same numerator, different denominator
            numerator = random.randint(1, 3)
            denominator1 = random.choice([2, 3, 4, 5, 6])
            denominator2 = random.choice([d for d in [2, 3, 4, 5, 6] if d != denominator1])
            
            fraction1 = f"{numerator}/{denominator1}"
            fraction2 = f"{numerator}/{denominator2}"
            
        else:  # pattern == 3
            # Unit fraction vs non-unit fraction
            denominator = random.choice([2, 3, 4, 5, 6])
            
            if random.choice([True, False]):
                fraction1 = f"1/{denominator}"
                fraction2 = f"{random.randint(2, denominator-1)}/{denominator}"
            else:
                fraction1 = f"{random.randint(2, denominator-1)}/{denominator}"
                fraction2 = f"1/{denominator}"
        
        # Determine the answer
        def fraction_value(frac_str):
            parts = frac_str.split('/')
            return int(parts[0]) / int(parts[1])
        
        value1 = fraction_value(fraction1)
        value2 = fraction_value(fraction2)
        
        if value1 < value2:
            answer = "<"
        elif value1 > value2:
            answer = ">"
        else:
            answer = "="
        
        return {
            "fraction1": fraction1,
            "fraction2": fraction2,
            "answer": answer,
            "type": "comparing_fractions",
            "display_type": "comparison"
        }