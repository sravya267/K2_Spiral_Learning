# pdf_generator.py

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

# ── Global colors ─────────────────────────────────────────────────────────────
DARK_GRAY = colors.HexColor('#333333')
MID_GRAY  = colors.HexColor('#777777')
BORDER    = colors.HexColor('#CCCCCC')
WHITE     = colors.white
TITLE_CLR = colors.HexColor('#4A148C')   # deep purple for title / HR

# Per-category: (header_bg, body_bg)
# Each section gets its own color so the sheet looks fun and easy to navigate
CAT_COLORS = {
    'addition':       (colors.HexColor('#C62828'), colors.HexColor('#FFF8F8')),
    'subtraction':    (colors.HexColor('#1565C0'), colors.HexColor('#F0F4FF')),
    'number_sense':   (colors.HexColor('#6A1B9A'), colors.HexColor('#F9F0FF')),
    'skip_counting':  (colors.HexColor('#00695C'), colors.HexColor('#F0FFFB')),
    'place_value':    (colors.HexColor('#E65100'), colors.HexColor('#FFF8F0')),
    'time_telling':   (colors.HexColor('#880E4F'), colors.HexColor('#FFF0F6')),
    'money_counting': (colors.HexColor('#1B5E20'), colors.HexColor('#F1FFF4')),
    'word_problems':  (colors.HexColor('#311B92'), colors.HexColor('#F4F0FF')),
    'shapes':         (colors.HexColor('#01579B'), colors.HexColor('#F0F8FF')),
    'fractions':      (colors.HexColor('#BF360C'), colors.HexColor('#FFF5F0')),
    'measurement':    (colors.HexColor('#004D40'), colors.HexColor('#F0FFFD')),
    'patterns':       (colors.HexColor('#4A148C'), colors.HexColor('#FAF0FF')),
    'graphing':       (colors.HexColor('#0D47A1'), colors.HexColor('#EFF5FF')),
    'odd_even':       (colors.HexColor('#33691E'), colors.HexColor('#F6FFF0')),
    'general':        (colors.HexColor('#37474F'), colors.HexColor('#F5F5F5')),
}

