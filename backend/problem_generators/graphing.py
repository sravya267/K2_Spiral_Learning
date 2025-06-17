# problem_generators/graphing.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class GraphingProblemGenerator(BaseProblemGenerator):
    """Generator for graphing and data analysis problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["pictographs"],
            INTERMEDIATE: ["pictographs", "bar_graphs"],
            ADVANCED: ["bar_graphs", "analyzing_data"]
        }
        
        # Data categories for graphs
        self.graph_categories = [
            {"name": "Favorite Fruits", "items": ["Apple", "Banana", "Orange", "Grapes", "Strawberry"]},
            {"name": "Pets", "items": ["Dog", "Cat", "Fish", "Bird", "Hamster"]},
            {"name": "Sports", "items": ["Soccer", "Basketball", "Swimming", "Running", "Baseball"]},
            {"name": "Weather", "items": ["Sunny", "Rainy", "Cloudy", "Snowy", "Windy"]},
            {"name": "Colors", "items": ["Red", "Blue", "Green", "Yellow", "Purple"]}
        ]
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a graphing problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "pictographs":
            return self._generate_pictographs_problem(difficulty)
        elif selected_subcategory == "bar_graphs":
            return self._generate_bar_graphs_problem(difficulty)
        elif selected_subcategory == "analyzing_data":
            return self._generate_analyzing_data_problem(difficulty)
        else:
            raise ValueError(f"Unsupported graphing subcategory: {selected_subcategory}")
    
    def _generate_pictographs_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem reading a pictograph"""
        # Select a category
        category = random.choice(self.graph_categories)
        
        # Generate data (simplified for pictographs)
        if difficulty == BEGINNER:
            # Use 3 items with values 1-5
            items = random.sample(category["items"], 3)
            max_value = 5
        else:  # INTERMEDIATE
            # Use 4 items with values 1-10
            items = random.sample(category["items"], 4)
            max_value = 10
        
        # Generate values for each item
        values = {item: random.randint(1, max_value) for item in items}
        
        # Generate a question
        question_type = random.choice(["read_value", "max_value", "min_value"])
        
        if question_type == "read_value":
            # Ask for the value of a specific item
            question_item = random.choice(items)
            question = f"How many {question_item.lower()}s are there?"
            answer = str(values[question_item])
            
        elif question_type == "max_value":
            # Ask for the item with the most
            max_item = max(values, key=values.get)
            question = f"Which item has the most?"
            answer = max_item
            
        else:  # min_value
            # Ask for the item with the least
            min_item = min(values, key=values.get)
            question = f"Which item has the least?"
            answer = min_item
        
        return {
            "category": category["name"],
            "items": items,
            "values": values,
            "question": question,
            "answer": answer,
            "type": "pictographs",
            "display_type": "pictograph"
        }
    
    # problem_generators/graphing.py (continued)

    def _generate_bar_graphs_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem reading a bar graph"""
        # Select a category
        category = random.choice(self.graph_categories)
        
        # Generate data
        if difficulty == INTERMEDIATE:
            # Use 4 items with values 1-15
            items = random.sample(category["items"], 4)
            max_value = 15
        else:  # ADVANCED
            # Use 5 items with values 1-50
            items = random.sample(category["items"], 5)
            max_value = 50
        
        # Generate values for each item
        values = {item: random.randint(1, max_value) for item in items}
        
        # Generate a question
        question_type = random.choice(["read_value", "max_value", "min_value", "difference", "total"])
        
        if question_type == "read_value":
            # Ask for the value of a specific item
            question_item = random.choice(items)
            question = f"How many {question_item.lower()}s are there?"
            answer = str(values[question_item])
            
        elif question_type == "max_value":
            # Ask for the item with the most
            max_item = max(values, key=values.get)
            question = f"Which item has the most?"
            answer = max_item
            
        elif question_type == "min_value":
            # Ask for the item with the least
            min_item = min(values, key=values.get)
            question = f"Which item has the least?"
            answer = min_item
            
        elif question_type == "difference":
            # Ask for the difference between two items
            item1, item2 = random.sample(items, 2)
            difference = abs(values[item1] - values[item2])
            question = f"What is the difference between {item1} and {item2}?"
            answer = str(difference)
            
        else:  # total
            # Ask for the total across all items
            total = sum(values.values())
            question = f"What is the total of all items?"
            answer = str(total)
        
        return {
            "category": category["name"],
            "items": items,
            "values": values,
            "question": question,
            "answer": answer,
            "type": "bar_graphs",
            "display_type": "bar_graph"
        }
    
    def _generate_analyzing_data_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem analyzing data from a graph"""
        # This is an advanced problem where students need to interpret data
        
        # Select a category
        category = random.choice(self.graph_categories)
        
        # Use all 5 items with values 1-50
        items = category["items"]
        max_value = 50
        
        # Generate values for each item
        values = {item: random.randint(1, max_value) for item in items}
        
        # Generate more complex analytical questions
        question_type = random.choice(["comparison", "more_than", "less_than", "average"])
        
        if question_type == "comparison":
            # Compare multiple items
            item_subset = random.sample(items, 3)
            sorted_subset = sorted(item_subset, key=lambda x: values[x], reverse=True)
            question = f"Order these from most to least: {', '.join(item_subset)}"
            answer = ", ".join(sorted_subset)
            
        elif question_type == "more_than":
            # Count items with more than a threshold
            threshold = random.randint(10, 40)
            count = sum(1 for value in values.values() if value > threshold)
            question = f"How many items have more than {threshold}?"
            answer = str(count)
            
        elif question_type == "less_than":
            # Count items with less than a threshold
            threshold = random.randint(10, 40)
            count = sum(1 for value in values.values() if value < threshold)
            question = f"How many items have less than {threshold}?"
            answer = str(count)
            
        else:  # average
            # Calculate the average
            average = sum(values.values()) / len(values)
            question = f"What is the average (mean) of all items?"
            answer = str(round(average, 1))
        
        return {
            "category": category["name"],
            "items": items,
            "values": values,
            "question": question,
            "answer": answer,
            "type": "analyzing_data",
            "display_type": "bar_graph"
        }