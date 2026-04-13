# pdf_generator.py

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def _format_problem_text(i, problem):
    """Format a problem dict into a human-readable string for the worksheet."""
    # Many generators (word_problems, odd_even, graphing, place_value, etc.) include a pre-built question
    if "question" in problem:
        return f"{i + 1}. {problem['question']}"

    category = problem.get("category", "")
    prob_type = problem.get("type", "")

    if category in ("addition",) or prob_type == "addition":
        first = problem.get("first_number", "?")
        second = problem.get("second_number", "?")
        return f"{i + 1}.  {first}  +  {second}  =  _______"

    if category in ("subtraction",) or prob_type == "subtraction":
        first = problem.get("first_number", "?")
        second = problem.get("second_number", "?")
        return f"{i + 1}.  {first}  -  {second}  =  _______"

    if prob_type == "comparison":
        first = problem.get("first_number", "?")
        second = problem.get("second_number", "?")
        return f"{i + 1}.  {first}  ___  {second}  (use <, >, or =)"

    if prob_type == "ordering":
        numbers = problem.get("numbers", [])
        return f"{i + 1}.  Order from least to greatest:  {',  '.join(str(n) for n in numbers)}"

    if prob_type == "before_after":
        num = problem.get("number", "?")
        q_type = problem.get("question_type", "before")
        return f"{i + 1}.  What comes {q_type} {num}?  _______"

    if prob_type == "missing_numbers":
        sequence = problem.get("sequence", problem.get("numbers", []))
        seq_str = ",  ".join("___" if n is None else str(n) for n in sequence)
        return f"{i + 1}.  Fill in the missing number:  {seq_str}"

    # Generic fallback
    return f"{i + 1}.  _______"


def create_worksheet_pdf(problems, worksheet_type, number_range, concepts, output_path, include_answer_key=False):
    """Generate a PDF worksheet from pre-generated problems.

    Args:
        problems: List of problem dicts from generate_problems()
        worksheet_type: "spiral" or "fluency"
        number_range: "beginner", "intermediate", or "advanced"
        concepts: List of concept identifiers
        output_path: File path to write the PDF to
        include_answer_key: Whether to append an answer key page
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "WorksheetTitle",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.purple,
        spaceAfter=16,
    )

    subtitle_style = ParagraphStyle(
        "WorksheetSubtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.grey,
        spaceAfter=12,
    )

    problem_style = ParagraphStyle(
        "Problem",
        parent=styles["Normal"],
        fontSize=14,
        leading=24,
    )

    answer_key_title_style = ParagraphStyle(
        "AnswerKeyTitle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.darkblue,
        spaceAfter=12,
    )

    answer_style = ParagraphStyle(
        "Answer",
        parent=styles["Normal"],
        fontSize=12,
        leading=20,
    )

    elements = []

    # --- Header ---
    type_label = "Spiral Review" if worksheet_type == "spiral" else "Fluency Sheet"
    elements.append(Paragraph("Math Fun Worksheet!", title_style))
    elements.append(Paragraph(f"{type_label}  |  Difficulty: {number_range.capitalize()}", subtitle_style))
    elements.append(Spacer(1, 10))

    # --- Problems ---
    for i, problem in enumerate(problems):
        text = _format_problem_text(i, problem)
        elements.append(Paragraph(text, problem_style))

        # Optionally embed a visualization (Drawing is a Flowable in ReportLab)
        category = problem.get("category", "")
        try:
            generator = None
            if category == "addition":
                from problem_generators.addition import AdditionProblemGenerator
                generator = AdditionProblemGenerator()
            elif category == "shapes":
                from problem_generators.shapes import ShapesProblemGenerator
                generator = ShapesProblemGenerator()

            if generator is not None:
                drawing = generator.generate_visualization(problem)
                if drawing is not None:
                    elements.append(drawing)
                    elements.append(Spacer(1, 6))
        except Exception as e:
            # Visualization is optional; never let it break PDF generation
            print(f"Could not generate visualization for problem {i + 1}: {e}")

        elements.append(Spacer(1, 20))

    # --- Answer Key (optional) ---
    if include_answer_key:
        elements.append(PageBreak())
        elements.append(Paragraph("Answer Key", answer_key_title_style))
        elements.append(Spacer(1, 10))
        for i, problem in enumerate(problems):
            answer = problem.get("answer", "—")
            elements.append(Paragraph(f"{i + 1}.  {answer}", answer_style))

    doc.build(elements)
    return output_path
