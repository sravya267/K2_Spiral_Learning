from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from pydantic import BaseModel
from typing import List, Optional
import tempfile

from problem_generators.problems import generate_problems
from pdf_reporting.pdf_generator import create_worksheet_pdf

app = FastAPI(title="Math Worksheet Generator API")

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sravya1.pythonanywhere.com", "http://localhost:3000"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory if it doesn't exist
os.makedirs("temp_pdfs", exist_ok=True)

class WorksheetRequest(BaseModel):
    worksheet_type: str  # "spiral" or "fluency"
    number_range: str  # "beginner", "intermediate", or "advanced"
    concepts: List[str]  # List of selected math concepts
    problem_count: Optional[int] = 15  # Default for fluency sheets

@app.get("/")
async def root():
    return {"message": "Math Worksheet Generator API"}

@app.get("/concepts")
async def get_concepts():
    """Returns all available math concepts organized by category"""
    return {
        "number_sense": ["subitizing", "comparison", "ordering", "before_after", "missing_numbers"],
        "addition": ["add_zero", "add_one", "same_number_addition", "near_doubles"],
        "subtraction": ["subtract_zero", "subtract_one", "same_number_subtraction", "near_doubles"],
        "time_telling": ["whole_hours", "half_hours", "quarter_hours", "five_minute_increments"],
        "money_counting": ["identifying_coins", "counting_pennies_nickels", "mixed_coins", "making_change"],
        "place_value": ["ones_tens", "ones_tens_hundreds", "expanded_form"],
        "word_problems": ["one_step", "two_step", "multi_step"],
        "shapes": ["basic_2d_3d", "edges_faces_vertices"],
        "skip_counting": ["by_ones_twos", "by_fives_tens", "by_hundreds"],
        "fractions": ["halves_wholes", "thirds_fourths", "comparing_fractions"],
        "measurement": ["comparing_objects", "non_standard_units", "rulers_inches_cm"],
        "patterns": ["abab_patterns", "extending_patterns", "creating_patterns"],
        "graphing": ["pictographs", "bar_graphs", "analyzing_data"],
        "odd_even": ["identifying", "sorting", "problem_solving"]
    }

@app.post("/generate-worksheet")
async def generate_worksheet(request: WorksheetRequest):
    """Generates a math worksheet based on user specifications"""

    # Validate request
    if request.worksheet_type not in ["spiral", "fluency"]:
        raise HTTPException(status_code=400, detail="Invalid worksheet type")

    if request.number_range not in ["beginner", "intermediate", "advanced"]:
        raise HTTPException(status_code=400, detail="Invalid number range")

    if not request.concepts:
        raise HTTPException(status_code=400, detail="No concepts selected")

    if request.worksheet_type == "fluency" and len(request.concepts) > 1:
        raise HTTPException(status_code=400, detail="Fluency worksheets can only target one concept")

    # Generate problems
    try:
        problems = generate_problems(
            worksheet_type=request.worksheet_type,
            number_range=request.number_range,
            concepts=request.concepts,
            problem_count=request.problem_count if request.worksheet_type == "fluency" else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating problems: {str(e)}")

    # Create a unique filename for the PDF
    filename = f"math_worksheet_{uuid.uuid4()}.pdf"
    filepath = os.path.join("temp_pdfs", filename)

    # Generate PDF
    try:
        create_worksheet_pdf(
            problems=problems,
            worksheet_type=request.worksheet_type,
            number_range=request.number_range,
            concepts=request.concepts,
            output_path=filepath
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating PDF: {str(e)}")

    # Return the PDF file
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/pdf"
    )

@app.on_event("shutdown")
def cleanup():
    """Clean up temporary files on shutdown"""
    for file in os.listdir("temp_pdfs"):
        try:
            os.remove(os.path.join("temp_pdfs", file))
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)










#*******************************************************************************
#*******************************************************************************









# import sys
# import os

# # Add the project root to the Python path
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, project_root)


# from fastapi import FastAPI, Form, HTTPException
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from typing import List, Optional
# import os
# from datetime import datetime
# import traceback

# # Import from other modules
# from problem_generators.problems import generate_problem, get_number_range  # Import from problems.py
# from pdf_reporting.pdf_generator import create_worksheet_pdf  # Import from pdf_generator.py

# # Print virtual environment information
# print("Python Executable:", sys.executable)
# print("Virtual Environment:", os.environ.get('VIRTUAL_ENV', 'Not in a virtual environment'))

# app = FastAPI(title="Math Worksheet Generator API")

# # Enable CORS for React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://sravya1.pythonanywhere.com", "http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Conditionally mount static files directory if it exists
# static_dir = "/home/sravya1/K2_Spiral_Learning/frontend/build/static"
# if os.path.exists(static_dir):
#     app.mount("/static", StaticFiles(directory=static_dir), name="static")

# # Create a directory for temporary PDFs if it doesn't exist
# temp_pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_pdfs")
# os.makedirs(temp_pdf_dir, exist_ok=True)

# # Models for request validation
# class WorksheetRequest(BaseModel):
#     worksheet_type: str
#     difficulty: str
#     concepts: List[str]
#     include_answer_key: bool = False
#     question_count: Optional[int] = 15

# @app.get("/api/health")
# def health_check():
#     return {"status": "healthy", "message": "Math Worksheet Generator API is running"}

