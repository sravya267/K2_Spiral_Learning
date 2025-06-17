# problem_generators/addition.py (enhanced with visualization)

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.units import inch

class AdditionProblemGenerator(BaseProblemGenerator):
    """Generator for addition problems with visualization support"""
    
    def __init__(self):
        super().__init__()
        
        # Single list of all available subcategories
        self.subcategories = ["add_zero", "add_one", "same_number_addition", "near_doubles", "add_random_numbers"]
        
        # Kid-friendly colors for visualizations
        self.kid_colors = [
            colors.HexColor('#FF9AA2'),  # soft red
            colors.HexColor('#FFB7B2'),  # salmon
            colors.HexColor('#FFDAC1'),  # peach
            colors.HexColor('#E2F0CB'),  # light green
            colors.HexColor('#B5EAD7'),  # mint
            colors.HexColor('#C7CEEA'),  # lavender
            colors.HexColor('#9ADCFF'),  # light blue
        ]
    
    def generate_problem(self, difficulty: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """Generate an addition problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        selected_subcategory = self.select_subcategory(self.subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "add_zero":
            return self._generate_add_zero_problem(difficulty)
        elif selected_subcategory == "add_one":
            return self._generate_add_one_problem(difficulty)
        elif selected_subcategory == "same_number_addition":
            return self._generate_same_number_problem(difficulty)
        elif selected_subcategory == "near_doubles":
            return self._generate_near_doubles_problem(difficulty)
        elif selected_subcategory == "add_random_numbers":
            return self._generate_random_numbers_problem(difficulty)
        else:
            raise ValueError(f"Unsupported addition subcategory: {selected_subcategory}")
    
    def generate_visualization(self, problem: Dict[str, Any]) -> Drawing:
        """
        Generate a visual representation of the addition problem
        
        Args:
            problem: Problem dictionary containing all necessary information
            
        Returns:
            A ReportLab Drawing object
        """
        first_number = problem.get('first_number', 0)
        second_number = problem.get('second_number', 0)
        
        # Different visualizations based on number size
        if first_number <= 10 and second_number <= 10:
            return self._generate_block_visualization(first_number, second_number)
        else:
            return self._generate_bar_chart_visualization(first_number, second_number)
    
    def _generate_block_visualization(self, first_number: int, second_number: int) -> Drawing:
        """Generate visualization using colored blocks for small numbers"""
        # Size and spacing parameters
        block_size = 30
        block_spacing = 5
        row_spacing = 40
        padding = 10
        
        # Calculate drawing dimensions
        max_blocks = max(first_number, second_number)
        drawing_width = (block_size + block_spacing) * max_blocks + padding * 2
        drawing_height = row_spacing * 3 + padding * 2  # 3 rows: first number, operator, second number
        
        drawing = Drawing(drawing_width, drawing_height)
        
        # Draw blocks for first number
        for i in range(first_number):
            color = random.choice(self.kid_colors)
            x = padding + i * (block_size + block_spacing)
            y = drawing_height - padding - block_size
            rect = Rect(x, y, block_size, block_size, 
                        fillColor=color, strokeColor=colors.black, strokeWidth=1)
            drawing.add(rect)
        
        # Draw + operator
        plus_x = drawing_width / 2
        plus_y = drawing_height - padding - block_size - row_spacing / 2
        drawing.add(String(plus_x - 5, plus_y - 5, "+", fontSize=16, fillColor=colors.black))
        
        # Draw blocks for second number
        for i in range(second_number):
            color = random.choice(self.kid_colors)
            x = padding + i * (block_size + block_spacing)
            y = drawing_height - padding - block_size - row_spacing - block_size
            rect = Rect(x, y, block_size, block_size, 
                        fillColor=color, strokeColor=colors.black, strokeWidth=1)
            drawing.add(rect)
            
        # Draw equals sign
        equals_x = drawing_width / 2
        equals_y = padding + row_spacing / 2
        drawing.add(String(equals_x - 5, equals_y - 5, "=", fontSize=16, fillColor=colors.black))
        
        # Draw question mark for answer
        question_x = drawing_width / 2
        question_y = padding + 5
        drawing.add(String(question_x - 5, question_y - 5, "?", fontSize=16, fillColor=colors.black))
        
        return drawing
    
    def _generate_bar_chart_visualization(self, first_number: int, second_number: int) -> Drawing:
        """Generate visualization using bar chart for larger numbers"""
        drawing_width = 300
        drawing_height = 200
        
        drawing = Drawing(drawing_width, drawing_height)
        
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 200
        chart.data = [[first_number, second_number]]
        chart.bars[0].fillColor = random.choice(self.kid_colors)
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(first_number, second_number) * 1.2
        chart.categoryAxis.labels.boxAnchor = 'n'
        chart.categoryAxis.labels.dx = 0
        chart.categoryAxis.labels.dy = -10
        chart.categoryAxis.categoryNames = [str(first_number), str(second_number)]
        
        drawing.add(chart)
        
        # Add + symbol between bars
        plus_x = 150
        plus_y = 30
        drawing.add(String(plus_x - 5, plus_y, "+", fontSize=18, fillColor=colors.black))
        
        # Add equals and question mark
        equals_x = 250
        equals_y = 100
        drawing.add(String(equals_x, equals_y, "= ?", fontSize=18, fillColor=colors.black))
        
        return drawing
    
    def _generate_add_zero_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate an addition problem where one number is zero"""
        num = self.generate_random_number(difficulty)
        
        return {
            "first_number": num,
            "second_number": 0,
            "answer": str(num),
            "type": "addition",
            "display_type": "vertical",
            "category": "addition",
            "subcategory": "add_zero"
        }
    
    def _generate_add_one_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate an addition problem where one number is one"""
        num = self.generate_random_number(difficulty)
        
        return {
            "first_number": num,
            "second_number": 1,
            "answer": str(num + 1),
            "type": "addition",
            "display_type": "vertical",
            "category": "addition",
            "subcategory": "add_one"
        }
    
    def _generate_same_number_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate an addition problem where both numbers are the same"""
        if difficulty == BEGINNER:
            # For beginner, use 0-20 range
            num = random.randint(0, 20)
        elif difficulty == INTERMEDIATE:
            # For intermediate, use 10-100 range
            num = random.randint(10, 100)
        else:  # ADVANCED
            # For advanced, use 100-999 range
            num = random.randint(100, 999)
        
        return {
            "first_number": num,
            "second_number": num,
            "answer": str(num + num),
            "type": "addition",
            "display_type": "vertical",
            "category": "addition",
            "subcategory": "same_number_addition"
        }
    
    def _generate_near_doubles_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a near-doubles addition problem (a + (a+1))"""
        if difficulty == BEGINNER:
            # For beginner, use 0-20 range
            base = random.randint(0, 19)  # Up to 19 so +1 stays in range
        elif difficulty == INTERMEDIATE:
            # For intermediate, use 10-100 range
            base = random.randint(10, 99)  # Up to 99 so +1 stays in range
        else:  # ADVANCED
            # For advanced, use 100-999 range
            base = random.randint(100, 998)  # Up to 998 so +1 stays in range
        
        num1 = base
        num2 = base + 1
        
        return {
            "first_number": num1,
            "second_number": num2,
            "answer": str(num1 + num2),
            "type": "addition",
            "display_type": "vertical",
            "category": "addition",
            "subcategory": "near_doubles"
        }
    
    def _generate_random_numbers_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate an addition problem with two random numbers within the difficulty range"""
        if difficulty == BEGINNER:
            # For beginner, use numbers 0-20
            num1 = random.randint(0, 20)
            num2 = random.randint(0, 20)
        elif difficulty == INTERMEDIATE:
            # For intermediate, use numbers 10-100
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
        else:  # ADVANCED
            # For advanced, use numbers 100-999
            num1 = random.randint(100, 999)
            num2 = random.randint(100, 999)
        
        return {
            "first_number": num1,
            "second_number": num2,
            "answer": str(num1 + num2),
            "type": "addition",
            "display_type": "vertical",
            "category": "addition",
            "subcategory": "add_random_numbers"
        }