# problem_generators/shapes.py (enhanced with visualization)

import random
from typing import Dict, Any, Optional, List
from .base import BaseProblemGenerator, BEGINNER, INTERMEDIATE, ADVANCED
from reportlab.graphics.shapes import Drawing, Rect, Circle, Polygon, String
from reportlab.lib import colors

class ShapesProblemGenerator(BaseProblemGenerator):
    """Generator for shape problems with visualization support"""
    
    def __init__(self):
        super().__init__()
        
        # Map of difficulty levels to available subcategories
        self.subcategories = {
            BEGINNER: ["basic_2d_3d"],
            INTERMEDIATE: ["basic_2d_3d", "edges_faces_vertices"],
            ADVANCED: ["edges_faces_vertices"]
        }
        
        # Define shapes with their properties
        self.shapes_2d = {
            "circle": {"sides": 0, "vertices": 0},
            "triangle": {"sides": 3, "vertices": 3},
            "square": {"sides": 4, "vertices": 4},
            "rectangle": {"sides": 4, "vertices": 4},
            "pentagon": {"sides": 5, "vertices": 5},
            "hexagon": {"sides": 6, "vertices": 6},
            "octagon": {"sides": 8, "vertices": 8}
        }
        
        self.shapes_3d = {
            "cube": {"faces": 6, "edges": 12, "vertices": 8},
            "rectangular prism": {"faces": 6, "edges": 12, "vertices": 8},
            "sphere": {"faces": 1, "edges": 0, "vertices": 0},
            "cone": {"faces": 2, "edges": 1, "vertices": 1},
            "cylinder": {"faces": 3, "edges": 2, "vertices": 0},
            "pyramid": {"faces": 5, "edges": 8, "vertices": 5}
        }
        
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
        """Generate a shapes problem for the given difficulty and subcategory"""
        
        # Validate difficulty
        if difficulty not in self.number_ranges:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")
        
        # Select subcategory if not specified
        available_subcategories = self.subcategories[difficulty]
        selected_subcategory = self.select_subcategory(available_subcategories, subcategory)
        
        # Generate problem based on subcategory
        if selected_subcategory == "basic_2d_3d":
            return self._generate_basic_2d_3d_problem(difficulty)
        elif selected_subcategory == "edges_faces_vertices":
            return self._generate_edges_faces_vertices_problem(difficulty)
        else:
            raise ValueError(f"Unsupported shapes subcategory: {selected_subcategory}")
    
    def generate_visualization(self, problem: Dict[str, Any]) -> Drawing:
        """
        Generate a visual representation of the shape problem
        
        Args:
            problem: Problem dictionary containing all necessary information
            
        Returns:
            A ReportLab Drawing object
        """
        shape_name = problem.get('shape_name', '')
        shape_type = problem.get('shape_type', '')
        
        # Size of the drawing
        width, height = 200, 200
        drawing = Drawing(width, height)
        
        # Center of the drawing
        cx, cy = width/2, height/2
        
        # Random color for the shape
        color = random.choice(self.kid_colors)
        
        if shape_name == "circle":
            shape = Circle(cx, cy, 70, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(shape)
        
        elif shape_name == "triangle":
            points = [cx, cy+70, cx-60, cy-35, cx+60, cy-35]
            shape = Polygon(points, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(shape)
        
        elif shape_name in ["square", "rectangle"]:
            if shape_name == "square":
                shape = Rect(cx-60, cy-60, 120, 120, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            else:
                shape = Rect(cx-70, cy-40, 140, 80, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(shape)
        
        elif shape_name == "pentagon":
            # Simple pentagon points
            points = [
                cx, cy+70,          # top
                cx+67, cy+22,       # upper right
                cx+41, cy-55,       # lower right
                cx-41, cy-55,       # lower left
                cx-67, cy+22        # upper left
            ]
            shape = Polygon(points, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(shape)
        
        elif shape_name == "hexagon":
            # Simple hexagon points
            points = [
                cx, cy+70,          # top
                cx+60, cy+35,       # upper right
                cx+60, cy-35,       # lower right
                cx, cy-70,          # bottom
                cx-60, cy-35,       # lower left
                cx-60, cy+35        # upper left
            ]
            shape = Polygon(points, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(shape)
        
        elif shape_name == "octagon":
            # Simple octagon points
            points = [
                cx+30, cy+70,       # upper right
                cx+70, cy+30,       # right upper
                cx+70, cy-30,       # right lower
                cx+30, cy-70,       # lower right
                cx-30, cy-70,       # lower left
                cx-70, cy-30,       # left lower
                cx-70, cy+30,       # left upper
                cx-30, cy+70        # upper left
            ]
            shape = Polygon(points, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(shape)
        
        # 3D shapes (simplified representations)
        elif shape_name == "cube" or shape_name == "rectangular prism":
            # Draw a simple 3D cube/prism
            # Front face
            front = Rect(cx-50, cy-50, 100, 100, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(front)
            
            # Top and side edges to give 3D effect
            top_points = [cx-50, cy+50, cx-20, cy+80, cx+80, cy+80, cx+50, cy+50]
            top = Polygon(top_points, fillColor=color.clone(alpha=0.8), strokeColor=colors.black, strokeWidth=2)
            drawing.add(top)
            
            side_points = [cx+50, cy+50, cx+80, cy+80, cx+80, cy-20, cx+50, cy-50]
            side = Polygon(side_points, fillColor=color.clone(alpha=0.6), strokeColor=colors.black, strokeWidth=2)
            drawing.add(side)
        
        elif shape_name == "sphere":
            # Draw a circle with shading to suggest a sphere
            outer = Circle(cx, cy, 70, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(outer)
            
            # Add highlight to suggest 3D
            highlight = Circle(cx-20, cy+20, 25, fillColor=colors.white.clone(alpha=0.3), strokeColor=None)
            drawing.add(highlight)
        
        elif shape_name == "cone":
            # Draw a simple cone
            # Triangular side
            side_points = [cx, cy+70, cx-60, cy-50, cx+60, cy-50]
            side = Polygon(side_points, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(side)
            
            # Circular base (ellipse to suggest perspective)
            base = Circle(cx, cy-50, 60, fillColor=color.clone(alpha=0.8), strokeColor=colors.black, strokeWidth=2)
            drawing.add(base)
        
        elif shape_name == "cylinder":
            # Draw a simple cylinder
            # Rectangle for the body
            body = Rect(cx-40, cy-60, 80, 120, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(body)
            
            # Ellipses for top and bottom to suggest 3D
            top = Circle(cx, cy+60, 40, fillColor=color.clone(alpha=0.8), strokeColor=colors.black, strokeWidth=2)
            drawing.add(top)
            
            bottom = Circle(cx, cy-60, 40, fillColor=color.clone(alpha=0.6), strokeColor=colors.black, strokeWidth=2)
            drawing.add(bottom)
        
        elif shape_name == "pyramid":
            # Draw a simple pyramid
            # Base
            base_points = [cx-60, cy-50, cx+60, cy-50, cx+60, cy+20, cx-60, cy+20]
            base = Polygon(base_points, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(base)
            
            # Triangular faces
            face1_points = [cx, cy+70, cx-60, cy-50, cx+60, cy-50]
            face1 = Polygon(face1_points, fillColor=color.clone(alpha=0.8), strokeColor=colors.black, strokeWidth=2)
            drawing.add(face1)
            
            # Another visible triangular face
            face2_points = [cx, cy+70, cx+60, cy-50, cx+60, cy+20]
            face2 = Polygon(face2_points, fillColor=color.clone(alpha=0.6), strokeColor=colors.black, strokeWidth=2)
            drawing.add(face2)
        
        else:
            # Default to a rectangle for unknown shapes
            shape = Rect(cx-60, cy-60, 120, 120, fillColor=color, strokeColor=colors.black, strokeWidth=2)
            drawing.add(shape)
            
            # Add text label
            drawing.add(String(cx-30, cy, shape_name, fontSize=14, fillColor=colors.black))
        
        # Add question mark for identification problems
        if problem.get('type') == 'basic_2d_3d':
            drawing.add(String(width-30, 20, "?", fontSize=24, fontName="Helvetica-Bold", fillColor=colors.red))
        
        # For edges/faces/vertices problems, highlight the relevant parts
        if problem.get('type') == 'edges_faces_vertices':
            question_type = problem.get('question_type', '')
            
            if question_type == 'vertices' and shape_name not in ['circle', 'sphere']:
                # Highlight vertices with small red circles
                if shape_name == 'square' or shape_name == 'rectangle':
                    vertices = [
                        (cx-60, cy-60), (cx+60, cy-60),  # Bottom corners
                        (cx+60, cy+60), (cx-60, cy+60)   # Top corners
                    ]
                    for vx, vy in vertices:
                        drawing.add(Circle(vx, vy, 5, fillColor=colors.red, strokeColor=colors.black, strokeWidth=1))
                
                # Add more vertex highlighting for other shapes as needed
            
            elif question_type == 'edges' and shape_name not in ['circle', 'sphere']:
                # Could add edge highlighting with thicker/colored lines
                pass
            
            elif question_type == 'faces' and shape_type == '3d':
                # Could add face highlighting with different colors
                pass
        
        return drawing
    
    def _generate_basic_2d_3d_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem identifying basic 2D or 3D shapes"""
        # For beginners, focus more on 2D shapes
        if difficulty == BEGINNER:
            shape_type = random.choices(["2d", "3d"], weights=[0.7, 0.3])[0]
        else:
            shape_type = random.choices(["2d", "3d"], weights=[0.1, 0.9])[0]
        
        if shape_type == "2d":
            shape_name = random.choice(list(self.shapes_2d.keys()))
            properties = self.shapes_2d[shape_name]
        else:
            shape_name = random.choice(list(self.shapes_3d.keys()))
            properties = self.shapes_3d[shape_name]
        
        return {
            "shape_name": shape_name,
            "shape_type": shape_type,
            "properties": properties,
            "answer": shape_name,
            "type": "basic_2d_3d",
            "display_type": "shape",
            "category": "shapes",
            "subcategory": "basic_2d_3d"
        }
    
    def _generate_edges_faces_vertices_problem(self, difficulty: str) -> Dict[str, Any]:
        """Generate a problem counting edges, faces, or vertices of shapes"""
        # Focus on 3D shapes for these problems
        shape_name = random.choice(list(self.shapes_3d.keys()))
        properties = self.shapes_3d[shape_name]
        
        # Choose which property to ask about
        if difficulty == INTERMEDIATE:
            # For intermediate, focus on simpler properties (faces)
            property_type = random.choice(["faces", "edges", "vertices"])
        else:  # ADVANCED
            # For advanced, focus more on complex properties
            property_type = random.choice(["edges", "vertices", "faces"])
        
        property_value = properties[property_type]
        
        return {
            "shape_name": shape_name,
            "shape_type": "3d",
            "question_type": property_type,
            "answer": str(property_value),
            "type": "edges_faces_vertices",
            "display_type": "shape",
            "category": "shapes",
            "subcategory": "edges_faces_vertices"
        }