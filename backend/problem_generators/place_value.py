# problem_generators/place_value.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class PlaceValueProblemGenerator(BaseProblemGenerator):
    """Generator for place value problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["ones_tens"],
            INTERMEDIATE: ["ones_tens", "ones_tens_hundreds"],
            ADVANCED: ["ones_tens_hundreds", "expanded_form"]
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a place value problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "ones_tens":
            return self._generate_ones_tens_problem()
        elif selected_subcategory == "ones_tens_hundreds":
            return self._generate_ones_tens_hundreds_problem()
        elif selected_subcategory == "expanded_form":
            return self._generate_expanded_form_problem()
        else:
            raise ValueError(f"Unsupported place value subcategory: {selected_subcategory}")
    
    def _generate_ones_tens_problem(self) -> Dict[str, Any]:
        """Generate a problem identifying ones and tens places"""
        # Generate a 2-digit number
        num = random.randint(10, 99)
        
        # Extract digits
        tens = num // 10
        ones = num % 10
        
        # Randomly choose to ask for ones or tens digit
        place = random.choice(["ones", "tens"])
        
        if place == "ones":
            answer = str(ones)
        else:  # tens
            answer = str(tens)
        
        return {
            "number": num,
            "place": place,
            "answer": answer,
            "type": "ones_tens",
            "display_type": "place_value_blocks"
        }
    
    def _generate_ones_tens_hundreds_problem(self) -> Dict[str, Any]:
        """Generate a problem identifying ones, tens, and hundreds places"""
        # Generate a 3-digit number
        num = random.randint(100, 999)
        
        # Extract digits
        hundreds = num // 100
        tens = (num % 100) // 10
        ones = num % 10
        
        # Randomly choose to ask for ones, tens, or hundreds digit
        place = random.choice(["ones", "tens", "hundreds"])
        
        if place == "ones":
            answer = str(ones)
        elif place == "tens":
            answer = str(tens)
        else:  # hundreds
            answer = str(hundreds)
        
        return {
            "number": num,
            "place": place,
            "answer": answer,
            "type": "ones_tens_hundreds",
            "display_type": "place_value_blocks"
        }
    
    def _generate_expanded_form_problem(self) -> Dict[str, Any]:
        """Generate a problem converting between standard and expanded form"""
        # Generate a 3-digit number
        num = random.randint(100, 999)
        
        # Extract digits
        hundreds = num // 100
        tens = (num % 100) // 10
        ones = num % 10
        
        # Create expanded form
        expanded_form = f"{hundreds} hundreds + {tens} tens + {ones} ones"
        
        # Randomly choose between standard → expanded or expanded → standard
        direction = random.choice(["to_expanded", "to_standard"])
        
        if direction == "to_expanded":
            question = f"Write {num} in expanded form"
            answer = expanded_form
        else:  # to_standard
            question = f"Write this number in standard form: {expanded_form}"
            answer = str(num)
        
        return {
            "number": num,
            "expanded_form": expanded_form,
            "question": question,
            "answer": answer,
            "type": "expanded_form",
            "display_type": "text"
        }