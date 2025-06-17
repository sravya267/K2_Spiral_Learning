from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing, Circle, Line, Rect, Polygon, String
from reportlab.graphics import renderPDF
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import math
import os
import random
import io
from datetime import datetime
from PIL import Image as PILImage

class MathWorksheetGenerator:
    """
    Main class for generating math worksheets using ReportLab
    """
    def __init__(self, output_path="worksheet.pdf"):
        """
        Initialize the worksheet generator

        Args:
            output_path (str): Path to save the generated PDF
        """
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        self.styles = getSampleStyleSheet()
        self.story = []

        # Create custom styles
        self.title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=0.3*inch
        )

        self.header_style = ParagraphStyle(
            'HeaderStyle',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=0.2*inch
        )

        self.problem_style = ParagraphStyle(
            'ProblemStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=0.1*inch
        )

def _add_worksheet_header(self, worksheet_type, level):
        """
        Add header with title, name, date fields

        Args:
            worksheet_type (str): "Spiral Review" or "Fluency Practice"
            level (str): "Beginner", "Intermediate", or "Advanced"
        """
        # Title
        title = f"{level} {worksheet_type} Worksheet"
        self.story.append(Paragraph(title, self.title_style))

        # Name and date fields
        data = [
            ['Name: _______________________', 'Date: _______________________']
        ]

        if worksheet_type == "Fluency Practice":
            data[0].append('Time: _______________________')

        # Create table for name/date/time
        header_table = Table(data, colWidths=[3*inch, 3*inch, 2*inch] if len(data[0]) > 2 else [3.5*inch, 3.5*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))

        self.story.append(header_table)
        self.story.append(Spacer(1, 0.25*inch))

    def _format_vertical_problem(self, num1, num2, operation='+'):
        """
        Format a vertical addition or subtraction problem

        Args:
            num1 (int): First number
            num2 (int): Second number
            operation (str): '+' or '-'

        Returns:
            list: Formatted problem lines
        """
        # Ensure num1 is always larger for subtraction
        if operation == '-' and num1 < num2:
            num1, num2 = num2, num1

        max_digits = max(len(str(num1)), len(str(num2))) + 1

        lines = []
        lines.append(' ' * (max_digits - len(str(num1))) + str(num1))
        lines.append(operation + ' ' * (max_digits - len(str(num2)) - 1) + str(num2))
        lines.append('-' * max_digits)
        lines.append(' ' * max_digits)  # Empty line for answer

        return lines

def _create_clock_problem(self, hour, minute=0):
        """
        Create a clock face drawing with specified time

        Args:
            hour (int): Hour (1-12)
            minute (int): Minute (0-59)

        Returns:
            Drawing: ReportLab drawing object with clock face
        """
        # Normalize hour to 12-hour format
        hour = hour % 12
        if hour == 0:
            hour = 12

        # Create drawing
        d = Drawing(100, 100)

        # Draw clock face
        d.add(Circle(50, 50, 40, fillColor=colors.white, strokeColor=colors.black, strokeWidth=1))

        # Draw hour markers
        for i in range(12):
            angle = math.radians(i * 30)
            x1 = 50 + 35 * math.sin(angle)
            y1 = 50 + 35 * math.cos(angle)
            x2 = 50 + 40 * math.sin(angle)
            y2 = 50 + 40 * math.cos(angle)
            d.add(Line(x1, y1, x2, y2, strokeColor=colors.black, strokeWidth=1))

            # Add numbers
            num_x = 50 + 28 * math.sin(angle)
            num_y = 50 + 28 * math.cos(angle)
            hour_num = i if i > 0 else 12
            d.add(String(num_x - 4 if hour_num > 9 else num_x - 2,
                         num_y - 3,
                         str(hour_num),
                         fontSize=8))

        # Draw hour hand
        hour_angle = math.radians((hour % 12) * 30 + minute * 0.5 - 90)
        hour_x = 50 + 20 * math.cos(hour_angle)
        hour_y = 50 + 20 * math.sin(hour_angle)
        d.add(Line(50, 50, hour_x, hour_y, strokeColor=colors.black, strokeWidth=2))

        # Draw minute hand
        minute_angle = math.radians(minute * 6 - 90)
        minute_x = 50 + 30 * math.cos(minute_angle)
        minute_y = 50 + 30 * math.sin(minute_angle)
        d.add(Line(50, 50, minute_x, minute_y, strokeColor=colors.black, strokeWidth=1))

        # Draw center point
        d.add(Circle(50, 50, 2, fillColor=colors.black))

        return d

