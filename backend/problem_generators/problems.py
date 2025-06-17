# problem_generators/problems.py

from typing import List, Dict, Any, Optional
import random
import json
import os
import logging

# Import problem generators
from .addition import AdditionProblemGenerator
from .subtraction import SubtractionProblemGenerator
from .number_sense import NumberSenseProblemGenerator
from .time_telling import TimeTellingProblemGenerator
from .money_counting import MoneyCountingProblemGenerator
from .place_value import PlaceValueProblemGenerator
from .word_problems import WordProblemGenerator
from .shapes import ShapesProblemGenerator
from .skip_counting import SkipCountingProblemGenerator
from .fractions import FractionsProblemGenerator
from .measurement import MeasurementProblemGenerator
from .patterns import PatternsProblemGenerator
from .graphing import GraphingProblemGenerator
from .odd_even import OddEvenProblemGenerator

# Create instances of all problem generators
_generators = {
    "addition": AdditionProblemGenerator(),
    "subtraction": SubtractionProblemGenerator(),
    "number_sense": NumberSenseProblemGenerator(),
    "time_telling": TimeTellingProblemGenerator(),
    "money_counting": MoneyCountingProblemGenerator(),
    "place_value": PlaceValueProblemGenerator(),
    "word_problems": WordProblemGenerator(),
    "shapes": ShapesProblemGenerator(),
    "skip_counting": SkipCountingProblemGenerator(),
    "fractions": FractionsProblemGenerator(),
    "measurement": MeasurementProblemGenerator(),
    "patterns": PatternsProblemGenerator(),
    "graphing": GraphingProblemGenerator(),
    "odd_even": OddEvenProblemGenerator()
}

# Map of subconcepts to their categories
_subconcept_to_category = {
    # Number Sense
    "subitizing": "number_sense",
    "comparison": "number_sense",
    "ordering": "number_sense",
    "before_after": "number_sense",
    "missing_numbers": "number_sense",
    
    # Addition
    "add_zero": "addition",
    "add_one": "addition",
    "same_number_addition": "addition",
    "near_doubles": "addition",
    
    # Subtraction
    "subtract_zero": "subtraction",
    "subtract_one": "subtraction",
    "same_number_subtraction": "subtraction",
    "near_doubles_subtraction": "subtraction",
    
    # Time Telling
    "whole_hours": "time_telling",
    "half_hours": "time_telling",
    "quarter_hours": "time_telling",
    "five_minute_increments": "time_telling",
    
    # Money Counting
    "identifying_coins": "money_counting",
    "counting_pennies_nickels": "money_counting",
    "mixed_coins": "money_counting",
    "making_change": "money_counting",
    
    # Place Value
    "ones_tens": "place_value",
    "ones_tens_hundreds": "place_value",
    "expanded_form": "place_value",
    
    # Word Problems
    "one_step": "word_problems",
    "two_step": "word_problems",
    "multi_step": "word_problems",
    
    # Shapes
    "basic_2d_3d": "shapes",
    "edges_faces_vertices": "shapes",
    
    # Skip Counting
    "by_ones_twos": "skip_counting",
    "by_fives_tens": "skip_counting",
    "by_hundreds": "skip_counting",
    
    # Fractions
    "halves_wholes": "fractions",
    "thirds_fourths": "fractions",
    "comparing_fractions": "fractions",
    
    # Measurement
    "comparing_objects": "measurement",
    "non_standard_units": "measurement",
    "rulers_inches_cm": "measurement",
    
    # Patterns & Algebra
    "abab_patterns": "patterns",
    "extending_patterns": "patterns",
    "creating_patterns": "patterns",
    
    # Graphing & Data
    "pictographs": "graphing",
    "bar_graphs": "graphing",
    "analyzing_data": "graphing",
    
    # Odd & Even Numbers
    "identifying": "odd_even",
    "sorting": "odd_even",
    "problem_solving": "odd_even"
}


