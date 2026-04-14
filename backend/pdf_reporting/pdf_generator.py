# pdf_generator.py

from xml.sax.saxutils import escape as xml_escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable,
)

# ── Palette ───────────────────────────────────────────────────────────────────
PURPLE       = colors.HexColor('#6B4FA0')
LIGHT_PURPLE = colors.HexColor('#F3EEFF')
DARK_GRAY    = colors.HexColor('#333333')
MID_GRAY     = colors.HexColor('#666666')
LIGHT_GRAY   = colors.HexColor('#EEEEEE')
BOX_BORDER   = colors.HexColor('#CCCCCC')


# ── Problem text formatting ───────────────────────────────────────────────────

def _fmt(text):
    """Escape XML special chars and convert newlines to <br/> for Paragraph."""
    return xml_escape(str(text)).replace('\n', '<br/>')


def _format_problem_text(problem):
    """Return the question string for a problem dict (no number prefix)."""

    # word_problems stores the question in 'text'
    if 'text' in problem:
        return problem['text']

    # many generators store a pre-built question string
    if 'question' in problem:
        return problem['question']

    prob_type = problem.get('type', '')
    category  = problem.get('category', '')

    # ── Addition ──────────────────────────────────────────────────────────────
    if category == 'addition' or prob_type == 'addition':
        return f"{problem.get('first_number','?')}  +  {problem.get('second_number','?')}  =  ______"

    # ── Subtraction ───────────────────────────────────────────────────────────
    if category == 'subtraction' or prob_type == 'subtraction':
        return f"{problem.get('first_number','?')}  -  {problem.get('second_number','?')}  =  ______"

    # ── Number Sense ──────────────────────────────────────────────────────────
    if prob_type == 'comparison':
        return (f"Compare:  {problem.get('first_number','?')}  ( )  {problem.get('second_number','?')}\n"
                "Write  <  ,  >  ,  or  =  in the circle")

    if prob_type == 'ordering':
        nums = ',  '.join(str(n) for n in problem.get('numbers', []))
        return f"Order from least to greatest:\n{nums}"

    if prob_type == 'before_after':
        return f"What number comes {problem.get('question_type','before')} {problem.get('number','?')}?\n______"

    if prob_type == 'missing_numbers':
        seq = problem.get('sequence', problem.get('numbers', []))
        formatted = ',  '.join('______' if n is None else str(n) for n in seq)
        return f"Fill in the missing number:\n{formatted}"

    # ── Skip Counting ─────────────────────────────────────────────────────────
    if prob_type in ('by_ones_twos', 'by_fives_tens', 'by_hundreds'):
        seq = problem.get('sequence', [])
        formatted = ',  '.join('______' if n is None else str(n) for n in seq)
        return f"Fill in the missing number:\n{formatted}"

    # ── Place Value ───────────────────────────────────────────────────────────
    if prob_type in ('ones_tens', 'ones_tens_hundreds'):
        return (f"What digit is in the {problem.get('place','')} place?\n"
                f"Number:  {problem.get('number','')}")

    # ── Time Telling ──────────────────────────────────────────────────────────
    if prob_type in ('whole_hours', 'half_hours', 'quarter_hours', 'five_minute_increments'):
        h = problem.get('hour', 0)
        m = problem.get('minute', 0)
        return f"Draw the clock hands to show:\n{h}:{m:02d}"

    # ── Money ─────────────────────────────────────────────────────────────────
    if prob_type == 'identifying_coins':
        return "What coin is this?\n______"

    if prob_type == 'counting_pennies_nickels':
        return (f"Count the {problem.get('coin_type','')}s:\n"
                f"{problem.get('count','')} coins  =  ______ cents")

    if prob_type == 'mixed_coins':
        coins = ',  '.join(problem.get('coins', []))
        return f"Count the coins:\n{coins}\nTotal  =  ______ cents"

    if prob_type == 'making_change':
        return (f"Cost: {problem.get('cost','')}c     Paid: {problem.get('payment','')}c\n"
                "Change  =  ______ cents")

    # ── Fractions ─────────────────────────────────────────────────────────────
    if prob_type in ('halves_wholes', 'thirds_fourths'):
        return (f"What fraction is shaded?\n"
                f"({problem.get('shaded_parts','')} out of {problem.get('total_parts','')} parts)")

    if prob_type == 'comparing_fractions':
        return (f"Compare:  {problem.get('fraction1','')}  ( )  {problem.get('fraction2','')}\n"
                "Write  <  ,  >  ,  or  =  in the circle")

    # ── Measurement ───────────────────────────────────────────────────────────
    if prob_type == 'comparing_objects':
        return (f"Which is {problem.get('property','')}er?\n"
                f"{problem.get('object1','')}     or     {problem.get('object2','')}")

    if prob_type == 'non_standard_units':
        return (f"How long is the {problem.get('item_to_measure','')}?\n"
                f"About  ______  {problem.get('measuring_object','')}s long")

    if prob_type == 'rulers_inches_cm':
        return f"Measure the line:\n______  {problem.get('unit','')}"

    # ── Patterns ──────────────────────────────────────────────────────────────
    if prob_type == 'abab_patterns':
        pattern = ',  '.join(str(p) for p in problem.get('pattern', []))
        return f"What comes next?\n{pattern},  ______"

    if prob_type == 'extending_patterns':
        pattern = ',  '.join(str(p) for p in problem.get('pattern', []))
        return f"Extend the pattern:\n{pattern},  ______"

    if prob_type == 'creating_patterns':
        seq = problem.get('pattern', [])
        formatted = ',  '.join('______' if n is None else str(n) for n in seq)
        return f"Fill in the missing numbers:\n{formatted}"

    # ── Shapes ────────────────────────────────────────────────────────────────
    if prob_type == 'basic_2d_3d':
        kind = '2D' if problem.get('shape_type') == '2d' else '3D'
        return f"Name this {kind} shape:\n______"

    if prob_type == 'edges_faces_vertices':
        return (f"How many {problem.get('question_type','')} does a "
                f"{problem.get('shape_name','')} have?\n______")

    # ── Fallback ──────────────────────────────────────────────────────────────
    return "______"


