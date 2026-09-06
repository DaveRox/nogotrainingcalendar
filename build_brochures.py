"""
Build two one-page PDF brochures for Dave Guilford / New York Life.
1. Estate Planning segment (affluent prospects: business owners, professionals, legacy)
2. Family Financial Planning segment (broader: families, retirement, protection)

Layout structure:
  - Header band (navy): logo left, name/credentials right
  - Hero section (full width): headline + lead paragraph
  - Two columns: left (about + services), right (process + quote + credentials)
  - CTA band (navy): call to action + contact info
  - Footer: compliance text
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# ============================================================
# FONT REGISTRATION
# ============================================================
pdfmetrics.registerFont(TTFont('Georgia', 'C:/Windows/Fonts/georgia.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-Bold', 'C:/Windows/Fonts/georgiab.ttf'))
pdfmetrics.registerFont(TTFont('Georgia-Italic', 'C:/Windows/Fonts/georgiai.ttf'))
pdfmetrics.registerFont(TTFont('Calibri', 'C:/Windows/Fonts/calibri.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Bold', 'C:/Windows/Fonts/calibrib.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Light', 'C:/Windows/Fonts/calibril.ttf'))

# ============================================================
# BRAND COLORS
# ============================================================
NYL_NAVY = HexColor('#000A62')
NYL_NAVY_LIGHT = HexColor('#1A237E')
NYL_GRAY = HexColor('#474952')
NYL_LIGHT_GRAY = HexColor('#F8F7F7')
NYL_BORDER = HexColor('#E0DCD4')
WHITE = HexColor('#FFFFFF')
ACCENT_GOLD = HexColor('#C9A227')
ACCENT_BLUE = HexColor('#0A58CA')

# ============================================================
# PAGE SETUP
# ============================================================
PAGE_W, PAGE_H = letter  # 612 x 792 points
MARGIN = 0.75 * inch  # 54 points

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def draw_wrapped_text(c, text, x, y, max_width, font_name, font_size, leading, color=NYL_GRAY, max_lines=None):
    """Draw text with word wrapping. Returns y position after drawing."""
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while c.stringWidth(last + '...', font_name, font_size) > max_width and len(last) > 0:
            last = last.rsplit(' ', 1)[0] if ' ' in last else last[:-1]
        lines[-1] = last + '...'

    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y

def draw_nyl_logo(c, x, y, height=28):
    """Draw a simplified NYL logo: navy square with white building silhouette + text."""
    icon_size = height
    c.setFillColor(NYL_NAVY)
    c.roundRect(x, y, icon_size, icon_size, 2, fill=1, stroke=0)
    # Building silhouette in white
    c.setFillColor(white)
    bw = icon_size * 0.5
    bh = icon_size * 0.5
    bx = x + (icon_size - bw) / 2
    by = y + icon_size * 0.15
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    # Clock tower triangle
    p = c.beginPath()
    tw = bw * 0.35
    p.moveTo(bx + bw/2 - tw/2, by + bh)
    p.lineTo(bx + bw/2 + tw/2, by + bh)
    p.lineTo(bx + bw/2, by + bh + icon_size * 0.2)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # Clock face
    c.setFillColor(NYL_NAVY)
    c.circle(bx + bw/2, by + bh + icon_size * 0.07, icon_size * 0.07, fill=1, stroke=0)

    # Text next to icon
    text_x = x + icon_size + 7
    c.setFillColor(NYL_NAVY)
    c.setFont('Georgia-Bold', height * 0.45)
    c.drawString(text_x, y + height * 0.58, 'New York Life')
    c.setFont('Calibri', height * 0.25)
    c.setFillColor(NYL_GRAY)
    c.drawString(text_x, y + height * 0.18, 'Insurance & Annuities')

def draw_nyl_logo_white(c, x, y, height=28):
    """Draw NYL logo icon on navy background (white icon, no text)."""
    icon_size = height
    c.setFillColor(white)
    c.roundRect(x, y, icon_size, icon_size, 2, fill=1, stroke=0)
    # Building silhouette in navy
    c.setFillColor(NYL_NAVY)
    bw = icon_size * 0.5
    bh = icon_size * 0.5
    bx = x + (icon_size - bw) / 2
    by = y + icon_size * 0.15
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    # Clock tower
    p = c.beginPath()
    tw = bw * 0.35
    p.moveTo(bx + bw/2 - tw/2, by + bh)
    p.lineTo(bx + bw/2 + tw/2, by + bh)
    p.lineTo(bx + bw/2, by + bh + icon_size * 0.2)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # Clock face
    c.setFillColor(white)
    c.circle(bx + bw/2, by + bh + icon_size * 0.07, icon_size * 0.07, fill=1, stroke=0)

def draw_circle_number(c, x, y, number, diameter=20, fill_color=NYL_NAVY, text_color=white):
    """Draw a circled number."""
    c.setFillColor(fill_color)
    c.circle(x + diameter/2, y + diameter/2, diameter/2, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont('Calibri-Bold', diameter * 0.5)
    text_w = c.stringWidth(str(number), 'Calibri-Bold', diameter * 0.5)
    c.drawString(x + (diameter - text_w) / 2, y + diameter * 0.28, str(number))

def draw_section_header(c, x, y, text, accent_color, font_size=12):
    """Draw a section header with underline accent. Returns y after header."""
    c.setFillColor(NYL_NAVY)
    c.setFont('Georgia-Bold', font_size)
    c.drawString(x, y, text)
    c.setStrokeColor(accent_color)
    c.setLineWidth(2)
    c.line(x, y - 4, x + 45, y - 4)
    return y - 18

def draw_footer(c, y_pos):
    """Draw the footer with compliance text."""
    c.setFillColor(NYL_GRAY)
    c.setFont('Calibri', 6.5)
    footer_text = ("New York Life Insurance Company pays royalties for use of its trademarks. Dave Guilford is an agent of and licensed to sell insurance through "
                   "New York Life Insurance Company and may be licensed with various other independent unaffiliated insurance companies. The Royal Lion logo and "
                   "New York Life are registered service marks of New York Life Insurance Company. Guarantees are backed by the claims-paying ability of the issuer.")
    y = draw_wrapped_text(c, footer_text, MARGIN, y_pos, PAGE_W - 2 * MARGIN, 'Calibri', 6.5, 9, color=NYL_GRAY)
    y -= 4
    c.setFillColor(HexColor('#999999'))
    c.setFont('Calibri', 6.5)
    c.drawString(MARGIN, y, "© 2026 Dave Guilford  |  daveguilford.com  |  (504) 915-3403")
    return y

# ============================================================
# COMMON HEADER
# ============================================================

def draw_header(c, accent_color):
    """Draw the top header band. Returns y position below header."""
    header_height = 100
    c.setFillColor(NYL_NAVY)
    c.rect(0, PAGE_H - header_height, PAGE_W, header_height, fill=1, stroke=0)

    # Logo icon on left (white version)
    draw_nyl_logo_white(c, MARGIN, PAGE_H - 40, height=28)
    # "New York Life" text next to icon
    c.setFillColor(white)
    c.setFont('Georgia-Bold', 12)
    c.drawString(MARGIN + 36, PAGE_H - 26, 'New York Life')
    c.setFont('Calibri', 7)
    c.setFillColor(HexColor('#B0B8D0'))
    c.drawString(MARGIN + 36, PAGE_H - 37, 'Insurance & Annuities')

    # Right side: name and credentials (right-aligned, smaller to avoid collision)
    c.setFillColor(white)
    c.setFont('Georgia-Bold', 11)
    name_text = "Dave Guilford, CLF\u00ae  ChFC\u00ae  CLU\u00ae  RICP\u00ae  CLTC\u00ae  FSCP\u00ae"
    name_w = c.stringWidth(name_text, 'Georgia-Bold', 11)
    c.drawString(PAGE_W - MARGIN - name_w, PAGE_H - 27, name_text)
    c.setFont('Calibri', 7.5)
    role_text = "Director of Development  |  New York Life  |  New Orleans General Office"
    role_w = c.stringWidth(role_text, 'Calibri', 7.5)
    c.setFillColor(HexColor('#B0B8D0'))
    c.drawString(PAGE_W - MARGIN - role_w, PAGE_H - 40, role_text)

    # Accent line under header
    c.setFillColor(accent_color)
    c.rect(0, PAGE_H - header_height - 3, PAGE_W, 3, fill=1, stroke=0)

    return PAGE_H - header_height - 3

# ============================================================
# COMMON CTA BAND
# ============================================================

def draw_cta_band(c, accent_color):
    """Draw the CTA band at bottom. Returns y position above CTA."""
    cta_height = 60
    cta_y = 100
    c.setFillColor(NYL_NAVY)
    c.rect(0, cta_y, PAGE_W, cta_height, fill=1, stroke=0)

    # Accent line on top
    c.setFillColor(accent_color)
    c.rect(0, cta_y + cta_height, PAGE_W, 2, fill=1, stroke=0)

    # Left side: headline + subtext (constrained width to avoid overlap with contact info)
    c.setFillColor(white)
    c.setFont('Georgia-Bold', 13)
    c.drawString(MARGIN, cta_y + 38, "Start with a conversation, not a pitch.")
    c.setFillColor(HexColor('#B0B8D0'))
    c.setFont('Calibri', 8.5)
    draw_wrapped_text(c, "Book twenty minutes on my calendar. Zoom, phone, or coffee. Plain English, no obligation.",
                     MARGIN, cta_y + 22, 250, 'Calibri', 8.5, 11, color=HexColor('#B0B8D0'))

    # Right side: contact info (right-aligned block)
    contact_x = PAGE_W - MARGIN - 195
    c.setFillColor(white)
    c.setFont('Calibri-Bold', 9)
    c.drawString(contact_x, cta_y + 40, "(504) 915-3403")
    c.setFont('Calibri', 8)
    c.setFillColor(HexColor('#B0B8D0'))
    c.drawString(contact_x, cta_y + 28, "dguilford@eaglestrategies.com")
    c.drawString(contact_x, cta_y + 16, "calendly.com/daveguilford/quickcheckin")
    c.drawString(contact_x, cta_y + 4, "639 Loyola Ave, Ste. 1900  |  New Orleans, LA 70113")

    return cta_y  # top of footer area, below CTA

# ============================================================
# BROCHURE 1: ESTATE PLANNING
# ============================================================

def build_estate_planning_brochure():
    output_path = os.path.join(os.path.dirname(__file__), 'Guilford_Estate_Planning_Brochure.pdf')
    c = canvas.Canvas(output_path, pagesize=letter)

    below_header = draw_header(c, ACCENT_GOLD)

    # ---- HERO SECTION (full width) ----
    y = below_header - 25
    c.setFillColor(NYL_NAVY)
    c.setFont('Georgia-Bold', 24)
    c.drawString(MARGIN, y, "What you've built")
    y -= 28
    c.drawString(MARGIN, y, "deserves a plan that lasts.")
    y -= 28

    lead_text = ("You've spent decades building something real. A business, a home, a family, a life's "
                 "work. The question isn't whether you've been successful. It's whether what you've "
                 "built will survive you in the way you want it to. That's a different question, and "
                 "it needs a different kind of advisor.")
    y = draw_wrapped_text(c, lead_text, MARGIN, y, PAGE_W - 2 * MARGIN, 'Calibri', 10, 14, color=NYL_GRAY)
    y -= 14

    # ---- TWO-COLUMN BODY ----
    col_gap = 24
    col_w = (PAGE_W - 2 * MARGIN - col_gap) / 2
    left_x = MARGIN
    right_x = MARGIN + col_w + col_gap
    col_top = y  # Both columns start at same y

    # CTA band top is at y=160 (100 + 60). We need content to end above that.
    col_bottom_limit = 168

    # LEFT COLUMN
    ly = col_top
    ly = draw_section_header(c, left_x, ly, "Why work with me", ACCENT_GOLD)

    about_text = ("I've been a Marine, a stockbroker, a commodities trader, a real estate "
                  "managing partner, and a business owner who rebuilt after Katrina. I've "
                  "made payroll, ridden out volatile markets, and turned a failing operation "
                  "profitable. When you tell me about your business, your risk, or your worry "
                  "about what comes next, it isn't theoretical to me.")
    ly = draw_wrapped_text(c, about_text, left_x, ly, col_w, 'Calibri', 9, 12, color=NYL_GRAY)
    ly -= 6

    about_text2 = ("Today I'm Director of Development for New York Life's New Orleans "
                   "General Office. Before that I was an agent, financial planner, and "
                   "registered investment adviser. Six designations cover the full arc of "
                   "a financial life. If your question touches money, family, or a business, "
                   "it almost certainly lands inside work I do every day.")
    ly = draw_wrapped_text(c, about_text2, left_x, ly, col_w, 'Calibri', 9, 12, color=NYL_GRAY)
    ly -= 10

    ly = draw_section_header(c, left_x, ly, "How I help", ACCENT_GOLD)

    services = [
        ("Estate & Legacy Planning", "Wealth transfer strategies designed around your family, not a template."),
        ("Business Succession", "Who takes over, when, and how the money works. Plans that work when the day comes."),
        ("Life Insurance Structures", "The right structures to protect your family and fund your estate plan."),
        ("Long-Term Care Planning", "One health event shouldn't undo a lifetime of careful saving."),
        ("Retirement Income", "Turning savings into a paycheck that lasts as long as you do."),
    ]

    for title, desc in services:
        c.setFillColor(NYL_NAVY)
        c.setFont('Calibri-Bold', 9)
        c.drawString(left_x, ly, title)
        ly -= 11
        ly = draw_wrapped_text(c, desc, left_x, ly, col_w, 'Calibri', 8.5, 11, color=NYL_GRAY)
        ly -= 5

    # RIGHT COLUMN
    ry = col_top
    ry = draw_section_header(c, right_x, ry, "What working with me looks like", ACCENT_GOLD, font_size=11)

    steps = [
        ("A real conversation", "Twenty minutes about where you are and where you want to go. No products, no pitch, no obligation."),
        ("A plan in plain English", "Clear recommendations built around your goals. You'll understand every piece before you decide anything."),
        ("A partner over time", "Life changes. The plan adapts. My team stays at the table. You'll never be a file in a drawer."),
    ]

    for i, (title, desc) in enumerate(steps):
        draw_circle_number(c, right_x, ry - 2, i + 1, diameter=18, fill_color=ACCENT_GOLD, text_color=NYL_NAVY)
        text_x = right_x + 26
        c.setFillColor(NYL_NAVY)
        c.setFont('Calibri-Bold', 9.5)
        c.drawString(text_x, ry + 2, title)
        ry -= 12
        ry = draw_wrapped_text(c, desc, text_x, ry, col_w - 26, 'Calibri', 8.5, 11, color=NYL_GRAY)
        ry -= 7

    # Quote box
    ry -= 4
    quote_h = 62
    c.setFillColor(NYL_LIGHT_GRAY)
    c.roundRect(right_x, ry - quote_h, col_w, quote_h, 4, fill=1, stroke=0)
    c.setFillColor(ACCENT_GOLD)
    c.roundRect(right_x, ry - quote_h, 3, quote_h, 1.5, fill=1, stroke=0)

    quote_text = ("\"Most people are on the 40-40-40 Plan: work 40 hours a week for 40 years "
                  "to retire on 40% of what they already can't afford to live on. You can "
                  "break the cycle.\"")
    ry = draw_wrapped_text(c, quote_text, right_x + 12, ry - 14, col_w - 24, 'Georgia-Italic', 9, 12, color=NYL_NAVY)
    c.setFillColor(NYL_GRAY)
    c.setFont('Calibri-Bold', 7.5)
    c.drawString(right_x + 12, ry + 1, "Dave Guilford")
    ry -= 14

    # Credentials
    ry = draw_section_header(c, right_x, ry, "Six designations", ACCENT_GOLD, font_size=11)

    creds = [
        ("ChFC\u00ae", "Chartered Financial Consultant", "Your whole financial picture as one plan."),
        ("CLU\u00ae", "Chartered Life Underwriter", "Gold standard in insurance and wealth transfer."),
        ("RICP\u00ae", "Retirement Income Certified Professional", "So your money doesn't retire before you do."),
        ("CLTC\u00ae", "Certification in Long Term Care", "A health event never becomes a financial one."),
        ("CLF\u00ae", "Chartered Leadership Fellow", "Advanced training in leading financial teams."),
        ("FSCP\u00ae", "Financial Services Certified Professional", "Ethical, client-first advice. No product quota."),
    ]

    for abbrev, full, desc in creds:
        c.setFillColor(NYL_NAVY)
        c.setFont('Calibri-Bold', 8.5)
        c.drawString(right_x, ry, f"{abbrev}  {full}")
        ry -= 10
        ry = draw_wrapped_text(c, desc, right_x, ry, col_w, 'Calibri', 8, 10.5, color=NYL_GRAY, max_lines=1)
        ry -= 3

    # ---- CTA BAND ----
    draw_cta_band(c, ACCENT_GOLD)

    # ---- FOOTER ----
    draw_footer(c, 88)

    c.showPage()
    c.save()
    print(f"Estate Planning brochure saved: {output_path}")
    return output_path

# ============================================================
# BROCHURE 2: FAMILY FINANCIAL PLANNING
# ============================================================

def build_family_planning_brochure():
    output_path = os.path.join(os.path.dirname(__file__), 'Guilford_Family_Planning_Brochure.pdf')
    c = canvas.Canvas(output_path, pagesize=letter)

    below_header = draw_header(c, ACCENT_BLUE)

    # ---- HERO SECTION (full width) ----
    y = below_header - 25
    c.setFillColor(NYL_NAVY)
    c.setFont('Georgia-Bold', 24)
    c.drawString(MARGIN, y, "Will your money last")
    y -= 28
    c.drawString(MARGIN, y, "as long as you do?")
    y -= 28

    lead_text = ("Whether you're planning for retirement, protecting your family, or figuring out "
                "how to pay for long-term care, you need answers that actually make sense. Not "
                "jargon. Not a sales pitch. A plan you understand, built around your life, from "
                "someone who's been on both sides of the table.")
    y = draw_wrapped_text(c, lead_text, MARGIN, y, PAGE_W - 2 * MARGIN, 'Calibri', 10, 14, color=NYL_GRAY)
    y -= 14

    # ---- TWO-COLUMN BODY ----
    col_gap = 24
    col_w = (PAGE_W - 2 * MARGIN - col_gap) / 2
    left_x = MARGIN
    right_x = MARGIN + col_w + col_gap
    col_top = y

    # LEFT COLUMN
    ly = col_top
    ly = draw_section_header(c, left_x, ly, "Why work with me", ACCENT_BLUE)

    about_text = ("I've been a Marine, a stockbroker, a commodities trader, a real estate "
                  "managing partner, and a business owner who rebuilt after Katrina. I've "
                  "made payroll and ridden out volatile markets. I've started over. When "
                  "you tell me about your worries, it isn't theoretical to me.")
    ly = draw_wrapped_text(c, about_text, left_x, ly, col_w, 'Calibri', 9, 12, color=NYL_GRAY)
    ly -= 6

    about_text2 = ("Today I'm Director of Development for New York Life's New Orleans "
                   "General Office. I train agents for a living, and before that I was an "
                   "agent, financial planner, and registered investment adviser. Six "
                   "designations cover the full arc of a financial life. No jargon, no pressure.")
    ly = draw_wrapped_text(c, about_text2, left_x, ly, col_w, 'Calibri', 9, 12, color=NYL_GRAY)
    ly -= 10

    ly = draw_section_header(c, left_x, ly, "How I help", ACCENT_BLUE)

    services = [
        ("Retirement Planning", "Will your money last as long as you do? We build a plan you understand."),
        ("Life Insurance", "What happens to your family if something happens to you? Protection that works."),
        ("Long-Term Care", "One health event can undo a lifetime of saving. We make sure it doesn't."),
        ("Income Planning", "Saving for retirement is one skill. Turning it into a paycheck is another."),
        ("Family Protection", "A business, a home, a family. One bad event shouldn't undo it all."),
    ]

    for title, desc in services:
        c.setFillColor(NYL_NAVY)
        c.setFont('Calibri-Bold', 9)
        c.drawString(left_x, ly, title)
        ly -= 11
        ly = draw_wrapped_text(c, desc, left_x, ly, col_w, 'Calibri', 8.5, 11, color=NYL_GRAY)
        ly -= 5

    # RIGHT COLUMN
    ry = col_top
    ry = draw_section_header(c, right_x, ry, "What working with me looks like", ACCENT_BLUE, font_size=11)

    steps = [
        ("A real conversation", "Twenty minutes about where you are and where you want to go. No products, no pitch, no obligation."),
        ("A plan in plain English", "Clear recommendations built around your goals. You'll understand every piece before you decide anything."),
        ("A partner over time", "Life changes. Careers, families, businesses. The plan adapts. You'll never be a file in a drawer."),
    ]

    for i, (title, desc) in enumerate(steps):
        draw_circle_number(c, right_x, ry - 2, i + 1, diameter=18, fill_color=ACCENT_BLUE, text_color=white)
        text_x = right_x + 26
        c.setFillColor(NYL_NAVY)
        c.setFont('Calibri-Bold', 9.5)
        c.drawString(text_x, ry + 2, title)
        ry -= 12
        ry = draw_wrapped_text(c, desc, text_x, ry, col_w - 26, 'Calibri', 8.5, 11, color=NYL_GRAY)
        ry -= 7

    # Quote box
    ry -= 4
    quote_h = 62
    c.setFillColor(NYL_LIGHT_GRAY)
    c.roundRect(right_x, ry - quote_h, col_w, quote_h, 4, fill=1, stroke=0)
    c.setFillColor(ACCENT_BLUE)
    c.roundRect(right_x, ry - quote_h, 3, quote_h, 1.5, fill=1, stroke=0)

    quote_text = ("\"You don't rise to the occasion, you fall to the level of your training. "
                  "Whether in combat or in business, this is an objective truth. Be a student "
                  "of whatever game you're playing.\"")
    ry = draw_wrapped_text(c, quote_text, right_x + 12, ry - 14, col_w - 24, 'Georgia-Italic', 9, 12, color=NYL_NAVY)
    c.setFillColor(NYL_GRAY)
    c.setFont('Calibri-Bold', 7.5)
    c.drawString(right_x + 12, ry + 1, "Dave Guilford")
    ry -= 14

    # Credentials
    ry = draw_section_header(c, right_x, ry, "Six designations", ACCENT_BLUE, font_size=11)

    creds = [
        ("ChFC\u00ae", "Chartered Financial Consultant", "Your whole financial picture as one plan."),
        ("CLU\u00ae", "Chartered Life Underwriter", "Life insurance and wealth transfer, done right."),
        ("RICP\u00ae", "Retirement Income Certified Professional", "So your money doesn't retire before you do."),
        ("CLTC\u00ae", "Certification in Long Term Care", "A health event never becomes a financial one."),
        ("CLF\u00ae", "Chartered Leadership Fellow", "Advanced training in leading financial teams."),
        ("FSCP\u00ae", "Financial Services Certified Professional", "Ethical, client-first advice. No product quota."),
    ]

    for abbrev, full, desc in creds:
        c.setFillColor(NYL_NAVY)
        c.setFont('Calibri-Bold', 8.5)
        c.drawString(right_x, ry, f"{abbrev}  {full}")
        ry -= 10
        ry = draw_wrapped_text(c, desc, right_x, ry, col_w, 'Calibri', 8, 10.5, color=NYL_GRAY, max_lines=1)
        ry -= 3

    # ---- CTA BAND ----
    draw_cta_band(c, ACCENT_BLUE)

    # ---- FOOTER ----
    draw_footer(c, 88)

    c.showPage()
    c.save()
    print(f"Family Planning brochure saved: {output_path}")
    return output_path

# ============================================================
# BUILD BOTH
# ============================================================

if __name__ == '__main__':
    path1 = build_estate_planning_brochure()
    path2 = build_family_planning_brochure()
    print("\nBoth brochures built successfully.")