# @app.post("/api/generate-worksheet")
# async def generate_worksheet(
#     worksheet_type: str = Form(...),
#     difficulty: str = Form(...),
#     concepts: List[str] = Form(...),
#     include_answer_key: bool = Form(False),
#     question_count: int = Form(15)
# ):
#     try:
#         # Get number range based on difficulty using the imported function
#         number_range = get_number_range(difficulty)

#         # Generate problems using the imported function
#         problems_with_answers = []

#         if worksheet_type == "spiral":
#             # Create spiral review with one problem from each selected concept
#             for concept in concepts:
#                 problem, answer = generate_problem(concept, number_range)
#                 problems_with_answers.append((problem, answer, concept))
#         else:  # fluency practice
#             concept = concepts[0]  # Only use the first selected concept for fluency
#             for _ in range(question_count):
#                 problem, answer = generate_problem(concept, number_range)
#                 problems_with_answers.append((problem, answer, concept))

#         # Generate title
#         if worksheet_type == "spiral":
#             title = "Math Spiral Review"
#         else:
#             concept_name = concepts[0].replace("_", " ").title()
#             title = f"{concept_name} Fluency Practice"

#         # Create the worksheet PDF using the imported function
#         pdf_path = create_worksheet_pdf(
#             worksheet_type=worksheet_type,
#             concepts=concepts,
#             problems_with_answers=problems_with_answers,
#             include_answer_key=include_answer_key,
#             title=title
#         )

#         # Generate a unique filename for the response
#         filename = f"math_worksheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

#         # Headers for file download
#         headers = {
#             "Content-Disposition": f"attachment; filename={filename}",
#             "Content-Type": "application/pdf",
#         }

#         # Make sure the file exists before attempting to return it
#         if not os.path.exists(pdf_path):
#             raise HTTPException(status_code=500, detail="PDF generation failed")

#         # Log file size for debugging
#         file_size = os.path.getsize(pdf_path)
#         print(f"Generated PDF size: {file_size} bytes")

#         return FileResponse(
#             path=pdf_path,
#             filename=filename,
#             headers=headers,
#             media_type="application/pdf"
#         )
#     except Exception as e:
#         error_details = traceback.format_exc()
#         print(f"Error generating worksheet: {str(e)}\n{error_details}")
#         raise HTTPException(status_code=500, detail=f"Error generating worksheet: {str(e)}")

# @app.get("/api/download/{filename}")
# async def download_file(filename: str):
#     file_path = os.path.join(temp_pdf_dir, filename)

#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     return FileResponse(
#         path=file_path,
#         filename=f"math_worksheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
#         media_type="application/pdf"
#     )

# @app.get("/api/concepts")
# async def get_concepts():
#     """Return all available math concepts."""
#     concepts = [
#         {"id": "number_sense", "name": "Number Sense", "icon": "#"},
#         {"id": "addition", "name": "Addition", "icon": "+"},
#         {"id": "subtraction", "name": "Subtraction", "icon": "−"},
#         {"id": "time_telling", "name": "Time Telling", "icon": "🕒"},
#         {"id": "money_counting", "name": "Money", "icon": "💰"},
#         {"id": "place_value", "name": "Place Value", "icon": "1️⃣"},
#         {"id": "word_problems", "name": "Word Problems", "icon": "📝"},
#         {"id": "shapes", "name": "Shapes", "icon": "⭐"},
#         {"id": "skip_counting", "name": "Skip Counting", "icon": "2️⃣"},
#         {"id": "fractions", "name": "Fractions", "icon": "½"},
#         {"id": "measurement", "name": "Measurement", "icon": "📏"},
#         {"id": "patterns_algebra", "name": "Patterns & Algebra", "icon": "🔄"},
#         {"id": "graphing_data", "name": "Graphing & Data", "icon": "📊"},
#         {"id": "odd_even", "name": "Odd & Even", "icon": "🔢"}
#     ]
#     return {"concepts": concepts}

# @app.get("/debug-pdf-test")
# def debug_pdf_test():
#     try:
#         from reportlab.pdfgen import canvas
#         from reportlab.lib.pagesizes import letter

#         # Create absolute path for PDF file
#         test_filename = os.path.join(temp_pdf_dir, f"debug_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
#         print(f"Debug test PDF path: {test_filename}")

#         # Ensure directory exists
#         os.makedirs(temp_pdf_dir, exist_ok=True)

#         # Create a simple PDF with reportlab directly
#         c = canvas.Canvas(test_filename, pagesize=letter)
#         c.setFont("Helvetica", 12)
#         c.drawString(100, 700, "Debug PDF Test")
#         c.drawString(100, 680, "If you can read this, PDF generation is working correctly.")
#         c.drawString(100, 660, f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         c.save()

#         # Verify the file exists and has content
#         if os.path.exists(test_filename) and os.path.getsize(test_filename) > 0:
#             print(f"Debug PDF created successfully. Size: {os.path.getsize(test_filename)} bytes")

#             # Serve the PDF file
#             headers = {
#                 "Content-Disposition": f"attachment; filename=debug_test.pdf",
#                 "Content-Type": "application/pdf",
#             }

#             return FileResponse(
#                 path=test_filename,
#                 filename="debug_test.pdf",
#                 headers=headers,
#                 media_type="application/pdf"
#             )
#         else:
#             return {"error": "Failed to create PDF file"}

#     except Exception as e:
#         error_details = traceback.format_exc()
#         return {"error": str(e), "traceback": error_details}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)