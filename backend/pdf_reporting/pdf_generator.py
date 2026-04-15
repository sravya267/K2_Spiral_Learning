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

# ── Colors ────────────────────────────────────────────────────────────────────
BLACK    = colors.black
DARK_GRAY = colors.HexColor('#333333')
MID_GRAY  = colors.HexColor('#666666')
WHITE     = colors.white
TITLE_CLR = colors.HexColor('#1A237E')   # deep navy for page title

CATEGORY_NAMES = {
    'addition':       'Add.',
    'subtraction':    'Subtract.',
    'number_sense':   'Number Sense.',
    'skip_counting':  'Skip count.',
    'place_value':    'Place Value.',
    'time_telling':   'Write the time.',
    'money_counting': 'Count the money.',
    'word_problems':  'Solve the word problem.',
    'shapes':         'Shapes.',
    'fractions':      'Fractions.',
    'measurement':    'Measurement.',
    'patterns':       'Find the pattern.',
    'graphing':       'Data & Graphing.',
    'odd_even':       'Odd or Even?',
    'general':        'Solve.',
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _e(text):
    """Escape XML special chars and convert newlines to <br/>."""
    return xml_escape(str(text)).replace('\n', '<br/>')


def _vertical_math(op_char, n1_str, n2_str, styles):
    """Return a Table Flowable for a vertical math problem.

    Numbers are large and bold; the answer bar is a drawn LINEABOVE
    (avoids unicode bar characters that Courier can't encode).
    """
    w = max(len(n1_str), len(n2_str))
    raw1 = n1_str.rjust(w + 1)
    raw2 = op_char + n2_str.rjust(w)

    def _p(s):
        escaped = xml_escape(s).replace(' ', '&nbsp;')
        return Paragraph(escaped, styles['math'])

    char_pt = 12.5   # Courier-Bold at 20 pt ≈ 12.5 pt/char
    cell_w  = (w + 3) * char_pt

    tbl = Table(
        [[_p(raw1)],
         [_p(raw2)],
         [Spacer(1, 18)]],   # space below bar = answer area
        colWidths=[cell_w],
    )
    tbl.setStyle(TableStyle([
        ('TOPPADDING',    (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
        ('LINEABOVE',     (0, 2), (-1, 2), 2, BLACK),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 10),
    ]))
    return tbl


def _format_problem(problem, num, styles):
    """Return a list of Flowables for one problem."""
    prob_type = problem.get('type', '')
    category  = problem.get('category', '')

    # ── Vertical math ─────────────────────────────────────────────────────────
    if category in ('addition', 'subtraction') or prob_type in ('addition', 'subtraction'):
        op = '+' if (category == 'addition' or prob_type == 'addition') else '-'
        n1 = str(problem.get('first_number',  '?'))
        n2 = str(problem.get('second_number', '?'))
        return [_vertical_math(op, n1, n2, styles), Spacer(1, 4)]

    # ── Pre-built question fields ─────────────────────────────────────────────
    if 'text' in problem:        # word_problems
        return [
            Paragraph(_e(problem['text']), styles['q']),
            Spacer(1, 6),
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
            f'&nbsp;&nbsp;[ ]&nbsp;&nbsp;'
            f'<b>{_e(problem.get("second_number","?"))}</b>'
            f'&nbsp;&nbsp;<font size="9" color="grey">(write &lt;, &gt;, or =)</font>',
            styles['q'])]

    if prob_type == 'ordering':
        nums = ',&nbsp;&nbsp;'.join(str(n) for n in problem.get('numbers', []))
        return [
            Paragraph(f'{num}. Order from least to greatest:', styles['q']),
            Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;{nums}', styles['q']),
            Paragraph('___________________________', styles['ans']),
        ]

    if prob_type == 'before_after':
        return [
            Paragraph(
                f'{num}. What comes <b>{_e(problem.get("question_type","before"))}</b>'
                f' {_e(problem.get("number","?"))}?',
                styles['q']),
            Paragraph('_______', styles['ans']),
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
            Paragraph('_______', styles['ans']),
        ]

    # ── Time telling ──────────────────────────────────────────────────────────
    if prob_type in ('whole_hours', 'half_hours', 'quarter_hours', 'five_minute_increments'):
        h = problem.get('hour', 0)
        m = problem.get('minute', 0)
        return [
            Paragraph(f'{num}. What time does the clock show?', styles['q']),
            Paragraph(f'The clock shows <b>{h}:{m:02d}</b>', styles['q']),
            Paragraph('_______', styles['ans']),
        ]

    # ── Money ─────────────────────────────────────────────────────────────────
    if prob_type == 'identifying_coins':
        return [
            Paragraph(f'{num}. What coin is this?', styles['q']),
            Paragraph('_______', styles['ans']),
        ]
    if prob_type == 'counting_pennies_nickels':
        return [Paragraph(
            f'{num}. Count the {_e(problem.get("coin_type",""))}s:<br/>'
            f'&nbsp;&nbsp;{_e(problem.get("count",""))} coins = ______ cents',
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
            Paragraph(
                f'{num}. What fraction is shaded?<br/>'
                f'({_e(problem.get("shaded_parts",""))} of'
                f' {_e(problem.get("total_parts",""))} parts)',
                styles['q']),
            Paragraph('_______', styles['ans']),
        ]
    if prob_type == 'comparing_fractions':
        return [Paragraph(
            f'{num}.&nbsp;&nbsp;'
            f'<b>{_e(problem.get("fraction1",""))}</b>'
            f'&nbsp;&nbsp;[ ]&nbsp;&nbsp;'
            f'<b>{_e(problem.get("fraction2",""))}</b>'
            f'&nbsp;&nbsp;<font size="9" color="grey">(write &lt;, &gt;, or =)</font>',
            styles['q'])]

    # ── Measurement ───────────────────────────────────────────────────────────
    if prob_type == 'comparing_objects':
        return [
            Paragraph(
                f'{num}. Which is {_e(problem.get("property",""))}er?<br/>'
                f'{_e(problem.get("object1",""))}'
                f'&nbsp;&nbsp;or&nbsp;&nbsp;'
                f'{_e(problem.get("object2",""))}',
                styles['q']),
            Paragraph('_______', styles['ans']),
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
        return [Paragraph(f'{num}. Fill in:<br/>&nbsp;&nbsp;{fmt}', styles['q'])]

    # ── Shapes ────────────────────────────────────────────────────────────────
    if prob_type == 'basic_2d_3d':
        kind = '2D' if problem.get('shape_type') == '2d' else '3D'
        return [
            Paragraph(f'{num}. Name this {kind} shape:', styles['q']),
            Paragraph('_______', styles['ans']),
        ]
    if prob_type == 'edges_faces_vertices':
        return [
            Paragraph(
                f'{num}. How many <b>{_e(problem.get("question_type",""))}</b>'
                f' does a {_e(problem.get("shape_name",""))} have?',
                styles['q']),
            Paragraph('_______', styles['ans']),
        ]

    # ── Fallback ──────────────────────────────────────────────────────────────
    return [Paragraph(f'{num}. ______', styles['q'])]


def _make_section(category, problems, col_w, styles):
    """Build one section box: small instruction label + problems, black border."""
    label = CATEGORY_NAMES.get(category, category.replace('_', ' ').title() + '.')

    inner = [Paragraph(label, styles['sec_label']), Spacer(1, 6)]
    for i, prob in enumerate(problems):
        inner.extend(_format_problem(prob, i + 1, styles))
        inner.append(Spacer(1, 6))

    section = Table(
        [[inner]],
        colWidths=[col_w],
        spaceBefore=0, spaceAfter=0,
    )
    section.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), WHITE),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('BOX',           (0, 0), (-1, -1), 1.5, BLACK),
    ]))
    return section