def _create_coin_image(self, coin_type):
        """
        Create an image of a coin

        Args:
            coin_type (str): "penny", "nickel", "dime", or "quarter"

        Returns:
            Image: ReportLab image object
        """
        # This is a placeholder - in a real implementation, you would use actual coin images
        # For now, we'll create simple representations

        coin_values = {
            "penny": "1¢",
            "nickel": "5¢",
            "dime": "10¢",
            "quarter": "25¢"
        }

        coin_sizes = {
            "penny": 50,
            "nickel": 55,
            "dime": 45,
            "quarter": 60
        }

        # Create a drawing with the coin
        size = coin_sizes.get(coin_type.lower(), 50)
        d = Drawing(size, size)

        # Draw the coin
        d.add(Circle(size/2, size/2, size/2 - 2,
                     fillColor=colors.gold if coin_type.lower() == "penny" else colors.silver,
                     strokeColor=colors.black,
                     strokeWidth=1))

        # Add the value text
        value = coin_values.get(coin_type.lower(), "")
        d.add(String(size/2 - 8, size/2 - 4, value, fontSize=10, fillColor=colors.black))

        # Convert to image buffer
        img_buffer = io.BytesIO()
        renderPDF.drawToFile(d, img_buffer, 'coin')
        img_buffer.seek(0)

        # Convert to PIL Image and then to ReportLab Image
        pil_img = PILImage.open(img_buffer)
        pil_img = pil_img.convert('RGB')

        img_temp = f"temp_{coin_type}.png"
        pil_img.save(img_temp)

        # Create ReportLab Image
        img = Image(img_temp, width=size, height=size)

        # Clean up temp file
        os.remove(img_temp)

        return img

def _create_shape_drawing(self, shape_type):
        """
        Create a drawing of a geometric shape

        Args:
            shape_type (str): Type of shape to draw

        Returns:
            Drawing: ReportLab drawing object
        """
        d = Drawing(100, 100)

        if shape_type.lower() == "square":
            # Draw a square
            d.add(Rect(20, 20, 60, 60,
                       fillColor=colors.white,
                       strokeColor=colors.black,
                       strokeWidth=1))

        elif shape_type.lower() == "rectangle":
            # Draw a rectangle
            d.add(Rect(10, 30, 80, 40,
                       fillColor=colors.white,
                       strokeColor=colors.black,
                       strokeWidth=1))

        elif shape_type.lower() == "triangle":
            # Draw a triangle
            p = Polygon([50, 90, 10, 20, 90, 20],
                         fillColor=colors.white,
                         strokeColor=colors.black,
                         strokeWidth=1)
            d.add(p)

        elif shape_type.lower() == "circle":
            # Draw a circle
            d.add(Circle(50, 50, 40,
                         fillColor=colors.white,
                         strokeColor=colors.black,
                         strokeWidth=1))

        elif shape_type.lower() == "pentagon":
            # Draw a pentagon
            points = []
            for i in range(5):
                angle = math.radians(i * 72 - 90)
                x = 50 + 40 * math.cos(angle)
                y = 50 + 40 * math.sin(angle)
                points.extend([x, y])

            p = Polygon(points,
                         fillColor=colors.white,
                         strokeColor=colors.black,
                         strokeWidth=1)
            d.add(p)

        elif shape_type.lower() == "hexagon":
            # Draw a hexagon
            points = []
            for i in range(6):
                angle = math.radians(i * 60)
                x = 50 + 40 * math.cos(angle)
                y = 50 + 40 * math.sin(angle)
                points.extend([x, y])

            p = Polygon(points,
                         fillColor=colors.white,
                         strokeColor=colors.black,
                         strokeWidth=1)
            d.add(p)

        else:
            # Default to a circle if shape not recognized
            d.add(Circle(50, 50, 40,
                         fillColor=colors.white,
                         strokeColor=colors.black,
                         strokeWidth=1))
            d.add(String(35, 48, "?", fontSize=20))

        return d

