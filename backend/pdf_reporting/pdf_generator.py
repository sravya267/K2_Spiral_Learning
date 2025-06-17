# pdf_generator.py

import os
import random
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics import renderPDF

# Import the problem generator
from problem_generators.problems import generate_problems


def generate_worksheet_pdf(output_path, worksheet_type, number_range, concepts, problem_count=None):
    """Generate a PDF worksheet with problems and visualizations"""
    
    # Generate problems using your existing function
    problems = generate_problems(worksheet_type, number_range, concepts, problem_count)
    
    # Create the PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Add a custom title style
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.purple,
    )
    
    # Add a custom problem style
    problem_style = ParagraphStyle(
        'Problem',
        parent=styles['Normal'],
        fontSize=14,
        leading=24,
    )
    
    # Elements to add to the PDF
    elements = []
    
    # Add title
    title = "Math Fun Worksheet!"
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 20))
    
    # Add each problem
    for i, problem in enumerate(problems):
        # Get problem details
        category = problem.get('category', '')
        
        # Format problem text based on category
        if category == 'addition':
            first_number = problem.get('first_number', 0)
            second_number = problem.get('second_number', 0)
            text = f"{i+1}. {first_number} + {second_number} = _______"
            
        elif category == 'subtraction':
            first_number = problem.get('first_number', 0)
            second_number = problem.get('second_number', 0)
            text = f"{i+1}. {first_number} - {second_number} = _______"
            
        elif category == 'shapes':
            shape_type = problem.get('subcategory', '')
            if shape_type == 'basic_2d_3d':
                text = f"{i+1}. What shape is shown? _______"
            else:
                text = f"{i+1}. Count the edges, faces, or vertices: _______"
                
        else:
            text = f"{i+1}. Problem: _______"
        
        elements.append(Paragraph(text, problem_style))
        
        # Try to add visualization if available
        try:
            # Get the appropriate generator based on category
            if category == 'addition':
                from problem_generators.addition import AdditionProblemGenerator
                generator = AdditionProblemGenerator()
            elif category == 'shapes':
                from problem_generators.shapes import ShapesProblemGenerator
                generator = ShapesProblemGenerator()
            # Add more categories as needed
            
            # Generate visualization
            if generator:
                drawing = generator.generate_visualization(problem)
                if drawing:
                    # Save drawing to temporary file
                    temp_file = f"temp_{i}.png"
                    renderPDF.drawToFile(drawing, temp_file, 'PNG')
                    
                    # Add image to document
                    from reportlab.platypus import Image
                    img = Image(temp_file, width=200, height=150)
                    elements.append(img)
                    elements.append(Spacer(1, 10))
        except Exception as e:
            print(f"Could not generate visualization for problem {i+1}: {e}")
        
        # Add space between problems
        elements.append(Spacer(1, 20))
    
    # Build the PDF
    doc.build(elements)
    
    return output_path


# # Example usage
# if __name__ == "__main__":
#     # Create addition worksheet
#     generate_worksheet_pdf(
#         "math_worksheet.pdf",
#         "fluency",
#         "beginner",
#         ["add_one"],
#         problem_count=5
#     )
    
#     # Create shapes worksheet
#     generate_worksheet_pdf(
#         "shapes_worksheet.pdf",
#         "fluency",
#         "beginner",
#         ["basic_2d_3d"],
#         problem_count=5
#     )