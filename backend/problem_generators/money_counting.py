# problem_generators/money_counting.py

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED

class MoneyCountingProblemGenerator(BaseProblemGenerator):
    """Generator for money counting problems"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["identifying_coins", "counting_pennies_nickels"],
            INTERMEDIATE: ["counting_pennies_nickels", "mixed_coins"],
            ADVANCED: ["mixed_coins", "making_change"]
        }
        
        # Coin values in cents
        self.coin_values = {
            "penny": 1,
            "nickel": 5,
            "dime": 10,
            "quarter": 25
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate a money counting problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "identifying_coins":
            return self._generate_identifying_coins_problem()
        elif selected_subcategory == "counting_pennies_nickels":
            return self._generate_counting_pennies_nickels_problem()
        elif selected_subcategory == "mixed_coins":
            return self._generate_mixed_coins_problem()
        elif selected_subcategory == "making_change":
            return self._generate_making_change_problem()
        else:
            raise ValueError(f"Unsupported money counting subcategory: {selected_subcategory}")
    
    def _generate_identifying_coins_problem(self) -> Dict[str, Any]:
        """Generate a problem identifying a type of coin"""
        coin_type = random.choice(list(self.coin_values.keys()))
        
        return {
            "coin_type": coin_type,
            "answer": coin_type,
            "type": "identifying_coins",
            "display_type": "image"
        }
    
    def _generate_counting_pennies_nickels_problem(self) -> Dict[str, Any]:
        """Generate a problem counting pennies and nickels"""
        # Choose coin type
        coin_type = random.choice(["penny", "nickel"])
        
        # Number of coins (1-10)
        count = random.randint(1, 10)
        
        # Calculate total value
        total_value = count * self.coin_values[coin_type]
        
        return {
            "coin_type": coin_type,
            "count": count,
            "total_value": total_value,
            "answer": f"{total_value} cents",
            "type": "counting_pennies_nickels",
            "display_type": "coins"
        }
    
    def _generate_mixed_coins_problem(self) -> Dict[str, Any]:
        """Generate a problem counting a mix of coins"""
        # Select which coins to include
        if random.choice([True, False]):
            available_coins = ["penny", "nickel", "dime"]
        else:
            available_coins = ["penny", "nickel", "dime", "quarter"]
        
        # Generate a random mix of coins (3-8 coins total)
        coins = []
        for _ in range(random.randint(3, 8)):
            coins.append(random.choice(available_coins))
        
        # Calculate total value
        total_value = sum(self.coin_values[coin] for coin in coins)
        
        return {
            "coins": coins,
            "total_value": total_value,
            "answer": f"{total_value} cents",
            "type": "mixed_coins",
            "display_type": "coins"
        }
    
    def _generate_making_change_problem(self) -> Dict[str, Any]:
        """Generate a problem making change"""
        # Item cost (5-95 cents)
        cost = random.randint(5, 95)
        
        # Payment amount ($1.00)
        payment = 100
        
        # Calculate change
        change = payment - cost
        
        return {
            "cost": cost,
            "payment": payment,
            "change": change,
            "answer": f"{change} cents",
            "type": "making_change",
            "display_type": "text"
        }