# def generate_problems(
#     worksheet_type: str,
#     number_range: str,
#     concepts: List[str],
#     problem_count: Optional[int] = None
# ) -> List[Dict[str, Any]]:
#     """
#     Generate problems for a worksheet based on specified parameters.
    
#     Args:
#         worksheet_type: "spiral" or "fluency"
#         number_range: "beginner", "intermediate", or "advanced"
#         concepts: List of concept identifiers
#         problem_count: Number of problems for fluency worksheets (default: 15)
        
#     Returns:
#         List of problem dictionaries containing question, answer, and display info
#     """
#     all_problems = []
    
#     # For fluency sheets: single concept, multiple problems
#     if worksheet_type == "fluency":
#         # Make sure we have at least one concept
#         if not concepts:
#             return []
            
#         # Get the first concept (fluency focuses on one concept)
#         concept = concepts[0]
        
#         # Determine which category this concept belongs to
#         category = _subconcept_to_category.get(concept)
#         if not category:
#             return []
        
#         # Get the corresponding problem generator
#         generator = _generators.get(category)
#         if not generator:
#             return []
        
#         # Generate multiple problems of the same concept
#         count = problem_count if problem_count is not None else 15
        
#         for _ in range(count):
#             try:
#                 # Generate a problem with the specified subcategory
#                 problem = generator.generate_problem(number_range, concept)
                
#                 # Add metadata to the problem
#                 problem["category"] = category
#                 problem["subcategory"] = concept
                
#                 all_problems.append(problem)
#             except Exception as e:
#                 print(f"Error generating {concept} problem: {str(e)}")
    
#     # For spiral review: multiple concepts, one problem each
#     else:  # worksheet_type == "spiral"
#         # Track subcategories we've already generated
#         used_subcategories = set()
        
#         for concept in concepts:
#             # Check if this is a category name instead of a subcategory
#             if concept in _generators:
#                 # This is a main category (like "addition"), generate one problem for each subcategory
#                 category = concept
#                 generator = _generators[category]
                
#                 # Find all subcategories for this category
#                 subcategories = [subcat for subcat, cat in _subconcept_to_category.items() if cat == category]
                
#                 # Generate one problem for each subcategory
#                 for subcategory in subcategories:
#                     if subcategory not in used_subcategories:  # Avoid duplicates
#                         try:
#                             problem = generator.generate_problem(number_range, subcategory)
#                             problem["category"] = category
#                             problem["subcategory"] = subcategory
#                             all_problems.append(problem)
#                             used_subcategories.add(subcategory)
#                         except Exception as e:
#                             print(f"Error generating {subcategory} problem: {str(e)}")
#             else:
#                 # This is a specific subcategory (like "add_one")
#                 category = _subconcept_to_category.get(concept)
#                 if not category:
#                     continue
                
#                 # Get the generator for this category
#                 generator = _generators.get(category)
#                 if not generator:
#                     continue
                
#                 if concept not in used_subcategories:  # Avoid duplicates
#                     try:
#                         # Generate one problem of this concept
#                         problem = generator.generate_problem(number_range, concept)
                        
#                         # Add metadata to the problem
#                         problem["category"] = category
#                         problem["subcategory"] = concept
                        
#                         all_problems.append(problem)
#                         used_subcategories.add(concept)
#                     except Exception as e:
#                         print(f"Error generating {concept} problem: {str(e)}")

#     print(f"Generated {len(all_problems)} problems:")
#     for i, problem in enumerate(all_problems):
#         print(f"  Problem {i+1}: {problem.get('category', 'unknown')} - {problem.get('subcategory', 'unknown')}")
    
#     return all_problems