CATEGORY_NAMES = {
    'addition':       'Addition',
    'subtraction':    'Subtraction',
    'number_sense':   'Number Sense',
    'skip_counting':  'Skip Counting',
    'place_value':    'Place Value',
    'time_telling':   'Time Telling',
    'money_counting': 'Money',
    'word_problems':  'Word Problems',
    'shapes':         'Shapes',
    'fractions':      'Fractions',
    'measurement':    'Measurement',
    'patterns':       'Patterns & Algebra',
    'graphing':       'Graphing & Data',
    'odd_even':       'Odd & Even',
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _e(text):
    """Escape XML special chars and convert newlines to <br/>."""
    return xml_escape(str(text)).replace('\n', '<br/>')


def _vertical_math(op_char, n1_str, n2_str, styles):
    """Return a Table Flowable for a vertical math problem.

    Uses a LINEABOVE on the answer row so we never need unicode bar chars
    (which are not available in standard Courier encoding).
    """
    w = max(len(n1_str), len(n2_str))
    # Right-justify both lines to the same width.
    # Replace spaces with &nbsp; so Paragraph preserves them.
    raw1 = n1_str.rjust(w + 1)
    raw2 = op_char + n2_str.rjust(w)

    def _p(s):
        escaped = xml_escape(s).replace(' ', '&nbsp;')
        return Paragraph(escaped, styles['math'])

    char_pt = 9.6   # Courier-Bold at 16 pt ≈ 9.6 pt/char
    cell_w  = (w + 3) * char_pt

    tbl = Table(
        [[_p(raw1)],
         [_p(raw2)],
         [Spacer(1, 14)]],   # blank row below the drawn bar = answer space
        colWidths=[cell_w],
    )
    tbl.setStyle(TableStyle([
        ('TOPPADDING',    (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
        ('LINEABOVE',     (0, 2), (-1, 2), 1.5, DARK_GRAY),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 8),
    ]))
    return tbl


def _format_problem(problem, num, styles):
    """Return a list of Flowables for one problem inside a section box."""
    prob_type = problem.get('type', '')
    category  = problem.get('category', '')

    # ── Vertical math (addition / subtraction) ────────────────────────────────
    if category in ('addition', 'subtraction') or prob_type in ('addition', 'subtraction'):
        # Use plain ASCII +/- so Courier can encode them without issues
        op  = '+' if (category == 'addition' or prob_type == 'addition') else '-'
        n1  = str(problem.get('first_number',  '?'))
        n2  = str(problem.get('second_number', '?'))
        return [_vertical_math(op, n1, n2, styles), Spacer(1, 4)]

    # ── Pre-built question fields ─────────────────────────────────────────────
    if 'text' in problem:        # word_problems
        return [
            Paragraph(_e(problem['text']), styles['q']),
            Spacer(1, 4),
            Paragraph('Answer: _______________________________', styles['ans']),
        ]
    if 'question' in problem:
        return [
            Paragraph(f'{num}. {_e(problem["question"])}', styles['q']),
            Paragraph('Answer: _______________', styles['ans']),
        ]

    # ── Number sense ──────────────────────────────────────────────────────────
    if prob_type == 'comparison':
        return [Paragraph(
            f'{num}.&nbsp;&nbsp;'
            f'<b>{_e(problem.get("first_number","?"))}</b>'
            f'&nbsp;&nbsp;( )&nbsp;&nbsp;'
            f'<b>{_e(problem.get("second_number","?"))}</b>'
            f'&nbsp;&nbsp;<font size="9" color="grey">(write &lt;, &gt;, or =)</font>',
            styles['q'])]

    if prob_type == 'ordering':
        nums = ',&nbsp;&nbsp;'.join(str(n) for n in problem.get('numbers', []))
        return [
            Paragraph(f'{num}. Order from least to greatest:', styles['q']),
            Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;{nums}', styles['q']),
            Paragraph('Answer: _______________', styles['ans']),
        ]

    if prob_type == 'before_after':
        return [
            Paragraph(
                f'{num}. What comes <b>{_e(problem.get("question_type","before"))}</b>'
                f' {_e(problem.get("number","?"))}?',
                styles['q']),
            Paragraph('Answer: _______', styles['ans']),
        ]

    if prob_type == 'missing_numbers':
        seq = problem.get('sequence', problem.get('numbers', []))
        fmt = ',&nbsp;&nbsp;'.join('______' if n is None else str(n) for n in seq)
        return [Paragraph(f'{num}. {fmt}', styles['q'])]

    # ── Skip counting ─────────────────────────────────────────────────────────
    if prob_type in ('by_ones_twos', 'by_fives_tens', 'by_hundreds'):
        seq = problem.get('sequence', [])
        fmt = ',&nbsp;&nbsp;'.join('______' if n is None else str(n) for n in seq)
        return [Paragraph(f'{num}. {fmt}', styles['q'])]

    # ── Place value ───────────────────────────────────────────────────────────
    if prob_type in ('ones_tens', 'ones_tens_hundreds'):
        return [
            Paragraph(
                f'{num}. What digit is in the <b>{_e(problem.get("place",""))}</b> place?',
                styles['q']),
            Paragraph(
                f'&nbsp;&nbsp;&nbsp;&nbsp;Number: <b>{_e(problem.get("number",""))}</b>',
                styles['q']),
            Paragraph('Answer: _______', styles['ans']),
        ]

    # ── Time telling ──────────────────────────────────────────────────────────
    if prob_type in ('whole_hours', 'half_hours', 'quarter_hours', 'five_minute_increments'):
        h = problem.get('hour', 0)
        m = problem.get('minute', 0)
        return [
            Paragraph(f'{num}. Draw clock hands to show <b>{h}:{m:02d}</b>', styles['q']),
            Spacer(1, 30),
        ]

    # ── Money ─────────────────────────────────────────────────────────────────
    if prob_type == 'identifying_coins':
        return [
            Paragraph(f'{num}. What coin is this?', styles['q']),
            Paragraph('Answer: _______', styles['ans']),
        ]
    if prob_type == 'counting_pennies_nickels':
        return [Paragraph(
            f'{num}. Count the {_e(problem.get("coin_type",""))}s:<br/>'
            f'&nbsp;&nbsp;&nbsp;&nbsp;{_e(problem.get("count",""))} coins = ______ cents',
            styles['q'])]
    if prob_type == 'mixed_coins':
        coins = ', '.join(problem.get('coins', []))
        return [Paragraph(
            f'{num}. Count: {_e(coins)}<br/>Total = ______ cents',
            styles['q'])]
    if prob_type == 'making_change':
        return [Paragraph(
            f'{num}. Cost: {_e(problem.get("cost",""))}c'
            f'&nbsp;&nbsp;Paid: {_e(problem.get("payment",""))}c<br/>'
            f'Change = ______ cents',
            styles['q'])]

    # ── Fractions ─────────────────────────────────────────────────────────────
    if prob_type in ('halves_wholes', 'thirds_fourths'):
        return [
            Paragraph(f'{num}. What fraction is shaded?', styles['q']),
            Paragraph(
                f'({_e(problem.get("shaded_parts",""))}'
                f' of {_e(problem.get("total_parts",""))} parts)',
                styles['ans']),
            Paragraph('Answer: _______', styles['ans']),
        ]
    if prob_type == 'comparing_fractions':
        return [Paragraph(
            f'{num}.&nbsp;&nbsp;'
            f'<b>{_e(problem.get("fraction1",""))}</b>'
            f'&nbsp;&nbsp;( )&nbsp;&nbsp;'
            f'<b>{_e(problem.get("fraction2",""))}</b>'
            f'&nbsp;&nbsp;<font size="9" color="grey">(write &lt;, &gt;, or =)</font>',
            styles['q'])]

    # ── Measurement ───────────────────────────────────────────────────────────
    if prob_type == 'comparing_objects':
        return [
            Paragraph(
                f'{num}. Which is {_e(problem.get("property",""))}er?', styles['q']),
            Paragraph(
                f'{_e(problem.get("object1",""))}'
                f'&nbsp;&nbsp;or&nbsp;&nbsp;'
                f'{_e(problem.get("object2",""))}',
                styles['q']),
            Paragraph('Answer: _______', styles['ans']),
        ]
    if prob_type == 'non_standard_units':
        return [Paragraph(
            f'{num}. How long is the {_e(problem.get("item_to_measure",""))}?<br/>'
            f'About ______ {_e(problem.get("measuring_object",""))}s long',
            styles['q'])]
    if prob_type == 'rulers_inches_cm':
        return [Paragraph(
            f'{num}. Measure the line ({_e(problem.get("unit",""))}):<br/>'
            f'______ {_e(problem.get("unit",""))}',
            styles['q'])]

    # ── Patterns ─────────────────────────────────────────────────────────────
    if prob_type == 'abab_patterns':
        pat = ',&nbsp;&nbsp;'.join(str(p) for p in problem.get('pattern', []))
        return [Paragraph(f'{num}. What comes next?<br/>&nbsp;&nbsp;{pat}, ______', styles['q'])]
    if prob_type == 'extending_patterns':
        pat = ',&nbsp;&nbsp;'.join(str(p) for p in problem.get('pattern', []))
        return [Paragraph(f'{num}. Extend the pattern:<br/>&nbsp;&nbsp;{pat}, ______', styles['q'])]
    if prob_type == 'creating_patterns':
        seq = problem.get('pattern', [])
        fmt = ',&nbsp;&nbsp;'.join('______' if n is None else str(n) for n in seq)
        return [Paragraph(f'{num}. Fill in missing numbers:<br/>&nbsp;&nbsp;{fmt}', styles['q'])]

    # ── Shapes ────────────────────────────────────────────────────────────────
    if prob_type == 'basic_2d_3d':
        kind = '2D' if problem.get('shape_type') == '2d' else '3D'
        return [
            Paragraph(f'{num}. Name this {kind} shape:', styles['q']),
            Paragraph('Answer: _______', styles['ans']),
        ]
    if prob_type == 'edges_faces_vertices':
        return [
            Paragraph(
                f'{num}. How many <b>{_e(problem.get("question_type",""))}</b>'
                f' does a {_e(problem.get("shape_name",""))} have?',
                styles['q']),
            Paragraph('Answer: _______', styles['ans']),
        ]

    # ── Fallback ──────────────────────────────────────────────────────────────
    return [Paragraph(f'{num}. ______', styles['q'])]


def _make_section(category, problems, col_w, styles):
    """Build one category section as a two-row Table: colored header + problem body."""
    display = CATEGORY_NAMES.get(category, category.replace('_', ' ').title())
    hdr_clr, body_clr = CAT_COLORS.get(category, CAT_COLORS['general'])

    header = Paragraph(display, styles['sec_head'])

    inner = []
    for i, prob in enumerate(problems):
        inner.extend(_format_problem(prob, i + 1, styles))
        inner.append(Spacer(1, 5))

    section = Table(
        [[header], [inner]],
        colWidths=[col_w],
        spaceBefore=4, spaceAfter=4,
    )
    section.setStyle(TableStyle([
        # header row
        ('BACKGROUND',    (0, 0), (-1, 0), hdr_clr),
        ('TEXTCOLOR',     (0, 0), (-1, 0), WHITE),
        ('TOPPADDING',    (0, 0), (-1, 0), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
        ('LEFTPADDING',   (0, 0), (-1, 0), 10),
        ('RIGHTPADDING',  (0, 0), (-1, 0), 10),
        # body row
        ('BACKGROUND',    (0, 1), (-1, 1), body_clr),
        ('TOPPADDING',    (0, 1), (-1, 1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
        ('LEFTPADDING',   (0, 1), (-1, 1), 10),
        ('RIGHTPADDING',  (0, 1), (-1, 1), 10),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        # border
        ('BOX',           (0, 0), (-1, -1), 1.2, BORDER),
    ]))
    return section


# ── Page border ───────────────────────────────────────────────────────────────

def _draw_page_border(canvas, doc):
    canvas.saveState()
    m = 0.3 * inch
    w, h = letter
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(1.5)
    canvas.rect(m, m, w - 2 * m, h - 2 * m)
    canvas.setLineWidth(0.5)
    canvas.rect(m + 4, m + 4, w - 2 * m - 8, h - 2 * m - 8)
    canvas.restoreState()


# ── Main PDF builder ──────────────────────────────────────────────────────────

def create_worksheet_pdf(problems, worksheet_type, number_range, concepts,
                         output_path, include_answer_key=False):
    """Generate a K-2 spiral review worksheet with colorful category section boxes."""

    MARGIN    = 0.55 * inch
    PAGE_W, PAGE_H = letter
    content_w = PAGE_W - 2 * MARGIN

    doc = BaseDocTemplate(
        output_path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    frame = Frame(
        MARGIN, MARGIN, content_w, PAGE_H - 2 * MARGIN,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
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
        'title':    S('title',    fontName='Helvetica-Bold',  fontSize=18,
                       textColor=TITLE_CLR, alignment=TA_CENTER, spaceAfter=4),
        'name':     S('name',     fontName='Helvetica',       fontSize=12,
                       textColor=DARK_GRAY),
        'sec_head': S('sec_head', fontName='Helvetica-Bold',  fontSize=13,
                       textColor=WHITE, alignment=TA_CENTER),
        # Main question text — slightly larger and well-leaded for young readers
        'q':        S('q',        fontName='Helvetica',       fontSize=13,
                       textColor=DARK_GRAY, leading=21, spaceAfter=2),
        # Vertical math — Courier-Bold so digits line up cleanly
        'math':     S('math',     fontName='Courier-Bold',    fontSize=16,
                       textColor=DARK_GRAY, leading=22, alignment=TA_LEFT),
        # Smaller grey hint text under questions
        'ans':      S('ans',      fontName='Helvetica',       fontSize=10,
                       textColor=MID_GRAY, spaceAfter=2),
        # Answer key page
        'ak_head':  S('ak_head',  fontName='Helvetica-Bold',  fontSize=16,
                       textColor=TITLE_CLR, alignment=TA_CENTER, spaceAfter=8),
        'ak_item':  S('ak_item',  fontName='Helvetica',       fontSize=12,
                       textColor=DARK_GRAY, leading=22),
    }

    elements = []

    # ── Page title & name line ────────────────────────────────────────────────
    type_label = 'Spiral Review' if worksheet_type == 'spiral' else 'Fluency Practice'
    elements.append(Paragraph(
        f'Math {type_label}  \u2014  {number_range.capitalize()}',
        styles['title']))
    elements.append(Spacer(1, 4))

    info = Table(
        [[Paragraph('Name: ____________________________________', styles['name']),
          Paragraph('Date: _________________', styles['name']),
          Paragraph(f'Score: _____ / {len(problems)}', styles['name'])]],
        colWidths=[content_w * 0.45, content_w * 0.33, content_w * 0.22],
    )
    info.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(info)
    elements.append(HRFlowable(
        width='100%', thickness=2, color=TITLE_CLR, spaceAfter=8))

    # ── Group problems by category ────────────────────────────────────────────
    seen = {}
    for p in problems:
        cat = p.get('category', 'general')
        seen.setdefault(cat, []).append(p)

    col_w = (content_w - 8) / 2

    sections = [_make_section(cat, probs, col_w, styles)
                for cat, probs in seen.items()]

    if not sections:
        elements.append(Paragraph('No problems generated.', styles['q']))
    else:
        if len(sections) % 2:
            sections.append(Spacer(1, 1))

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
        elements.append(HRFlowable(
            width='100%', thickness=2, color=TITLE_CLR, spaceAfter=10))

        em_dash = '\u2014'
        ak_cells = [
            Paragraph(
                f'<b>{i + 1}.</b>  {_e(p.get("answer", em_dash))}',
                styles['ak_item'])
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