def _create_fraction_visual(self, numerator, denominator):
        """
        Create a visual representation of a fraction

        Args:
            numerator (int): Fraction numerator
            denominator (int): Fraction denominator

        Returns:
            Drawing: ReportLab drawing object
        """
        d = Drawing(200, 80)

        # Draw the whole
        total_width = 180
        part_width = total_width / denominator
        height = 30

        # Draw all parts
        for i in range(denominator):
            x = 10 + i * part_width
            d.add(Rect(x, 25, part_width, height,
                       fillColor=colors.white,
                       strokeColor=colors.black,
                       strokeWidth=1))

        # Fill in the numerator parts
        for i in range(numerator):
            x = 10 + i * part_width
            d.add(Rect(x, 25, part_width, height,
                       fillColor=colors.lightgrey,
                       strokeColor=colors.black,
                       strokeWidth=1))

        # Add fraction text
        d.add(String(90, 5, f"{numerator}/{denominator}", fontSize=12))

        return d

def _create_number_grid(self, start, end, highlight=None, skip_by=1):
        """
        Create a number grid for counting exercises

        Args:
            start (int): Starting number
            end (int): Ending number
            highlight (list): List of numbers to highlight
            skip_by (int): Count by this number

        Returns:
            Table: ReportLab table object
        """
        if highlight is None:
            highlight = []

        # Calculate grid dimensions
        numbers = list(range(start, end + 1, skip_by))
        rows = math.ceil(len(numbers) / 10)

        # Create grid data
        data = []
        for r in range(rows):
            row = []
            for c in range(10):
                idx = r * 10 + c
                if idx < len(numbers):
                    row.append(str(numbers[idx]))
                else:
                    row.append("")
            data.append(row)

        # Create table
        grid_table = Table(data, colWidths=[0.3*inch] * 10)

        # Set styles
        styles = [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]

        # Add highlighting
        for num in highlight:
            if num in numbers:
                idx = numbers.index(num)
                row = idx // 10
                col = idx % 10
                styles.append(('BACKGROUND', (col, row), (col, row), colors.lightgrey))

        grid_table.setStyle(TableStyle(styles))

        return grid_table

def generate_addition_problems(self, num_problems, level):
        """
        Generate addition problems based on level

        Args:
            num_problems (int): Number of problems to generate
            level (str): "Beginner", "Intermediate", or "Advanced"
        """
        self.story.append(Paragraph("Addition Problems", self.header_style))

        # Define number ranges based on level
        if level.lower() == "beginner":
            max_num = 9
        elif level.lower() == "intermediate":
            max_num = 99
        else:  # Advanced
            max_num = 999

        # Generate problems
        problem_tables = []

        for _ in range(num_problems):
            if level.lower() == "beginner":
                # Generate simple single-digit problems
                num1 = random.randint(0, max_num)
                num2 = random.randint(0, max_num)
            elif level.lower() == "intermediate":
                # Generate double-digit problems without regrouping
                num1 = random.randint(10, max_num)
                # Ensure no regrouping needed
                ones_digit = num1 % 10
                max_ones = 9 - ones_digit
                tens_digit = random.randint(0, 9)
                num2 = tens_digit * 10 + random.randint(0, max_ones)
            else:  # Advanced
                # Generate triple-digit problems without regrouping
                num1 = random.randint(100, max_num)
                # Ensure no regrouping needed
                ones_digit = num1 % 10
                tens_digit = (num1 // 10) % 10
                max_ones = 9 - ones_digit
                max_tens = 9 - tens_digit
                hundreds_digit = random.randint(0, 9)
                num2 = hundreds_digit * 100 + random.randint(0, max_tens) * 10 + random.randint(0, max_ones)

            # Format problem
            problem_lines = self._format_vertical_problem(num1, num2, '+')

            # Create table for the problem
            data = [[line] for line in problem_lines]
            problem_table = Table(data, colWidths=[1.2*inch])
            problem_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (0, -1), 12),
            ]))

            problem_tables.append(problem_table)

        # Arrange problems in rows of 4
        problems_per_row = 4
        for i in range(0, len(problem_tables), problems_per_row):
            batch = problem_tables[i:i+problems_per_row]

            # Create a row of problems
            problem_row = Table([batch], colWidths=[1.5*inch] * len(batch))
            problem_row.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            self.story.append(problem_row)
            self.story.append(Spacer(1, 0.2*inch))

