# problem_generators/measurement.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class MeasurementProblemGenerator(BaseProblemGenerator):
    """Generator for measurement problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["comparing_objects"],
            INTERMEDIATE: ["comparing_objects", "non_standard_units"],
            ADVANCED: ["non_standard_units", "rulers_inches_cm"]
        }
        
        # Objects for comparison problems
        self.comparison_objects = [
            {"name": "pencil", "property": "length", "comparisons": ["eraser", "book", "ruler"]},
            {"name": "tree", "property": "height", "comparisons": ["flower", "bush", "house"]},
            {"name": "elephant", "property": "size", "comparisons": ["dog", "cat", "mouse"]},
            {"name": "book", "property": "weight", "comparisons": ["paper", "backpack", "desk"]}
        ]
        
        # Non-standard measuring units
        self.measuring_objects = ["paperclip", "crayon", "pencil", "hand", "foot", "block"]
        
        # Items to measure
        self.items_to_measure = ["book", "desk", "door", "window", "whiteboard", "notebook", "tablet"]
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a measurement problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "comparing_objects":
            return self._generate_comparing_objects_problem()
        elif selected_subcategory == "non_standard_units":
            return self._generate_non_standard_units_problem()
        elif selected_subcategory == "rulers_inches_cm":
            return self._generate_rulers_inches_cm_problem()
        else:
            raise ValueError(f"Unsupported measurement subcategory: {selected_subcategory}")
    
    def _generate_comparing_objects_problem(self) -> Dict[str, Any]:
        """Generate a problem comparing objects by size/length/height"""
        # Select a primary object
        obj = random.choice(self.comparison_objects)
        
        # Select a comparison object
        comparison_obj = random.choice(obj["comparisons"])
        
        # Determine the property to compare
        property_name = obj["property"]
        
        # Randomly determine which is bigger/longer/taller
        if random.choice([True, False]):
            # Primary object is bigger
            answer = f"{obj['name']} is {property_name}er"
            question_type = "comparison"
        else:
            # Comparison object is bigger
            answer = f"{comparison_obj} is {property_name}er"
            question_type = "comparison"
        
        return {
            "object1": obj["name"],
            "object2": comparison_obj,
            "property": property_name,
            "question_type": question_type,
            "answer": answer,
            "type": "comparing_objects",
            "display_type": "comparison"
        }
    
    def _generate_non_standard_units_problem(self) -> Dict[str, Any]:
        """Generate a problem measuring with non-standard units"""
        # Select a measuring object
        measuring_object = random.choice(self.measuring_objects)
        
        # Select an item to measure
        item = random.choice(self.items_to_measure)
        
        # Generate a plausible measurement
        if measuring_object in ["paperclip", "crayon", "block"]:
            # Smaller measuring objects need more units
            measurement = random.randint(5, 15)
        else:
            # Larger measuring objects need fewer units
            measurement = random.randint(2, 8)
        
        return {
            "measuring_object": measuring_object,
            "item_to_measure": item,
            "measurement": measurement,
            "answer": str(measurement),
            "type": "non_standard_units",
            "display_type": "measurement"
        }
    
    def _generate_rulers_inches_cm_problem(self) -> Dict[str, Any]:
        """Generate a problem measuring with rulers (inches or cm)"""
        # Choose unit (inches or cm)
        unit = random.choice(["inches", "centimeters"])
        
        # Generate a measurement
        if unit == "inches":
            # Generate a measurement in inches (1 to 12 inches)
            whole_part = random.randint(1, 11)
            fraction_part = random.choice([0, 0.25, 0.5, 0.75])
            measurement = whole_part + fraction_part
            
            if fraction_part == 0:
                answer = f"{whole_part} inches"
            else:
                # Format fractions as strings (1/4, 1/2, 3/4)
                fraction_str = {0.25: "1/4", 0.5: "1/2", 0.75: "3/4"}[fraction_part]
                answer = f"{whole_part} {fraction_str} inches"
                
        else:  # cm
            # Generate a measurement in cm (1 to 30 cm)
            measurement = random.randint(1, 30)
            answer = f"{measurement} centimeters"
        
        return {
            "unit": unit,
            "measurement": measurement,
            "answer": answer,
            "type": "rulers_inches_cm",
            "display_type": "ruler"
        }