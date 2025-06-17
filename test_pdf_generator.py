# Update the import section to include logging
import logging
import os
import random
from typing import List, Dict, Any, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics import renderPDF

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)

# Ensure temp directory exists for visualizations
temp_viz_dir = os.path.join(current_dir, "temp_pdfs")
os.makedirs(temp_viz_dir, exist_ok=True)
logging.info(f"Temporary visualization directory: {temp_viz_dir}")


def try_generate_addition_viz(problem: Dict[str, Any], number: int) -> Optional[str]:
    """Try to generate an addition visualization"""
    try:
        # Import the AdditionProblemGenerator
        import sys
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from problem_generators.addition import AdditionProblemGenerator
        
        logging.info(f"Generating addition visualization for problem {number}")
        
        # Create generator and visualization
        generator = AdditionProblemGenerator()
        drawing = generator.generate_visualization(problem)
        
        if drawing:
            # Save to temporary file
            output_path = os.path.join(temp_viz_dir, f"addition_{number}.png")
            renderPDF.drawToFile(drawing, output_path, 'PNG')
            logging.info(f"Addition visualization saved to: {output_path}")
            return output_path
        else:
            logging.warning(f"Addition generator returned None for problem {number}")
    except Exception as e:
        logging.error(f"Could not generate addition visualization: {e}")
    
    return None


def try_generate_shapes_viz(problem: Dict[str, Any], number: int) -> Optional[str]:
    """Try to generate a shapes visualization"""
    try:
        # Import the ShapesProblemGenerator
        import sys
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from problem_generators.shapes import ShapesProblemGenerator
        
        logging.info(f"Generating shapes visualization for problem {number}")
        
        # Create generator and visualization
        generator = ShapesProblemGenerator()
        drawing = generator.generate_visualization(problem)
        
        if drawing:
            # Save to temporary file
            output_path = os.path.join(temp_viz_dir, f"shape_{number}.png")
            renderPDF.drawToFile(drawing, output_path, 'PNG')
            logging.info(f"Shape visualization saved to: {output_path}")
            return output_path
        else:
            logging.warning(f"Shapes generator returned None for problem {number}")
    except Exception as e:
        logging.error(f"Could not generate shapes visualization: {e}")
    
    return None