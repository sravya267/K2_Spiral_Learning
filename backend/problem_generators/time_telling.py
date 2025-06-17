# problem_generators/time_telling.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class TimeTellingProblemGenerator(BaseProblemGenerator):
    """Generator for time telling problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["whole_hours"],
            INTERMEDIATE: ["whole_hours", "half_hours"],
            ADVANCED: ["whole_hours", "half_hours", "quarter_hours", "five_minute_increments"]
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a time telling problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "whole_hours":
            return self._generate_whole_hours_problem()
        elif selected_subcategory == "half_hours":
            return self._generate_half_hours_problem()
        elif selected_subcategory == "quarter_hours":
            return self._generate_quarter_hours_problem()
        elif selected_subcategory == "five_minute_increments":
            return self._generate_five_minute_increments_problem()
        else:
            raise ValueError(f"Unsupported time telling subcategory: {selected_subcategory}")
    
    def _generate_whole_hours_problem(self) -> Dict[str, Any]:
        """Generate a problem telling time to the whole hour"""
        hour = random.randint(1, 12)
        minute = 0
        
        time_str = f"{hour}:00"
        
        return {
            "hour": hour,
            "minute": minute,
            "answer": time_str,
            "type": "whole_hours",
            "display_type": "clock"
        }
    
    def _generate_half_hours_problem(self) -> Dict[str, Any]:
        """Generate a problem telling time to the half hour"""
        hour = random.randint(1, 12)
        minute = 30
        
        time_str = f"{hour}:30"
        
        return {
            "hour": hour,
            "minute": minute,
            "answer": time_str,
            "type": "half_hours",
            "display_type": "clock"
        }
    
    def _generate_quarter_hours_problem(self) -> Dict[str, Any]:
        """Generate a problem telling time to quarter hours"""
        hour = random.randint(1, 12)
        minute = random.choice([15, 45])
        
        time_str = f"{hour}:{minute}"
        
        return {
            "hour": hour,
            "minute": minute,
            "answer": time_str,
            "type": "quarter_hours",
            "display_type": "clock"
        }
    
    def _generate_five_minute_increments_problem(self) -> Dict[str, Any]:
        """Generate a problem telling time to 5-minute increments"""
        hour = random.randint(1, 12)
        minute = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        
        time_str = f"{hour}:{minute:02d}"
        
        return {
            "hour": hour,
            "minute": minute,
            "answer": time_str,
            "type": "five_minute_increments",
            "display_type": "clock"
        }