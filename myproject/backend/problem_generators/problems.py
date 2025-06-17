import random
import math
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

def generate_problems(
    worksheet_type: str,
    number_range: str,
    concepts: List[str],
    problem_count: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Generate math problems based on worksheet type, number range, and selected concepts.

    Args:
        worksheet_type: "spiral" or "fluency"
        number_range: "beginner", "intermediate", or "advanced"
        concepts: List of concept identifiers
        problem_count: Number of problems (for fluency worksheets)

    Returns:
        List of problem dictionaries containing the necessary data to render each problem
    """

    # Set number range limits based on proficiency level
    if number_range == "beginner":
        max_num = 9  # Single-digit
    elif number_range == "intermediate":
        max_num = 99  # Double-digit
    else:  # advanced
        max_num = 999  # Triple-digit

    problems = []

    # For spiral review, generate one problem per concept
    if worksheet_type == "spiral":
        for concept in concepts:
            problem = generate_problem_for_concept(concept, number_range, max_num)
            if problem:
                problems.append(problem)

    # For fluency practice, generate multiple problems of the same type
    else:  # fluency
        count = problem_count or 15  # Default to 15 if not specified
        concept = concepts[0]  # Fluency worksheets focus on a single concept

        for _ in range(count):
            problem = generate_problem_for_concept(concept, number_range, max_num)
            if problem:
                problems.append(problem)

    return problems

def generate_problem_for_concept(concept: str, number_range: str, max_num: int) -> Dict[str, Any]:
    """Generate a single problem for the given concept"""

    # Extract category and subcategory from concept string
    if "_" in concept:
        parts = concept.split("_", 1)
        category = parts[0]
        subcategory = parts[1] if len(parts) > 1 else ""
    else:
        category = concept
        subcategory = ""

    # Dispatch to the appropriate generator based on category
    if category == "addition":
        return generate_addition_problem(subcategory, max_num)
    elif category == "subtraction":
        return generate_subtraction_problem(subcategory, max_num)
    elif category == "number_sense":
        return generate_number_sense_problem(subcategory, max_num)
    elif category == "time_telling":
        return generate_time_problem(subcategory)
    elif category == "money_counting":
        return generate_money_problem(subcategory, max_num)
    elif category == "place_value":
        return generate_place_value_problem(subcategory, max_num)
    elif category == "word_problems":
        return generate_word_problem(subcategory, max_num)
    elif category == "shapes":
        return generate_shapes_problem(subcategory)
    elif category == "skip_counting":
        return generate_skip_counting_problem(subcategory, max_num)
    elif category == "fractions":
        return generate_fraction_problem(subcategory)
    elif category == "measurement":
        return generate_measurement_problem(subcategory, max_num)
    elif category == "patterns":
        return generate_pattern_problem(subcategory, max_num)
    elif category == "graphing":
        return generate_graphing_problem(subcategory)
    elif category == "odd_even":
        return generate_odd_even_problem(subcategory, max_num)
    else:
        # Default to number sense if category not recognized
        return generate_number_sense_problem("comparison", max_num)

# Individual problem generators for each category

def generate_addition_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate addition problems based on subcategory"""
    problem = {
        "category": "addition",
        "subcategory": subcategory,
        "format": "vertical"
    }

    if subcategory == "add_zero":
        num = random.randint(1, max_num)
        problem.update({
            "first_number": num,
            "second_number": 0,
            "answer": num
        })
    elif subcategory == "add_one":
        num = random.randint(1, max_num - 1)
        problem.update({
            "first_number": num,
            "second_number": 1,
            "answer": num + 1
        })
    elif subcategory == "same_number_addition":
        num = random.randint(1, max_num // 2)
        problem.update({
            "first_number": num,
            "second_number": num,
            "answer": num + num
        })
    elif subcategory == "near_doubles":
        base = random.randint(1, max_num // 2)
        problem.update({
            "first_number": base,
            "second_number": base + 1,
            "answer": base + base + 1
        })
    else:
        # Default addition problem
        if max_num <= 9:  # Beginner
            a = random.randint(1, 5)
            b = random.randint(1, 9 - a)  # Ensure sum is single digit
        elif max_num <= 99:  # Intermediate
            a = random.randint(10, 50)
            b = random.randint(10, 40)
        else:  # Advanced
            a = random.randint(100, 500)
            b = random.randint(100, 400)

        problem.update({
            "first_number": a,
            "second_number": b,
            "answer": a + b
        })

    return problem

def generate_subtraction_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate subtraction problems based on subcategory"""
    problem = {
        "category": "subtraction",
        "subcategory": subcategory,
        "format": "vertical"
    }

    if subcategory == "subtract_zero":
        num = random.randint(1, max_num)
        problem.update({
            "first_number": num,
            "second_number": 0,
            "answer": num
        })
    elif subcategory == "subtract_one":
        num = random.randint(2, max_num)
        problem.update({
            "first_number": num,
            "second_number": 1,
            "answer": num - 1
        })
    elif subcategory == "same_number_subtraction":
        num = random.randint(1, max_num)
        problem.update({
            "first_number": num,
            "second_number": num,
            "answer": 0
        })
    elif subcategory == "near_doubles":
        result = random.randint(0, max_num // 2)
        base = result * 2 + 1
        problem.update({
            "first_number": base,
            "second_number": result + 1,
            "answer": result
        })
    else:
        # Default subtraction problem (no borrowing)
        if max_num <= 9:  # Beginner
            b = random.randint(1, 5)
            a = random.randint(b, 9)  # Ensure positive result
        elif max_num <= 99:  # Intermediate
            b = random.randint(10, 40)
            a = random.randint(b, 99)  # Ensure positive result
        else:  # Advanced
            b = random.randint(100, 400)
            a = random.randint(b, 999)  # Ensure positive result

        problem.update({
            "first_number": a,
            "second_number": b,
            "answer": a - b
        })

    return problem

def generate_number_sense_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate number sense problems based on subcategory"""
    problem = {
        "category": "number_sense",
        "subcategory": subcategory
    }

    if subcategory == "subitizing":
        num = random.randint(1, min(5, max_num))
        problem.update({
            "number": num,
            "format": "dots",
            "answer": num
        })
    elif subcategory == "comparison":
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        while a == b:  # Ensure numbers are different
            b = random.randint(1, max_num)

        symbol = "<" if a < b else ">" if a > b else "="
        problem.update({
            "first_number": a,
            "second_number": b,
            "format": "comparison",
            "answer": symbol
        })
    elif subcategory == "ordering":
        numbers = random.sample(range(1, max_num + 1), min(5, max_num))
        ordered = sorted(numbers)
        problem.update({
            "numbers": numbers,
            "format": "ordering",
            "answer": ordered
        })
    elif subcategory == "before_after":
        num = random.randint(2, max_num - 1)
        is_before = random.choice([True, False])
        question_num = num - 1 if is_before else num + 1
        problem.update({
            "number": num,
            "question_type": "before" if is_before else "after",
            "format": "before_after",
            "answer": question_num
        })
    elif subcategory == "missing_numbers":
        start = random.randint(1, max(1, max_num - 10))
        end = min(start + 10, max_num)
        sequence = list(range(start, end + 1))
        missing_index = random.randint(0, len(sequence) - 1)
        missing_number = sequence[missing_index]
        sequence[missing_index] = None
        problem.update({
            "sequence": sequence,
            "format": "missing_number",
            "answer": missing_number
        })
    else:
        # Default to comparison
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        symbol = "<" if a < b else ">" if a > b else "="
        problem.update({
            "first_number": a,
            "second_number": b,
            "format": "comparison",
            "answer": symbol
        })

    return problem

def generate_time_problem(subcategory: str) -> Dict[str, Any]:
    """Generate time-telling problems based on subcategory"""
    problem = {
        "category": "time_telling",
        "subcategory": subcategory,
        "format": "clock"
    }

    # Generate a random hour between 1 and 12
    hour = random.randint(1, 12)

    if subcategory == "whole_hours":
        minute = 0
        hour_angle = (hour % 12) * 30
        minute_angle = 0
        time_str = f"{hour}:00"
    elif subcategory == "half_hours":
        minute = 30
        hour_angle = (hour % 12) * 30 + 15  # Hour hand moves halfway
        minute_angle = 180
        time_str = f"{hour}:30"
    elif subcategory == "quarter_hours":
        is_quarter_past = random.choice([True, False])
        minute = 15 if is_quarter_past else 45
        hour_angle = (hour % 12) * 30 + (7.5 if is_quarter_past else 22.5)
        minute_angle = 90 if is_quarter_past else 270
        time_str = f"{hour}:{minute}"
    elif subcategory == "five_minute_increments":
        # Generate random minutes in 5-minute increments
        minute = random.randint(0, 11) * 5
        hour_angle = (hour % 12) * 30 + (minute / 60) * 30
        minute_angle = (minute / 60) * 360
        time_str = f"{hour}:{minute:02d}"
    else:
        # Default to whole hours
        minute = 0
        hour_angle = (hour % 12) * 30
        minute_angle = 0
        time_str = f"{hour}:00"

    problem.update({
        "hour": hour,
        "minute": minute,
        "hour_angle": hour_angle,
        "minute_angle": minute_angle,
        "time_string": time_str,
        "answer": time_str
    })

    return problem

def generate_money_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate money counting problems based on subcategory"""
    problem = {
        "category": "money_counting",
        "subcategory": subcategory,
        "format": "money"
    }

    if subcategory == "identifying_coins":
        coins = ["penny", "nickel", "dime", "quarter"]
        coin = random.choice(coins)
        value = {"penny": 1, "nickel": 5, "dime": 10, "quarter": 25}[coin]
        problem.update({
            "coin": coin,
            "value": value,
            "answer": coin
        })
    elif subcategory == "counting_pennies_nickels":
        penny_count = random.randint(0, 9)
        nickel_count = random.randint(0, 5)
        total_value = penny_count + nickel_count * 5
        problem.update({
            "pennies": penny_count,
            "nickels": nickel_count,
            "value": total_value,
            "answer": total_value
        })
    elif subcategory == "mixed_coins":
        # Generate random counts for different coins
        penny_count = random.randint(0, 5)
        nickel_count = random.randint(0, 3)
        dime_count = random.randint(0, 2)

        # Calculate total value
        total_value = penny_count + nickel_count * 5 + dime_count * 10

        # Ensure value is within range
        if max_num < 100:
            total_value = min(total_value, max_num)

        problem.update({
            "pennies": penny_count,
            "nickels": nickel_count,
            "dimes": dime_count,
            "quarters": 0,
            "value": total_value,
            "answer": total_value
        })
    elif subcategory == "making_change":
        # Generate a purchase amount and payment amount
        purchase_amount = random.randint(5, min(95, max_num))
        payment_amount = random.randint(purchase_amount, min(100, max_num))
        change = payment_amount - purchase_amount

        problem.update({
            "purchase_amount": purchase_amount,
            "payment_amount": payment_amount,
            "change": change,
            "answer": change
        })
    else:
        # Default to identifying coins
        coins = ["penny", "nickel", "dime", "quarter"]
        coin = random.choice(coins)
        value = {"penny": 1, "nickel": 5, "dime": 10, "quarter": 25}[coin]
        problem.update({
            "coin": coin,
            "value": value,
            "answer": coin
        })

    return problem

def generate_place_value_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate place value problems based on subcategory"""
    problem = {
        "category": "place_value",
        "subcategory": subcategory,
        "format": "place_value"
    }

    if subcategory == "ones_tens":
        # Generate a two-digit number
        number = random.randint(10, min(99, max_num))
        ones = number % 10
        tens = number // 10

        problem.update({
            "number": number,
            "ones": ones,
            "tens": tens,
            "answer": {"ones": ones, "tens": tens}
        })
    elif subcategory == "ones_tens_hundreds":
        # Generate a three-digit number
        number = random.randint(100, min(999, max_num))
        ones = number % 10
        tens = (number // 10) % 10
        hundreds = number // 100

        problem.update({
            "number": number,
            "ones": ones,
            "tens": tens,
            "hundreds": hundreds,
            "answer": {"ones": ones, "tens": tens, "hundreds": hundreds}
        })
    elif subcategory == "expanded_form":
        if max_num <= 9:
            number = random.randint(1, max_num)
            expanded = f"{number}"
            answer = expanded
        elif max_num <= 99:
            number = random.randint(10, max_num)
            tens = (number // 10) * 10
            ones = number % 10
            expanded = f"{tens} + {ones}" if ones > 0 else f"{tens}"
            answer = expanded
        else:
            number = random.randint(100, max_num)
            hundreds = (number // 100) * 100
            tens = ((number // 10) % 10) * 10
            ones = number % 10

            parts = []
            if hundreds > 0:
                parts.append(f"{hundreds}")
            if tens > 0:
                parts.append(f"{tens}")
            if ones > 0:
                parts.append(f"{ones}")

            expanded = " + ".join(parts)
            answer = expanded

        problem.update({
            "number": number,
            "expanded_form": expanded,
            "answer": answer
        })
    else:
        # Default to ones_tens
        number = random.randint(10, min(99, max_num))
        ones = number % 10
        tens = number // 10

        problem.update({
            "number": number,
            "ones": ones,
            "tens": tens,
            "answer": {"ones": ones, "tens": tens}
        })

    return problem

def generate_word_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate word problems based on subcategory"""
    problem = {
        "category": "word_problems",
        "subcategory": subcategory,
        "format": "word_problem"
    }

    if subcategory == "one_step":
        # Generate a simple one-step addition or subtraction problem
        operation = random.choice(["addition", "subtraction"])

        if operation == "addition":
            a = random.randint(1, min(max_num // 2, 10))
            b = random.randint(1, min(max_num - a, 10))

            objects = random.choice(["apples", "books", "pencils", "stickers", "toys"])

            problem_text = f"Sam has {a} {objects}. Pat gives Sam {b} more {objects}. How many {objects} does Sam have now?"

            problem.update({
                "text": problem_text,
                "operation": "addition",
                "first_number": a,
                "second_number": b,
                "answer": a + b
            })
        else:
            a = random.randint(5, min(max_num, 20))
            b = random.randint(1, min(a - 1, 10))

            objects = random.choice(["apples", "books", "pencils", "stickers", "toys"])

            problem_text = f"Sam has {a} {objects}. Sam gives {b} {objects} to Pat. How many {objects} does Sam have left?"

            problem.update({
                "text": problem_text,
                "operation": "subtraction",
                "first_number": a,
                "second_number": b,
                "answer": a - b
            })
    elif subcategory == "two_step":
        # Generate a two-step problem involving addition and subtraction
        a = random.randint(5, min(max_num // 2, 20))
        b = random.randint(1, min(max_num - a, 10))
        c = random.randint(1, min(a + b - 1, 10))

        objects = random.choice(["apples", "books", "pencils", "stickers", "toys"])

        problem_text = (
            f"Sam has {a} {objects}. Pat gives Sam {b} more {objects}. "
            f"Then Sam gives {c} {objects} to Alex. How many {objects} does Sam have now?"
        )

        problem.update({
            "text": problem_text,
            "operations": ["addition", "subtraction"],
            "first_number": a,
            "second_number": b,
            "third_number": c,
            "answer": a + b - c
        })
    elif subcategory == "multi_step":
        # Generate a multi-step problem with mixed operations
        a = random.randint(10, min(max_num // 3, 30))
        b = random.randint(5, min(max_num // 3, 15))
        c = random.randint(2, 5)
        d = random.randint(1, min(a + b*c - 1, 10))

        objects = random.choice(["apples", "books", "pencils", "stickers", "toys"])

        problem_text = (
            f"Sam has {a} {objects}. Sam buys {b} packs with {c} {objects} in each pack. "
            f"Then Sam gives {d} {objects} to friends. How many {objects} does Sam have now?"
        )

        problem.update({
            "text": problem_text,
            "operations": ["addition", "multiplication", "subtraction"],
            "first_number": a,
            "second_number": b,
            "third_number": c,
            "fourth_number": d,
            "answer": a + (b * c) - d
        })
    else:
        # Default to one-step addition
        a = random.randint(1, min(max_num // 2, 10))
        b = random.randint(1, min(max_num - a, 10))

        objects = random.choice(["apples", "books", "pencils", "stickers", "toys"])

        problem_text = f"Sam has {a} {objects}. Pat gives Sam {b} more {objects}. How many {objects} does Sam have now?"

        problem.update({
            "text": problem_text,
            "operation": "addition",
            "first_number": a,
            "second_number": b,
            "answer": a + b
        })

    return problem

def generate_shapes_problem(subcategory: str) -> Dict[str, Any]:
    """Generate shape problems based on subcategory"""
    problem = {
        "category": "shapes",
        "subcategory": subcategory,
        "format": "shapes"
    }

    if subcategory == "basic_2d_3d":
        # Choose between 2D and 3D shapes
        is_2d = random.choice([True, False])

        if is_2d:
            shapes = ["circle", "square", "triangle", "rectangle", "oval", "diamond"]
            shape = random.choice(shapes)

            problem.update({
                "dimension": "2D",
                "shape": shape,
                "answer": shape
            })
        else:
            shapes = ["cube", "sphere", "cylinder", "cone", "pyramid"]
            shape = random.choice(shapes)

            problem.update({
                "dimension": "3D",
                "shape": shape,
                "answer": shape
            })
    elif subcategory == "edges_faces_vertices":
        # 3D shapes with their properties
        shapes = [
            {"name": "cube", "faces": 6, "edges": 12, "vertices": 8},
            {"name": "rectangular prism", "faces": 6, "edges": 12, "vertices": 8},
            {"name": "triangular prism", "faces": 5, "edges": 9, "vertices": 6},
            {"name": "pyramid", "faces": 5, "edges": 8, "vertices": 5},
        ]

        shape = random.choice(shapes)
        question_type = random.choice(["faces", "edges", "vertices"])

        problem.update({
            "shape": shape["name"],
            "question_type": question_type,
            "answer": shape[question_type]
        })
    else:
        # Default to basic 2D shapes
        shapes = ["circle", "square", "triangle", "rectangle"]
        shape = random.choice(shapes)

        problem.update({
            "dimension": "2D",
            "shape": shape,
            "answer": shape
        })

    return problem

def generate_skip_counting_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate skip counting problems based on subcategory"""
    problem = {
        "category": "skip_counting",
        "subcategory": subcategory,
        "format": "skip_counting"
    }

    if subcategory == "by_ones_twos":
        # Skip counting by 1s or 2s
        skip_by = random.choice([1, 2])
        start = random.randint(0, min(20, max_num // 2))

        # Generate sequence with skip_by increment
        sequence = [start + i * skip_by for i in range(6)]

        # Choose a position to make missing
        missing_pos = random.randint(1, 4)
        missing_number = sequence[missing_pos]
        sequence[missing_pos] = None

        problem.update({
            "skip_by": skip_by,
            "sequence": sequence,
            "missing_position": missing_pos,
            "answer": missing_number
        })
    elif subcategory == "by_fives_tens":
        # Skip counting by 5s or 10s
        skip_by = random.choice([5, 10])
        start = random.randint(0, min(50, max_num // 2))

        # Ensure start is a multiple of skip_by for cleaner sequences
        start = (start // skip_by) * skip_by

        # Generate sequence with skip_by increment
        sequence = [start + i * skip_by for i in range(6)]

        # Choose a position to make missing
        missing_pos = random.randint(1, 4)
        missing_number = sequence[missing_pos]
        sequence[missing_pos] = None

        problem.update({
            "skip_by": skip_by,
            "sequence": sequence,
            "missing_position": missing_pos,
            "answer": missing_number
        })
    elif subcategory == "by_hundreds":
        # Skip counting by 100s
        skip_by = 100
        start = random.randint(0, min(500, max_num - 500))

        # Ensure start is a multiple of 100 for cleaner sequences
        start = (start // 100) * 100

        # Generate sequence with skip_by increment
        sequence = [start + i * skip_by for i in range(6)]

        # Choose a position to make missing
        missing_pos = random.randint(1, 4)
        missing_number = sequence[missing_pos]
        sequence[missing_pos] = None

        problem.update({
            "skip_by": skip_by,
            "sequence": sequence,
            "missing_position": missing_pos,
            "answer": missing_number
        })
    else:
        # Default to counting by 5s
        skip_by = 5
        start = random.randint(0, min(50, max_num // 2))
        start = (start // skip_by) * skip_by

        sequence = [start + i * skip_by for i in range(6)]
        missing_pos = random.randint(1, 4)
        missing_number = sequence[missing_pos]
        sequence[missing_pos] = None

        problem.update({
            "skip_by": skip_by,
            "sequence": sequence,
            "missing_position": missing_pos,
            "answer": missing_number
        })

    return problem

def generate_fraction_problem(subcategory: str) -> Dict[str, Any]:
    """Generate fraction problems based on subcategory"""
    problem = {
        "category": "fractions",
        "subcategory": subcategory,
        "format": "fractions"
    }

    if subcategory == "halves_wholes":
        # Generate problems about halves and wholes
        shapes = ["circle", "rectangle", "square"]
        shape = random.choice(shapes)

        is_half = random.choice([True, False])
        fraction = "1/2" if is_half else "1"

        problem.update({
            "shape": shape,
            "shaded_fraction": fraction,
            "answer": fraction
        })
    elif subcategory == "thirds_fourths":
        # Generate problems about thirds and fourths
        shapes = ["circle", "rectangle", "square"]
        shape = random.choice(shapes)

        denominator = random.choice([3, 4])
        numerator = random.randint(1, denominator)
        fraction = f"{numerator}/{denominator}"

        problem.update({
            "shape": shape,
            "shaded_fraction": fraction,
            "answer": fraction
        })
    elif subcategory == "comparing_fractions":
        # Generate fraction comparison problems
        denominators = [2, 3, 4, 6, 8]

        # Choose two denominators (can be the same)
        denom1 = random.choice(denominators)
        denom2 = random.choice(denominators)

        # Choose numerators
        num1 = random.randint(1, denom1)
        num2 = random.randint(1, denom2)

        # Calculate decimal values for comparison
        val1 = num1 / denom1
        val2 = num2 / denom2

        if val1 < val2:
            symbol = "<"
        elif val1 > val2:
            symbol = ">"
        else:
            symbol = "="

        problem.update({
            "fraction1": f"{num1}/{denom1}",
            "fraction2": f"{num2}/{denom2}",
            "answer": symbol
        })
    else:
        # Default to halves
        shapes = ["circle", "rectangle", "square"]
        shape = random.choice(shapes)

        is_half = random.choice([True, False])
        fraction = "1/2" if is_half else "1"

        problem.update({
            "shape": shape,
            "shaded_fraction": fraction,
            "answer": fraction
        })

    return problem

def generate_measurement_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate measurement problems based on subcategory"""
    problem = {
        "category": "measurement",
        "subcategory": subcategory,
        "format": "measurement"
    }

    if subcategory == "comparing_objects":
        # Generate problems comparing object sizes
        comparisons = ["taller/shorter", "longer/shorter", "heavier/lighter", "larger/smaller"]
        comparison = random.choice(comparisons)

        if comparison == "taller/shorter":
            objects = [("tree", 8), ("house", 5), ("person", 2), ("flower", 1)]
        elif comparison == "longer/shorter":
            objects = [("snake", 7), ("pencil", 3), ("crayon", 2), ("eraser", 1)]
        elif comparison == "heavier/lighter":
            objects = [("elephant", 9), ("dog", 5), ("book", 2), ("feather", 1)]
        else:  # larger/smaller
            objects = [("ball", 6), ("marble", 2), ("penny", 1), ("beach ball", 8)]

        # Choose two different objects
        obj1, val1 = random.choice(objects)
        obj2, val2 = None, None

        while obj2 is None or obj1 == obj2:
            obj2, val2 = random.choice(objects)

        # Determine the comparison relation
        if comparison == "taller/shorter":
            relation = "taller than" if val1 > val2 else "shorter than"
        elif comparison == "longer/shorter":
            relation = "longer than" if val1 > val2 else "shorter than"
        elif comparison == "heavier/lighter":
            relation = "heavier than" if val1 > val2 else "lighter than"
        else:  # larger/smaller
            relation = "larger than" if val1 > val2 else "smaller than"

        problem.update({
            "object1": obj1,
            "object2": obj2,
            "relation": relation,
            "answer": relation
        })
    elif subcategory == "non_standard_units":
        # Generate measurement with non-standard units
        objects = ["crayon", "paper clip", "pencil", "eraser", "book"]
        measuring_object = random.choice(objects)

        # Length in units (keep it small)
        length = random.randint(2, min(10, max_num))

        items = ["desk", "notebook", "folder", "tablet", "book"]
        item = random.choice(items)

        problem.update({
            "measuring_object": measuring_object,
            "item_to_measure": item,
            "length": length,
            "answer": length
        })
    elif subcategory == "rulers_inches_cm":
        # Generate ruler measurement problems
        unit = random.choice(["inches", "centimeters"])

        if unit == "inches":
            # Generate a length in inches (up to 12 inches)
            whole = random.randint(1, min(12, max_num))
            fraction = random.choice([0, 0.25, 0.5, 0.75])
            length = whole + fraction

            display_length = f"{whole}" if fraction == 0 else f"{whole} {fraction}/1"
            if fraction == 0.25:
                display_length = f"{whole} 1/4"
            elif fraction == 0.5:
                display_length = f"{whole} 1/2"
            elif fraction == 0.75:
                display_length = f"{whole} 3/4"
        else:
            # Generate a length in centimeters (up to 30 cm)
            length = random.randint(1, min(30, max_num))
            display_length = f"{length}"

        problem.update({
            "unit": unit,
            "length": length,
            "display_length": display_length,
            "answer": display_length
        })
    else:
        # Default to comparing objects
        objects = [("ball", 6), ("marble", 2)]
        obj1, val1 = objects[0]
        obj2, val2 = objects[1]

        relation = "larger than" if val1 > val2 else "smaller than"

        problem.update({
            "object1": obj1,
            "object2": obj2,
            "relation": relation,
            "answer": relation
        })

    return problem

def generate_pattern_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate pattern problems based on subcategory"""
    problem = {
        "category": "patterns",
        "subcategory": subcategory,
        "format": "patterns"
    }

    if subcategory == "abab_patterns":
        # Generate simple alternating patterns
        pattern_types = ["shape", "color", "number"]
        pattern_type = random.choice(pattern_types)

        if pattern_type == "shape":
            items = ["circle", "square", "triangle", "star"]
            a = random.choice(items)
            b = random.choice([i for i in items if i != a])

            pattern = [a, b, a, b, a]
            answer = b
        elif pattern_type == "color":
            items = ["red", "blue", "green", "yellow"]
            a = random.choice(items)
            b = random.choice([i for i in items if i != a])

            pattern = [a, b, a, b, a]
            answer = b
        else:  # number
            a = random.randint(1, min(5, max_num))
            b = random.randint(1, min(5, max_num))
            while b == a:
                b = random.randint(1, min(5, max_num))

            pattern = [a, b, a, b, a]
            answer = b

        problem.update({
            "pattern_type": pattern_type,
            "pattern": pattern,
            "answer": answer
        })
    elif subcategory == "extending_patterns":
        # Generate patterns with a rule to extend
        pattern_types = ["adding", "subtracting", "multiplying"]
        pattern_type = random.choice(pattern_types)

        if pattern_type == "adding":
            start = random.randint(1, min(10, max_num // 5))
            increment = random.randint(1, min(5, max_num // 5))

            pattern = [start + i * increment for i in range(5)]
            next_value = start + 5 * increment

            problem.update({
                "rule": f"Add {increment}",
                "pattern": pattern,
                "answer": next_value
            })
        elif pattern_type == "subtracting":
            start = random.randint(max(6, max_num // 2), max_num)
            decrement = random.randint(1, min(5, start // 5))

            pattern = [start - i * decrement for i in range(5)]
            next_value = start - 5 * decrement

            problem.update({
                "rule": f"Subtract {decrement}",
                "pattern": pattern,
                "answer": next_value
            })
        else:  # multiplying
            start = random.randint(1, min(3, max_num // 32))
            multiplier = random.randint(2, min(3, int(math.sqrt(max_num))))

            pattern = [start * (multiplier ** i) for i in range(5)]
            next_value = start * (multiplier ** 5)

            problem.update({
                "rule": f"Multiply by {multiplier}",
                "pattern": pattern,
                "answer": next_value
            })
    elif subcategory == "creating_patterns":
        # Generate patterns with missing elements
        start = random.randint(1, min(10, max_num // 5))
        increment = random.randint(1, min(5, max_num // 5))

        # Create a pattern with addition
        full_pattern = [start + i * increment for i in range(6)]

        # Remove 1-2 elements
        missing_positions = random.sample(range(1, 5), 2)
        missing_values = [full_pattern[pos] for pos in missing_positions]

        for pos in missing_positions:
            full_pattern[pos] = None

        problem.update({
            "pattern": full_pattern,
            "missing_positions": missing_positions,
            "answer": missing_values
        })
    else:
        # Default to simple alternating pattern
        a = random.randint(1, min(5, max_num))
        b = random.randint(1, min(5, max_num))
        while b == a:
            b = random.randint(1, min(5, max_num))

        pattern = [a, b, a, b, a]
        answer = b

        problem.update({
            "pattern_type": "number",
            "pattern": pattern,
            "answer": answer
        })

    return problem

def generate_graphing_problem(subcategory: str) -> Dict[str, Any]:
    """Generate graphing and data analysis problems based on subcategory"""
    problem = {
        "category": "graphing",
        "subcategory": subcategory,
        "format": "graphing"
    }

    if subcategory == "pictographs":
        # Generate simple pictograph problems
        categories = ["apples", "books", "toys", "pencils", "balls"]
        selected_categories = random.sample(categories, 3)

        # Generate counts for each category (1-5)
        counts = [random.randint(1, 5) for _ in range(3)]

        # Create questions about the data
        question_types = ["most", "least", "total", "difference"]
        question_type = random.choice(question_types)

        if question_type == "most":
            max_index = counts.index(max(counts))
            answer = selected_categories[max_index]
            question = f"Which has the most?"
        elif question_type == "least":
            min_index = counts.index(min(counts))
            answer = selected_categories[min_index]
            question = f"Which has the least?"
        elif question_type == "total":
            total = sum(counts)
            answer = total
            question = f"What is the total number?"
        else:  # difference
            max_count = max(counts)
            min_count = min(counts)
            answer = max_count - min_count
            max_index = counts.index(max_count)
            min_index = counts.index(min_count)
            question = f"What is the difference between {selected_categories[max_index]} and {selected_categories[min_index]}?"

        problem.update({
            "categories": selected_categories,
            "counts": counts,
            "question": question,
            "question_type": question_type,
            "answer": answer
        })
    elif subcategory == "bar_graphs":
        # Generate bar graph problems
        categories = ["apples", "oranges", "bananas", "grapes", "strawberries"]
        selected_categories = random.sample(categories, 4)

        # Generate counts for each category (1-10)
        counts = [random.randint(1, 10) for _ in range(4)]

        # Create questions about the data
        question_types = ["most", "least", "total", "difference", "sum_two"]
        question_type = random.choice(question_types)

        if question_type == "most":
            max_index = counts.index(max(counts))
            answer = selected_categories[max_index]
            question = f"Which fruit has the most?"
        elif question_type == "least":
            min_index = counts.index(min(counts))
            answer = selected_categories[min_index]
            question = f"Which fruit has the least?"
        elif question_type == "total":
            total = sum(counts)
            answer = total
            question = f"What is the total number of fruits?"
        elif question_type == "difference":
            max_count = max(counts)
            min_count = min(counts)
            answer = max_count - min_count
            max_index = counts.index(max_count)
            min_index = counts.index(min_count)
            question = f"What is the difference between {selected_categories[max_index]} and {selected_categories[min_index]}?"
        else:  # sum_two
            indices = random.sample(range(4), 2)
            cat1 = selected_categories[indices[0]]
            cat2 = selected_categories[indices[1]]
            answer = counts[indices[0]] + counts[indices[1]]
            question = f"What is the sum of {cat1} and {cat2}?"

        problem.update({
            "categories": selected_categories,
            "counts": counts,
            "question": question,
            "question_type": question_type,
            "answer": answer
        })
    elif subcategory == "analyzing_data":
        # Generate data analysis problems with more complex questions
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        selected_days = random.sample(days, 5)

        # Generate data points (e.g., temperature, steps, etc.)
        data_type = random.choice(["temperature", "steps", "books"])

        if data_type == "temperature":
            data_points = [random.randint(60, 90) for _ in range(5)]
            unit = "degrees"
        elif data_type == "steps":
            data_points = [random.randint(1000, 10000) for _ in range(5)]
            unit = "steps"
        else:  # books
            data_points = [random.randint(1, 5) for _ in range(5)]
            unit = "books"

        # Create more complex analysis questions
        question_types = ["highest", "lowest", "average", "range", "mode"]
        question_type = random.choice(question_types)

        if question_type == "highest":
            max_index = data_points.index(max(data_points))
            answer = selected_days[max_index]
            question = f"On which day was the {data_type} highest?"
        elif question_type == "lowest":
            min_index = data_points.index(min(data_points))
            answer = selected_days[min_index]
            question = f"On which day was the {data_type} lowest?"
        elif question_type == "average":
            avg = sum(data_points) / len(data_points)
            answer = round(avg, 1)
            question = f"What was the average {data_type} for the week?"
        elif question_type == "range":
            data_range = max(data_points) - min(data_points)
            answer = data_range
            question = f"What is the range of the {data_type}?"
        else:  # mode
            # Ensure there is a mode by duplicating one value
            mode_index = random.randint(0, 4)
            dup_index = random.randint(0, 4)
            while dup_index == mode_index:
                dup_index = random.randint(0, 4)

            data_points[dup_index] = data_points[mode_index]
            mode_value = data_points[mode_index]

            answer = mode_value
            question = f"What is the mode of the {data_type}?"

        problem.update({
            "data_type": data_type,
            "days": selected_days,
            "data_points": data_points,
            "unit": unit,
            "question": question,
            "question_type": question_type,
            "answer": answer
        })
    else:
        # Default to simple pictograph
        categories = ["apples", "books", "toys"]
        counts = [random.randint(1, 5) for _ in range(3)]

        max_index = counts.index(max(counts))
        answer = categories[max_index]
        question = "Which has the most?"

        problem.update({
            "categories": categories,
            "counts": counts,
            "question": question,
            "question_type": "most",
            "answer": answer
        })

    return problem

def generate_odd_even_problem(subcategory: str, max_num: int) -> Dict[str, Any]:
    """Generate odd/even number problems based on subcategory"""
    problem = {
        "category": "odd_even",
        "subcategory": subcategory,
        "format": "odd_even"
    }

    if subcategory == "identifying":
        # Generate a number and ask if it's odd or even
        number = random.randint(1, min(20, max_num))

        is_even = number % 2 == 0
        answer = "even" if is_even else "odd"

        problem.update({
            "number": number,
            "question": f"Is {number} odd or even?",
            "answer": answer
        })
    elif subcategory == "sorting":
        # Generate a set of numbers to sort into odd and even
        count = random.randint(4, 6)
        numbers = random.sample(range(1, min(20, max_num) + 1), count)

        odd_numbers = [n for n in numbers if n % 2 == 1]
        even_numbers = [n for n in numbers if n % 2 == 0]

        problem.update({
            "numbers": numbers,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "answer": {"odd": odd_numbers, "even": even_numbers}
        })
    elif subcategory == "problem_solving":
        # Generate a problem-solving question using odd/even concepts
        problem_types = ["next_even", "next_odd", "sum_type"]
        problem_type = random.choice(problem_types)

        if problem_type == "next_even":
            start = random.randint(1, min(20, max_num))
            next_even = start + (2 - (start % 2)) % 2

            problem.update({
                "start_number": start,
                "question": f"What is the next even number after {start}?",
                "answer": next_even
            })
        elif problem_type == "next_odd":
            start = random.randint(1, min(20, max_num))
            next_odd = start + (1 + (start % 2)) % 2

            problem.update({
                "start_number": start,
                "question": f"What is the next odd number after {start}?",
                "answer": next_odd
            })
        else:  # sum_type
            num1 = random.randint(1, min(10, max_num // 2))
            num2 = random.randint(1, min(10, max_num // 2))

            sum_val = num1 + num2
            is_even = sum_val % 2 == 0
            answer = "even" if is_even else "odd"

            problem.update({
                "first_number": num1,
                "second_number": num2,
                "sum": sum_val,
                "question": f"Is the sum of {num1} and {num2} odd or even?",
                "answer": answer
            })
    else:
        # Default to identifying odd/even
        number = random.randint(1, min(20, max_num))

        is_even = number % 2 == 0
        answer = "even" if is_even else "odd"

        problem.update({
            "number": number,
            "question": f"Is {number} odd or even?",
            "answer": answer
        })

    return problem