# ── Page border ───────────────────────────────────────────────────────────────

def _draw_page_border(canvas, doc):
    canvas.saveState()
    m = 0.35 * inch
    w, h = letter
    canvas.setStrokeColor(BLACK)
    canvas.setLineWidth(2)
    canvas.rect(m, m, w - 2 * m, h - 2 * m)
    canvas.restoreState()


# ── Main PDF builder ──────────────────────────────────────────────────────────

def create_worksheet_pdf(problems, worksheet_type, number_range, concepts,
                         output_path, include_answer_key=False):
    """Generate a K-2 spiral review worksheet."""

    MARGIN    = 0.5 * inch
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
        # Page title
        'title':     S('title',     fontName='Helvetica-Bold', fontSize=16,
                        textColor=TITLE_CLR, alignment=TA_CENTER, spaceAfter=2),
        # Name / date line
        'name':      S('name',      fontName='Helvetica', fontSize=12,
                        textColor=DARK_GRAY),
        # Small instruction text at the top of each box  (e.g. "Add.")
        'sec_label': S('sec_label', fontName='Helvetica-Bold', fontSize=11,
                        textColor=DARK_GRAY, spaceAfter=2),
        # Regular question text
        'q':         S('q',         fontName='Helvetica', fontSize=13,
                        textColor=DARK_GRAY, leading=21, spaceAfter=2),
        # Large bold Courier for vertical math — matches the reference image look
        'math':      S('math',      fontName='Courier-Bold', fontSize=20,
                        textColor=DARK_GRAY, leading=26, alignment=TA_LEFT),
        # Small grey answer line hints
        'ans':       S('ans',       fontName='Helvetica', fontSize=10,
                        textColor=MID_GRAY, spaceAfter=2),
        # Answer key page
        'ak_head':   S('ak_head',   fontName='Helvetica-Bold', fontSize=16,
                        textColor=TITLE_CLR, alignment=TA_CENTER, spaceAfter=8),
        'ak_item':   S('ak_item',   fontName='Helvetica', fontSize=12,
                        textColor=DARK_GRAY, leading=22),
    }

    elements = []

    # ── Page title & header ───────────────────────────────────────────────────
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
        width='100%', thickness=1.5, color=DARK_GRAY, spaceAfter=6))

    # ── Group problems by category ────────────────────────────────────────────
    seen = {}
    for p in problems:
        cat = p.get('category', 'general')
        seen.setdefault(cat, []).append(p)

    col_w = (content_w - 4) / 2   # 4 pt gap between columns

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
            ('TOPPADDING',    (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING',   (0, 0), (-1, -1), 2),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 2),
        ]))
        elements.append(grid)

    # ── Answer key ────────────────────────────────────────────────────────────
    if include_answer_key:
        elements.append(PageBreak())
        elements.append(Paragraph('Answer Key', styles['ak_head']))
        elements.append(HRFlowable(
            width='100%', thickness=1.5, color=DARK_GRAY, spaceAfter=10))

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
            ('LINEBELOW',     (0, 0), (-1, -2), 0.5, colors.HexColor('#DDDDDD')),
        ]))
        elements.append(ak_table)

    doc.build(elements)
    return output_path
