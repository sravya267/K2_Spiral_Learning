# problem_generators/base.py (enhanced with visualization support)

from typing import Dict, Any, Optional, List
import random
from reportlab.graphics.shapes import Drawing

# Constants for difficulty levels
BEGINNER = "beginner"
INTERMEDIATE = "intermediate"
ADVANCED = "advanced"

class BaseProblemGenerator:
    """Base class for all problem generators with visualization support"""
    
    def __init__(self):
        # Define number ranges for each difficulty level
        self.number_ranges = {
            BEGINNER: (0, 9),         # Single-digit (0-9)
            INTERMEDIATE: (10, 99),    # Double-digit (10-99)
            ADVANCED: (100, 999)       # Triple-digit (100-999)
        }
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a problem for the given difficulty level and subcategory.
        
        Args:
            difficulty: "beginner", "intermediate", or "advanced"
            subcategory: Specific subcategory (e.g., "add_zero" for addition)
            
        Returns:
            A problem dictionary containing question, answer, and display information
        """
        raise NotImplementedError("Subclasses must implement generate_problem")
    
    def generate_visualization(self, problem: Dict[str, Any]) -> Drawing:
        """
        Generate a ReportLab Drawing object to visualize the problem.
        
        Args:
            problem: Problem dictionary containing all necessary information
            
        Returns:
            A ReportLab Drawing object or None if no visualization is available
        """
        # Default implementation returns None - subclasses should override this
        return None
    
    def generate_random_number(self, difficulty: str) -> int:
        """Generate a random number within the range for the given difficulty level."""
        min_val, max_val = self.number_ranges[difficulty]
        return random.randint(min_val, max_val)
    
    def select_subcategory(self, subcategories: List[str], requested: Optional[str] = None) -> str:
        """
        Select a subcategory from the available ones.
        
        Args:
            subcategories: List of available subcategories
            requested: Specifically requested subcategory (if any)
            
        Returns:
            Selected subcategory
        """
        if requested and requested in subcategories:
            return requested
        return random.choice(subcategories)