# ── PDF builder ───────────────────────────────────────────────────────────────

def create_worksheet_pdf(problems, worksheet_type, number_range, concepts,
                         output_path, include_answer_key=False):
    """Generate a styled spiral-review PDF worksheet.

    Args:
        problems:           List of problem dicts from generate_problems()
        worksheet_type:     'spiral' or 'fluency'
        number_range:       'beginner', 'intermediate', or 'advanced'
        concepts:           List of concept identifiers
        output_path:        File path to write the PDF
        include_answer_key: Append an answer key page when True
    """
    MARGIN   = 0.55 * inch
    PAGE_W, PAGE_H = letter
    content_w = PAGE_W - 2 * MARGIN

    doc = BaseDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    frame = Frame(MARGIN, MARGIN, content_w, PAGE_H - 2 * MARGIN,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame])])

    # ── Styles ────────────────────────────────────────────────────────────────
    base = getSampleStyleSheet()['Normal']

    def S(name, **kw):
        p = ParagraphStyle(name, parent=base)
        for k, v in kw.items():
            setattr(p, k, v)
        return p

    banner_style  = S('Banner', fontName='Helvetica-Bold', fontSize=18,
                       textColor=colors.white, alignment=TA_CENTER)
    info_style    = S('Info',   fontName='Helvetica', fontSize=10, textColor=DARK_GRAY)
    num_style     = S('Num',    fontName='Helvetica-Bold', fontSize=13,
                       textColor=PURPLE, spaceAfter=2)
    q_style       = S('Q',      fontName='Helvetica', fontSize=12,
                       textColor=DARK_GRAY, leading=17, spaceAfter=2)
    ans_style     = S('Ans',    fontName='Helvetica', fontSize=9, textColor=MID_GRAY)
    ak_head_style = S('AKHead', fontName='Helvetica-Bold', fontSize=18,
                       textColor=PURPLE, alignment=TA_CENTER, spaceAfter=10)
    ak_item_style = S('AKItem', fontName='Helvetica', fontSize=11,
                       textColor=DARK_GRAY, leading=20)

    elements = []

    # ── Header banner ─────────────────────────────────────────────────────────
    type_label = 'Spiral Review' if worksheet_type == 'spiral' else 'Fluency Sheet'
    diff_label = number_range.capitalize()

    banner = Table(
        [[Paragraph(f'Math {type_label}  |  {diff_label}', banner_style)]],
        colWidths=[content_w],
    )
    banner.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), PURPLE),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
    ]))
    elements.append(banner)
    elements.append(Spacer(1, 8))

    # ── Student info ──────────────────────────────────────────────────────────
    info_row = Table(
        [[
            Paragraph('Name: _______________________________', info_style),
            Paragraph('Date: ________________', info_style),
            Paragraph(f'Score: ______ / {len(problems)}', info_style),
        ]],
        colWidths=[content_w * 0.45, content_w * 0.30, content_w * 0.25],
    )
    info_row.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(info_row)
    elements.append(Spacer(1, 4))
    elements.append(HRFlowable(width='100%', thickness=1.5, color=PURPLE, spaceAfter=8))

    # ── 2-column problem grid ─────────────────────────────────────────────────
    col_w = content_w / 2

    def make_cell(i, problem):
        q_text = _format_problem_text(problem)
        return [
            Paragraph(f'{i + 1}.', num_style),
            Paragraph(_fmt(q_text), q_style),
            Spacer(1, 4),
            Paragraph('Answer: _______________________', ans_style),
        ]

    cells = [make_cell(i, p) for i, p in enumerate(problems)]
    if len(cells) % 2:          # pad to even for 2-col layout
        cells.append([Paragraph('', q_style)])

    rows = [[cells[j], cells[j + 1]] for j in range(0, len(cells), 2)]

    style_cmds = [
        ('GRID',          (0, 0), (-1, -1), 0.75, BOX_BORDER),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]
    for r in range(len(rows)):
        bg = colors.white if r % 2 == 0 else LIGHT_PURPLE
        style_cmds.append(('BACKGROUND', (0, r), (-1, r), bg))

    grid = Table(rows, colWidths=[col_w, col_w])
    grid.setStyle(TableStyle(style_cmds))
    elements.append(grid)

    # ── Answer key (optional) ─────────────────────────────────────────────────
    if include_answer_key:
        elements.append(PageBreak())
        elements.append(Paragraph('Answer Key', ak_head_style))
        elements.append(HRFlowable(width='100%', thickness=1.5, color=PURPLE, spaceAfter=10))

        ak_cells = [
            Paragraph(f'<b>{i + 1}.</b>  {_fmt(p.get("answer", "-"))}', ak_item_style)
            for i, p in enumerate(problems)
        ]
        if len(ak_cells) % 2:
            ak_cells.append(Paragraph('', ak_item_style))

        ak_rows = [[ak_cells[j], ak_cells[j + 1]] for j in range(0, len(ak_cells), 2)]
        ak_table = Table(ak_rows, colWidths=[content_w / 2, content_w / 2])
        ak_table.setStyle(TableStyle([
            ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING',    (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING',   (0, 0), (-1, -1), 6),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
            ('LINEBELOW',     (0, 0), (-1, -2), 0.5, LIGHT_GRAY),
        ]))
        elements.append(ak_table)

    doc.build(elements)
    return output_path