def generate_subtraction_problems(self, num_problems, level):
        """
        Generate subtraction problems based on level

        Args:
            num_problems (int): Number of problems to generate
            level (str): "Beginner", "Intermediate", or "Advanced"
        """
        self.story.append(Paragraph("Subtraction Problems", self.header_style))

        # Define number ranges based on level
        if level.lower() == "beginner":
            max_num = 9
        elif level.lower() == "intermediate":
            max_num = 99
        else:  # Advanced
            max_num = 999

        # Generate problems
        problem_tables = []

        for _ in range(num_problems):
            if level.lower() == "beginner":
                # Generate simple single-digit problems
                num1 = random.randint(0, max_num)
                num2 = random.randint(0, num1)  # Ensure positive result
            elif level.lower() == "intermediate":
                # Generate double-digit problems without regrouping
                tens_digit = random.randint(1, 9)
                ones_digit = random.randint(0, 9)
                num1 = tens_digit * 10 + ones_digit

                # Ensure no regrouping needed (subtrahend ones <= minuend ones)
                max_tens = tens_digit
                max_ones = ones_digit

                sub_tens = random.randint(0, max_tens)
                sub_ones = random.randint(0, max_ones)
                num2 = sub_tens * 10 + sub_ones
            else:  # Advanced
                # Generate triple-digit problems without regrouping
                hundreds_digit = random.randint(1, 9)
                tens_digit = random.randint(0, 9)
                ones_digit = random.randint(0, 9)
                num1 = hundreds_digit * 100 + tens_digit * 10 + ones_digit

                # Ensure no regrouping needed
                max_hundreds = hundreds_digit
                max_tens = tens_digit
                max_ones = ones_digit

                sub_hundreds = random.randint(0, max_hundreds)
                sub_tens = random.randint(0, max_tens)
                sub_ones = random.randint(0, max_ones)
                num2 = sub_hundreds * 100 + sub_tens * 10 + sub_ones

            # Format problem
            problem_lines = self._format_vertical_problem(num1, num2, '-')

            # Create table for the problem
            data = [[line] for line in problem_lines]
            problem_table = Table(data, colWidths=[1.2*inch])
            problem_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (0, -1), 12),
            ]))

            problem_tables.append(problem_table)

        # Arrange problems in rows of 4
        problems_per_row = 4
        for i in range(0, len(problem_tables), problems_per_row):
            batch = problem_tables[i:i+problems_per_row]

            # Create a row of problems
            problem_row = Table([batch], colWidths=[1.5*inch] * len(batch))
            problem_row.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            self.story.append(problem_row)
            self.story.append(Spacer(1, 0.2*inch))

def generate_time_problems(self, num_problems, level):
        """
        Generate time telling problems based on level

        Args:
            num_problems (int): Number of problems to generate
            level (str): "Beginner", "Intermediate", or "Advanced"
        """
        self.story.append(Paragraph("Time Problems", self.header_style))

        # Define time options based on level
        if level.lower() == "beginner":
            # Whole hours only
            possible_hours = list(range(1, 13))
            possible_minutes = [0]
        elif level.lower() == "intermediate":
            # Half hours
            possible_hours = list(range(1, 13))
            possible_minutes = [0, 30]
        else:  # Advanced
            # Quarter and five-minute increments
            possible_hours = list(range(1, 13))
            possible_minutes = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

        # Generate problems
        clock_drawings = []
        problem_texts = []

        for i in range(num_problems):
            hour = random.choice(possible_hours)
            minute = random.choice(possible_minutes)

            # Create clock drawing
            clock = self._create_clock_problem(hour, minute)
            clock_drawings.append(clock)

            # Generate problem text
            if level.lower() == "beginner":
                problem_text = f"{i+1}. What time is shown on the clock? ______"
            else:
                problem_text = f"{i+1}. What time is shown on the clock? ______ : ______"

            problem_texts.append(Paragraph(problem_text, self.problem_style))

        # Arrange problems in rows of 2
        problems_per_row = 2
        for i in range(0, len(clock_drawings), problems_per_row):
            # Create content for this row
            clocks = clock_drawings[i:i+problems_per_row]
            texts = problem_texts[i:i+problems_per_row]

            # Create cells with clock and text
            cells = []
            for j in range(len(clocks)):
                cell_content = [clocks[j], texts[j]]
                cells.append(cell_content)

            # Pad with empty cells if needed
            while len(cells) < problems_per_row:
                cells.append(["", ""])

            # Transpose the cells for the table
            row_data = list(zip(*cells))

            # Create a table for this row of problems
            problem_row = Table(row_data, colWidths=[3*inch] * problems_per_row)
            problem_row.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            self.story.append(problem_row)
            self.story.append(Spacer(1, 0.2*inch))

