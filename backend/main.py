from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_reporting.pdf_generator import create_worksheet_pdf
from problem_generators.problems import generate_problems

app = FastAPI(title="Math Worksheet Generator API")

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://k2-spiral-frontend-929048657215.us-central1.run.app",  # Cloud Run frontend URL
        "http://localhost:3000"                                        # For local development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],                                     # Limit to methods you actually use
    allow_headers=["Content-Type", "Authorization"],                   # Common required headers
)

# Create temp directory if it doesn't exist
os.makedirs("temp_pdfs", exist_ok=True)

class WorksheetRequest(BaseModel):
    worksheet_type: str  # "spiral" or "fluency"
    difficulty: str  # "beginner", "intermediate", or "advanced" (instead of number_range)
    concepts: List[str]  # List of selected math concepts
    include_answer_key: bool = False  # Added to match frontend
    question_count: Optional[int] = 15  # Changed from problem_count to question_count

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

@app.post("/api/generate-worksheet")
async def generate_worksheet(request: WorksheetRequest):
    """Generates a math worksheet based on user specifications"""

    # Map difficulty to number_range (they're the same in this case)
    number_range = request.difficulty

    # Validate request
    if request.worksheet_type not in ["spiral", "fluency"]:
        raise HTTPException(status_code=400, detail="Invalid worksheet type")

    if number_range not in ["beginner", "intermediate", "advanced"]:
        raise HTTPException(status_code=400, detail="Invalid number range")

    if not request.concepts:
        raise HTTPException(status_code=400, detail="No concepts selected")

    if request.worksheet_type == "fluency" and len(request.concepts) > 1:
        raise HTTPException(status_code=400, detail="Fluency worksheets can only target one concept")

    # Generate problems
    try:
        problems = generate_problems(
            worksheet_type=request.worksheet_type,
            number_range=number_range,
            concepts=request.concepts,
            problem_count=request.question_count if request.worksheet_type == "fluency" else None
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
            number_range=number_range,
            concepts=request.concepts,
            output_path=filepath,
            include_answer_key=request.include_answer_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating PDF: {str(e)}")

    # Return a download URL instead of the file directly
    # For Cloud Run, we'll need the full URL with the appropriate host
    # Since we can't predict the exact URL, we'll use a relative path and let the frontend handle it
    download_url = f"/api/download/{filename}"
    return {"download_url": download_url}

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Endpoint to download the generated PDF file"""
    filepath = os.path.join("temp_pdfs", filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=filepath,
        filename=f"math_worksheet.pdf",
        media_type="application/pdf"
    )

# Add a health check endpoint for Cloud Run
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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
    # Use port 8080 for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)