# pdf_generator.py

from collections import defaultdict
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak,
)

# ── Palette ───────────────────────────────────────────────────────────────────
PURPLE      = colors.HexColor('#6B4FA0')
DARK_PURPLE = colors.HexColor('#4A3570')
LIGHT_PURPLE= colors.HexColor('#F3EEFF')
DARK_GRAY   = colors.HexColor('#222222')
MID_GRAY    = colors.HexColor('#555555')
BORDER      = colors.HexColor('#333333')
WHITE       = colors.white

# ── Category display names ────────────────────────────────────────────────────
CATEGORY_NAMES = {
    'addition':     'Addition',
    'subtraction':  'Subtraction',
    'number_sense': 'Number Sense',
    'skip_counting':'Skip Counting',
    'place_value':  'Place Value',
    'time_telling': 'Time Telling',
    'money_counting':'Money',
    'word_problems':'Word Problems',
    'shapes':       'Shapes',
    'fractions':    'Fractions',
    'measurement':  'Measurement',
    'patterns':     'Patterns & Algebra',
    'graphing':     'Graphing & Data',
    'odd_even':     'Odd & Even',
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _e(text):
    """Escape XML special chars and convert newlines to <br/>."""
    return xml_escape(str(text)).replace('\n', '<br/>')


def _format_problem(problem, num, styles):
    """Return a list of Paragraphs/Spacers for one problem inside a section."""
    prob_type = problem.get('type', '')
    category  = problem.get('category', '')

    # ── Vertical math (addition / subtraction) ────────────────────────────────
    if category in ('addition', 'subtraction') or prob_type in ('addition', 'subtraction'):
        op  = '+' if (category == 'addition' or prob_type == 'addition') else '\u2212'
        n1  = str(problem.get('first_number',  '?'))
        n2  = str(problem.get('second_number', '?'))
        w   = max(len(n1), len(n2)) + 1
        line1 = n1.rjust(w)
        line2 = (op + '\u2009' + n2).rjust(w)   # thin-space before number
        bar   = '\u2015' * w
        text  = f'<font name="Courier" size="15">{_e(line1)}<br/>{_e(line2)}<br/>{_e(bar)}</font>'
        return [Paragraph(text, styles['math']), Spacer(1, 4)]

    # ── Pre-built question fields ─────────────────────────────────────────────
    if 'text' in problem:        # word_problems
        q = problem['text']
        return [
            Paragraph(_e(q), styles['q']),
            Spacer(1, 6),
            Paragraph('Answer: _______________________________', styles['ans']),
        ]
    if 'question' in problem:
        return [Paragraph(f'{num}. {_e(problem["question"])}', styles['q']),
                Paragraph('Answer: _______________', styles['ans'])]

    # ── Number sense ──────────────────────────────────────────────────────────
    if prob_type == 'comparison':
        return [Paragraph(
            f'{num}. {_e(problem.get("first_number","?"))} '
            f'<font size="16">&#9675;</font> '
            f'{_e(problem.get("second_number","?"))}&nbsp;&nbsp;'
            f'<font size="9" color="grey">(write &lt;, &gt;, or =)</font>',
            styles['q'])]

    if prob_type == 'ordering':
        nums = ',  '.join(str(n) for n in problem.get('numbers', []))
        return [Paragraph(f'{num}. Order least to greatest:<br/>{_e(nums)}', styles['q']),
                Paragraph('Answer: _______________', styles['ans'])]

    if prob_type == 'before_after':
        return [Paragraph(
            f'{num}. What comes {_e(problem.get("question_type","before"))} {_e(problem.get("number","?"))}?',
            styles['q']),
                Paragraph('Answer: _______', styles['ans'])]

    if prob_type == 'missing_numbers':
        seq = problem.get('sequence', problem.get('numbers', []))
        fmt = ',  '.join('______' if n is None else str(n) for n in seq)
        return [Paragraph(f'{num}. {_e(fmt)}', styles['q'])]

    # ── Skip counting ─────────────────────────────────────────────────────────
    if prob_type in ('by_ones_twos', 'by_fives_tens', 'by_hundreds'):
        seq = problem.get('sequence', [])
        fmt = ',  '.join('______' if n is None else str(n) for n in seq)
        return [Paragraph(f'{num}. {_e(fmt)}', styles['q'])]

    # ── Place value ───────────────────────────────────────────────────────────
    if prob_type in ('ones_tens', 'ones_tens_hundreds'):
        return [Paragraph(
            f'{num}. What digit is in the <b>{_e(problem.get("place",""))}</b> place?<br/>'
            f'Number: <b>{_e(problem.get("number",""))}</b>',
            styles['q']),
                Paragraph('Answer: _______', styles['ans'])]

    # ── Time telling ──────────────────────────────────────────────────────────
    if prob_type in ('whole_hours', 'half_hours', 'quarter_hours', 'five_minute_increments'):
        h = problem.get('hour', 0)
        m = problem.get('minute', 0)
        return [Paragraph(f'{num}. Draw hands to show <b>{h}:{m:02d}</b>', styles['q']),
                Spacer(1, 30)]   # space for drawing

    # ── Money ─────────────────────────────────────────────────────────────────
    if prob_type == 'identifying_coins':
        return [Paragraph(f'{num}. What coin is this?', styles['q']),
                Paragraph('Answer: _______', styles['ans'])]
    if prob_type == 'counting_pennies_nickels':
        return [Paragraph(
            f'{num}. Count the {_e(problem.get("coin_type",""))}s:<br/>'
            f'{_e(problem.get("count",""))} coins = ______ cents', styles['q'])]
    if prob_type == 'mixed_coins':
        coins = ', '.join(problem.get('coins', []))
        return [Paragraph(f'{num}. Count: {_e(coins)}<br/>Total = ______ cents', styles['q'])]
    if prob_type == 'making_change':
        return [Paragraph(
            f'{num}. Cost: {_e(problem.get("cost",""))}¢&nbsp;&nbsp;'
            f'Paid: {_e(problem.get("payment",""))}¢<br/>Change = ______ ¢', styles['q'])]

    # ── Fractions ─────────────────────────────────────────────────────────────
    if prob_type in ('halves_wholes', 'thirds_fourths'):
        return [Paragraph(
            f'{num}. What fraction is shaded?<br/>'
            f'({_e(problem.get("shaded_parts",""))} of {_e(problem.get("total_parts",""))} parts)',
            styles['q']),
                Paragraph('Answer: _______', styles['ans'])]
    if prob_type == 'comparing_fractions':
        return [Paragraph(
            f'{num}. {_e(problem.get("fraction1",""))} '
            f'<font size="16">&#9675;</font> '
            f'{_e(problem.get("fraction2",""))}&nbsp;&nbsp;'
            f'<font size="9" color="grey">(write &lt;, &gt;, or =)</font>',
            styles['q'])]

    # ── Measurement ───────────────────────────────────────────────────────────
    if prob_type == 'comparing_objects':
        return [Paragraph(
            f'{num}. Which is {_e(problem.get("property",""))}er?<br/>'
            f'{_e(problem.get("object1",""))} &nbsp;&nbsp;or&nbsp;&nbsp; {_e(problem.get("object2",""))}',
            styles['q']),
                Paragraph('Answer: _______', styles['ans'])]
    if prob_type == 'non_standard_units':
        return [Paragraph(
            f'{num}. How long is the {_e(problem.get("item_to_measure",""))}?<br/>'
            f'About ______ {_e(problem.get("measuring_object",""))}s long', styles['q'])]
    if prob_type == 'rulers_inches_cm':
        return [Paragraph(f'{num}. Measure the line in {_e(problem.get("unit",""))}:<br/>______ {_e(problem.get("unit",""))}', styles['q'])]

    # ── Patterns ─────────────────────────────────────────────────────────────
    if prob_type == 'abab_patterns':
        pat = ', '.join(str(p) for p in problem.get('pattern', []))
        return [Paragraph(f'{num}. What comes next?<br/>{_e(pat)}, ______', styles['q'])]
    if prob_type == 'extending_patterns':
        pat = ', '.join(str(p) for p in problem.get('pattern', []))
        return [Paragraph(f'{num}. Extend the pattern:<br/>{_e(pat)}, ______', styles['q'])]
    if prob_type == 'creating_patterns':
        seq = problem.get('pattern', [])
        fmt = ', '.join('______' if n is None else str(n) for n in seq)
        return [Paragraph(f'{num}. Fill in the missing numbers:<br/>{_e(fmt)}', styles['q'])]

    # ── Shapes ────────────────────────────────────────────────────────────────
    if prob_type == 'basic_2d_3d':
        kind = '2D' if problem.get('shape_type') == '2d' else '3D'
        return [Paragraph(f'{num}. Name this {kind} shape:', styles['q']),
                Paragraph('Answer: _______', styles['ans'])]
    if prob_type == 'edges_faces_vertices':
        return [Paragraph(
            f'{num}. How many <b>{_e(problem.get("question_type",""))}</b> does a '
            f'{_e(problem.get("shape_name",""))} have?',
            styles['q']),
                Paragraph('Answer: _______', styles['ans'])]

    # ── Fallback ──────────────────────────────────────────────────────────────
    return [Paragraph(f'{num}. ______', styles['q'])]


def _make_section(category, problems, col_w, styles):
    """Build one category section as a Table with a bold header row."""
    display = CATEGORY_NAMES.get(category, category.replace('_', ' ').title())

    # Header cell
    header = Paragraph(display, styles['sec_head'])

    # Problem cells — collect all problem flowables into a single inner cell
    inner = []
    for i, prob in enumerate(problems):
        inner.extend(_format_problem(prob, i + 1, styles))
        inner.append(Spacer(1, 6))

    section = Table(
        [[header], [inner]],
        colWidths=[col_w],
        spaceBefore=6, spaceAfter=6,
    )
    section.setStyle(TableStyle([
        # header row
        ('BACKGROUND',    (0, 0), (-1, 0), DARK_PURPLE),
        ('TEXTCOLOR',     (0, 0), (-1, 0), WHITE),
        ('TOPPADDING',    (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('LEFTPADDING',   (0, 0), (-1, 0), 10),
        ('RIGHTPADDING',  (0, 0), (-1, 0), 10),
        # problems row
        ('BACKGROUND',    (0, 1), (-1, 1), WHITE),
        ('TOPPADDING',    (0, 1), (-1, 1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
        ('LEFTPADDING',   (0, 1), (-1, 1), 10),
        ('RIGHTPADDING',  (0, 1), (-1, 1), 10),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        # outer border
        ('BOX',           (0, 0), (-1, -1), 1.5, BORDER),
    ]))
    return section


# ── Page border drawn on every page ──────────────────────────────────────────

def _draw_page_border(canvas, doc):
    canvas.saveState()
    m = 0.3 * inch
    w, h = letter
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(2)
    canvas.rect(m, m, w - 2 * m, h - 2 * m)
    # inner thin border
    canvas.setLineWidth(0.5)
    canvas.rect(m + 4, m + 4, w - 2 * m - 8, h - 2 * m - 8)
    canvas.restoreState()


# ── Main PDF builder ──────────────────────────────────────────────────────────

def create_worksheet_pdf(problems, worksheet_type, number_range, concepts,
                         output_path, include_answer_key=False):
    """Generate a K-2 spiral review worksheet with category section boxes."""

    MARGIN    = 0.55 * inch
    PAGE_W, PAGE_H = letter
    content_w = PAGE_W - 2 * MARGIN

    doc = BaseDocTemplate(
        output_path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    frame = Frame(MARGIN, MARGIN, content_w, PAGE_H - 2 * MARGIN,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(
        id='main', frames=[frame], onPage=_draw_page_border)])

    # ── Styles ────────────────────────────────────────────────────────────────
    base = getSampleStyleSheet()['Normal']
    def S(name, **kw):
        p = ParagraphStyle(name, parent=base)
        for k, v in kw.items():
            setattr(p, k, v)
        return p

    styles = {
        'title':    S('title',    fontName='Helvetica-Bold', fontSize=16,
                       textColor=DARK_PURPLE, alignment=TA_CENTER, spaceAfter=4),
        'name':     S('name',     fontName='Helvetica', fontSize=11, textColor=DARK_GRAY),
        'sec_head': S('sec_head', fontName='Helvetica-Bold', fontSize=13,
                       textColor=WHITE, alignment=TA_CENTER),
        'q':        S('q',        fontName='Helvetica', fontSize=12,
                       textColor=DARK_GRAY, leading=18, spaceAfter=2),
        'math':     S('math',     fontName='Courier', fontSize=15,
                       textColor=DARK_GRAY, leading=20, alignment=TA_LEFT),
        'ans':      S('ans',      fontName='Helvetica', fontSize=10, textColor=MID_GRAY),
        'ak_head':  S('ak_head',  fontName='Helvetica-Bold', fontSize=16,
                       textColor=DARK_PURPLE, alignment=TA_CENTER, spaceAfter=8),
        'ak_item':  S('ak_item',  fontName='Helvetica', fontSize=11,
                       textColor=DARK_GRAY, leading=20),
    }

    elements = []

    # ── Page title & name line ────────────────────────────────────────────────
    type_label = 'Spiral Review' if worksheet_type == 'spiral' else 'Fluency Practice'
    elements.append(Paragraph(f'Math {type_label}  \u2014  {number_range.capitalize()}', styles['title']))
    elements.append(Spacer(1, 2))

    info = Table(
        [[Paragraph('Name: ______________________________________', styles['name']),
          Paragraph('Date: ____________________', styles['name']),
          Paragraph(f'Score: _____ / {len(problems)}', styles['name'])]],
        colWidths=[content_w * 0.45, content_w * 0.33, content_w * 0.22],
    )
    info.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                               ('TOPPADDING', (0,0), (-1,-1), 2),
                               ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
    elements.append(info)
    elements.append(HRFlowable(width='100%', thickness=1.5, color=DARK_PURPLE, spaceAfter=8))

    # ── Group problems by category (preserve order of first appearance) ────────
    seen = {}
    for p in problems:
        cat = p.get('category', 'general')
        seen.setdefault(cat, []).append(p)

    # ── Build one section box per category ────────────────────────────────────
    col_w = (content_w - 8) / 2   # 8 pt gap between columns

    sections = [_make_section(cat, probs, col_w, styles)
                for cat, probs in seen.items()]

    if not sections:
        elements.append(Paragraph('No problems generated.', styles['q']))
    else:
        # Pad to even number
        if len(sections) % 2:
            sections.append(Paragraph('', styles['q']))

        rows = [[sections[i], sections[i + 1]] for i in range(0, len(sections), 2)]

        grid = Table(rows, colWidths=[col_w, col_w], spaceAfter=0)
        grid.setStyle(TableStyle([
            ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING',    (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING',   (0, 0), (-1, -1), 4),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
        ]))
        elements.append(grid)

    # ── Answer key ────────────────────────────────────────────────────────────
    if include_answer_key:
        elements.append(PageBreak())
        elements.append(Paragraph('Answer Key', styles['ak_head']))
        elements.append(HRFlowable(width='100%', thickness=1.5, color=DARK_PURPLE, spaceAfter=10))

        em_dash = '\u2014'
        ak_cells = [
            Paragraph(f'<b>{i + 1}.</b>  {_e(p.get("answer", em_dash))}', styles['ak_item'])
            for i, p in enumerate(problems)
        ]
        if len(ak_cells) % 2:
            ak_cells.append(Paragraph('', styles['ak_item']))

        ak_rows = [[ak_cells[j], ak_cells[j + 1]] for j in range(0, len(ak_cells), 2)]
        ak_table = Table(ak_rows, colWidths=[content_w / 2, content_w / 2])
        ak_table.setStyle(TableStyle([
            ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING',    (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING',   (0, 0), (-1, -1), 6),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
            ('LINEBELOW',     (0, 0), (-1, -2), 0.5, colors.HexColor('#EEEEEE')),
        ]))
        elements.append(ak_table)

    doc.build(elements)
    return output_path