def generate_problems(
    worksheet_type: str,
    number_range: str,
    concepts: List[str],
    problem_count: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Generate problems for a worksheet based on specified parameters.
    
    Args:
        worksheet_type: "spiral" or "fluency"
        number_range: "beginner", "intermediate", or "advanced"
        concepts: List of concept identifiers
        problem_count: Number of problems for fluency worksheets (default: 15)
        
    Returns:
        List of problem dictionaries containing question, answer, and display info
    """
    all_problems = []
    
    # For fluency sheets: single concept, multiple problems
    if worksheet_type == "fluency":
        # Make sure we have at least one concept
        if not concepts:
            return []
            
        # Get the first concept (fluency focuses on one concept)
        concept = concepts[0]
        
        # Determine which category this concept belongs to
        category = _subconcept_to_category.get(concept)
        if not category:
            return []
        
        # Get the corresponding problem generator
        generator = _generators.get(category)
        if not generator:
            return []
        
        # Generate multiple problems of the same concept
        count = problem_count if problem_count is not None else 15
        
        for _ in range(count):
            try:
                # Generate a problem with the specified subcategory
                problem = generator.generate_problem(number_range, concept)
                
                # Add metadata to the problem
                problem["category"] = category
                problem["subcategory"] = concept
                
                all_problems.append(problem)
            except Exception as e:
                print(f"Error generating {concept} problem: {str(e)}")
    
    # For spiral review: multiple concepts, one problem each
    else:  # worksheet_type == "spiral"
        # Track subcategories we've already generated
        used_subcategories = set()
        
        for concept in concepts:
            # Check if this is a category name instead of a subcategory
            if concept in _generators:
                # This is a main category (like "addition"), generate one problem for each subcategory
                category = concept
                generator = _generators[category]
                
                # Find all subcategories for this category
                subcategories = [subcat for subcat, cat in _subconcept_to_category.items() if cat == category]
                
                # Generate one problem for each subcategory
                for subcategory in subcategories:
                    if subcategory not in used_subcategories:  # Avoid duplicates
                        try:
                            problem = generator.generate_problem(number_range, subcategory)
                            problem["category"] = category
                            problem["subcategory"] = subcategory
                            all_problems.append(problem)
                            used_subcategories.add(subcategory)
                        except Exception as e:
                            print(f"Error generating {subcategory} problem: {str(e)}")
            else:
                # This is a specific subcategory (like "add_one")
                category = _subconcept_to_category.get(concept)
                if not category:
                    continue
                
                # Get the generator for this category
                generator = _generators.get(category)
                if not generator:
                    continue
                
                if concept not in used_subcategories:  # Avoid duplicates
                    try:
                        # Generate one problem of this concept
                        problem = generator.generate_problem(number_range, concept)
                        
                        # Add metadata to the problem
                        problem["category"] = category
                        problem["subcategory"] = concept
                        
                        all_problems.append(problem)
                        used_subcategories.add(concept)
                    except Exception as e:
                        print(f"Error generating {concept} problem: {str(e)}")

    print(f"Generated {len(all_problems)} problems:")
    for i, problem in enumerate(all_problems):
        print(f"  Problem {i+1}: {problem.get('category', 'unknown')} - {problem.get('subcategory', 'unknown')}")
    
    # Save problems to a single JSON file in the backend/problem_generators folder
    try:
        # Create the directory path if it doesn't exist
        os.makedirs("backend/problem_generators", exist_ok=True)
        
        # Use a fixed filename for all problem sets
        filepath = "backend/problem_generators/generated_problems.json"
        
        # Save the problems to the JSON file (overwriting any existing file)
        with open(filepath, "w") as f:
            json.dump(all_problems, f, indent=2)
        print(f"\nDetailed problems saved to {filepath}")
        
        # If logging is configured, log the save action
        try:
            logging.info(f"Detailed problems saved to {filepath}")
        except:
            pass  # Skip logging if it's not configured
    except Exception as e:
        print(f"Error saving problems to JSON: {e}")
        try:
            logging.error(f"Error saving problems to JSON: {e}")
        except:
            pass  # Skip logging if it's not configured
    
    return all_problems