def generate_money_problems(self, num_problems, level):
        """
        Generate money counting problems based on level

        Args:
            num_problems (int): Number of problems to generate
            level (str): "Beginner", "Intermediate", or "Advanced"
        """
        self.story.append(Paragraph("Money Problems", self.header_style))

        # Define coin types based on level
        if level.lower() == "beginner":
            # Just pennies and nickels
            possible_coins = ["penny", "nickel"]
            max_coins = 5
        elif level.lower() == "intermediate":
            # Add dimes, mixed coins
            possible_coins = ["penny", "nickel", "dime"]
            max_coins = 8
        else:  # Advanced
            # All coins including quarters
            possible_coins = ["penny", "nickel", "dime", "quarter"]
            max_coins = 10

        # Generate problems
        for i in range(num_problems):
            # Determine number of coins
            num_coins = random.randint(2, max_coins)

            # Select coins
            coins = [random.choice(possible_coins) for _ in range(num_coins)]

            # Create coin images
            coin_images = [self._create_coin_image(coin) for coin in coins]

            # Calculate total
            total_cents = sum({
                "penny": 1,
                "nickel": 5,
                "dime": 10,
                "quarter": 25
            }[coin] for coin in coins)

            # Format problem text
            if level.lower() == "beginner":
                problem_text = f"{i+1}. Count the coins. Total: _____ cents"
            else:
                problem_text = f"{i+1}. Count the coins. Total: $_____"

            self.story.append(Paragraph(problem_text, self.problem_style))

            # Arrange coins in a row
            coin_row_data = [coin_images]
            coin_row = Table(coin_row_data, colWidths=[0.7*inch] * len(coin_images))
            coin_row.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            self.story.append(coin_row)
            self.story.append(Spacer(1, 0.3*inch))

def generate_place_value_problems(self, num_problems, level):
        """
        Generate place value problems based on level

        Args:
            num_problems (int): Number of problems to generate
            level (str): "Beginner", "Intermediate", or "Advanced"
        """
        self.story.append(Paragraph("Place Value Problems", self.header_style))

        # Define number ranges based on level
        if level.lower() == "beginner":
            # 1-99 (ones and tens)
            min_num = 10
            max_num = 99
            places = ["tens", "ones"]
        elif level.lower() == "intermediate":
            # 100-999 (hundreds, tens, ones)
            min_num = 100
            max_num = 999
            places = ["hundreds", "tens", "ones"]
        else:  # Advanced
            # 100-999 with expanded form
            min_num = 100
            max_num = 999
            places = ["hundreds", "tens", "ones"]

        # Generate problems
        for i in range(num_problems):
            # Generate a random number
            number = random.randint(min_num, max_num)

            # Create problem based on level
            if level.lower() in ["beginner", "intermediate"]:
                problem_text = f"{i+1}. For the number {number}, write the digit in each place value:"

                # Create place value boxes
                data = [[place] for place in places]
                data2 = [["_____"] for _ in places]

                pv_table = Table([list(zip(*data))[0], list(zip(*data2))[0]], colWidths=[1.2*inch] * len(places))
                pv_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]))

                self.story.append(Paragraph(problem_text, self.problem_style))
                self.story.append(pv_table)

            else:  # Advanced with expanded form
                problem_text = (
                    f"{i+1}. Write the number {number} in expanded form:\n"
                    f"{number} = _____ hundreds + _____ tens + _____ ones"
                )
                self.story.append(Paragraph(problem_text, self.problem_style))

            self.story.append(Spacer(1, 0.3*inch))

def generate_word_problems(self, num_problems, level):
        """
        Generate word problems based on level

        Args:
            num_problems (int): Number of problems to generate
            level (str): "Beginner", "Intermediate", or "Advanced"
        """
        self.story.append(Paragraph("Word Problems", self.header_style))

        # Define problem templates based on level
        beginner_templates = [
            "Sam has {num1} apples. He gets {num2} more apples. How many apples does Sam have now?",
            "There are {num1} birds in a tree. {num2} more birds join them. How many birds are there now?",
            "Maria has {num1} stickers. She gives {num2} stickers to her friend. How many stickers does Maria have left?",
            "There are {num1} children on the playground. {num2} children go home. How many children are left on the playground?",
            "Jack has {num1} toy cars. His friend has {num2} toy cars. How many toy cars do they have in total?"
        ]

        intermediate_templates = [
            "A class has {num1} students. If {num2} students are absent today, how many students are present?",
            "Jane buys a book for ${num1} and a pencil for ${num2}. How much did she spend in total?",
            "Tom has {num1} marbles. He gives {num2} marbles to his sister and gets {num3} marbles from his friend. How many marbles does Tom have now?",
            "A baker made {num1} cookies. He sold {num2} cookies in the morning and {num3} cookies in the afternoon. How many cookies are left?",
            "A shelf has {num1} books. A second shelf has {num2} books. How many more books are on the first shelf than the second shelf?"
        ]

        advanced_templates = [
            "A store has {num1} apples. On Monday, they sell {num2} apples. On Tuesday, they sell {num3} apples. On Wednesday, they get a delivery of {num4} more apples. How many apples does the store have now?",
            "A class of {num1} students is divided into groups of {num2}. How many complete groups can be formed, and how many students will be left over?",
            "A school ordered {num1} pencils. They were packed in boxes of {num2} pencils each. How many full boxes did the school receive, and how many extra pencils were there?",
            "A car travels at {num1} miles per hour. How far will it travel in {num2} hours?",
            "A rectangular garden is {num1} feet long and {num2} feet wide. What is the area of the garden in square feet?"
        ]

        # Select templates based on level
        if level.lower() == "beginner":
            templates = beginner_templates
            num_range = (1, 10)
        elif level.lower() == "intermediate":
            templates = intermediate_templates
            num_range = (10, 50)
        else:  # Advanced
            templates = advanced_templates
            num_range = (50, 200)

        # Generate problems
        for i in range(num_problems):
            # Select a random template
            template = random.choice(templates)

            # Generate random numbers
            if "{num1}" in template:
                num1 = random.randint(num_range[0], num_range[1])
                template = template.replace("{num1}", str(num1))

            if "{num2}" in template:
                num2 = random.randint(num_range[0], num_range[1])
                template = template.replace("{num2}", str(num2))

            if "{num3}" in template:
                num3 = random.randint(num_range[0], num_range[1])
                template = template.replace("{num3}", str(num3))

            if "{num4}" in template:
                num4 = random.randint(num_range[0], num_range[1])
                template = template.replace("{num4}", str(num4))

            # Format problem
            problem_text = f"{i+1}. {template}"
            self.story.append(Paragraph(problem_text, self.problem_style))

            # Add work space
            self.story.append(Paragraph("Show your work:", self.problem_style))

            # Create a box for work
            work_table = Table([[""], [""]], colWidths=[6*inch], rowHeights=[0.5*inch, 0.5*inch])
            work_table.setStyle(TableStyle([
                ('BOX', (0, 0), (0, 1), 0.5, colors.black),
                ('LINEABOVE', (0, 1), (0, 1), 0.5, colors.black),
            ]))

            self.story.append(work_table)
            self.story.append(Spacer(1, 0.3*inch))

