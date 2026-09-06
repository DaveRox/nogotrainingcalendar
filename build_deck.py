from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import re

# NYL Brand Colors
NAVY = RGBColor(0, 51, 102)
GOLD = RGBColor(184, 134, 11)
LIGHT_GRAY = RGBColor(242, 242, 242)
WHITE = RGBColor(255, 255, 255)
DARK_TEXT = RGBColor(51, 51, 51)

# Create presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_footer(slide, slide_num):
    """Add footer with disclaimer and slide number"""
    footer = slide.shapes.add_shape(1, Inches(0), Inches(6.8), Inches(13.333), Inches(0.7))
    footer.fill.solid()
    footer.fill.fore_color.rgb = LIGHT_GRAY
    footer.line.fill.background()
    
    disc_box = slide.shapes.add_textbox(Inches(0.3), Inches(6.9), Inches(9), Inches(0.5))
    tf = disc_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Internal use only. For agent use only. Not for use with the public."
    p.font.size = Pt(10)
    p.font.color.rgb = DARK_TEXT
    
    num_box = slide.shapes.add_textbox(Inches(12), Inches(6.9), Inches(1), Inches(0.5))
    tf = num_box.text_frame
    p = tf.paragraphs[0]
    p.text = str(slide_num)
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.alignment = PP_ALIGN.RIGHT

def add_slide(title, content_lines, is_technique=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header bar
    header_height = 1.1 if is_technique else 1.2
    header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(header_height))
    header.fill.solid()
    header.fill.fore_color.rgb = NAVY
    header.line.fill.background()
    
    if is_technique:
        # TECHNIQUE TRAINING label
        section_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.2), Inches(4), Inches(0.6))
        tf = section_box.text_frame
        p = tf.paragraphs[0]
        p.text = "TECHNIQUE TRAINING"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = GOLD
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(0.3), Inches(1.25), Inches(12.5), Inches(0.7))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(30)
        p.font.bold = True
        p.font.color.rgb = NAVY
    else:
        # ELEVATE branding
        elev_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.25), Inches(2), Inches(0.7))
        tf = elev_box.text_frame
        p = tf.paragraphs[0]
        p.text = "ELEVATE"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = GOLD
        
        # NEW ORG
        neworg_box = slide.shapes.add_textbox(Inches(5.5), Inches(0.25), Inches(2.5), Inches(0.7))
        tf = neworg_box.text_frame
        p = tf.paragraphs[0]
        p.text = "NEW ORG"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
        
        # Slide title
        title_box = slide.shapes.add_textbox(Inches(0.3), Inches(1.35), Inches(12.5), Inches(0.6))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = NAVY
    
    # Content
    if content_lines:
        start_y = 2.1
        content_box = slide.shapes.add_textbox(Inches(0.5), Inches(start_y), Inches(12.333), Inches(4.5))
        tf = content_box.text_frame
        tf.word_wrap = True
        
        for i, line in enumerate(content_lines):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            
            if line.strip().startswith(('1.', '2.', '3.', '•', '-')):
                p.level = 0
                if line.strip().startswith(('•', '-')):
                    p.text = "  " + line.strip()[1:].strip()
                else:
                    p.text = "  " + line.strip()
            elif line.strip().startswith(('→', '  •')):
                p.level = 1
                p.text = line.strip().replace('→', '').strip()
            else:
                p.level = 0
                p.text = line
            
            p.font.size = Pt(18)
            p.font.color.rgb = DARK_TEXT
            p.space_after = Pt(8)
    
    add_footer(slide, len(prs.slides))
    return slide

# ========== TITLE SLIDE ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.2))
header.fill.solid()
header.fill.fore_color.rgb = NAVY
header.line.fill.background()

elev_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.25), Inches(2), Inches(0.7))
tf = elev_box.text_frame
p = tf.paragraphs[0]
p.text = "ELEVATE"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = GOLD

title_box = slide.shapes.add_textbox(Inches(1), Inches(2.8), Inches(11.333), Inches(1.5))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Market Week Overview"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

sub_box = slide.shapes.add_textbox(Inches(1), Inches(4.3), Inches(11.333), Inches(1))
tf = sub_box.text_frame
p = tf.paragraphs[0]
p.text = "Week of June 29, 2026"
p.font.size = Pt(28)
p.font.color.rgb = DARK_TEXT
p.alignment = PP_ALIGN.CENTER

add_footer(slide, 1)

# Slide 1: Week in Review
add_slide("Week in Review: U.S. Markets Overview", [
    "• S&P 500 closed at 7,499.36, up 0.79% for the week (~14% YTD)",
    "• Nasdaq gained 1.52%, led by semiconductor strength",
    "• Dow Jones added 136 points, closing above 52,300",
    "• Russell 20.00 rose 0.46%, showing market broadening",
    "• VIX dropped 6.80% to 16.45, reduced near-term volatility",
    "",
    "Plain English: Best first half since 20. Tech still leads but diversification emerging — a healthy sign."
])

# Slide 2: Key Economic Data
add_slide("Key Economic Data Released Last Week", [
    "• Job openings beat expectations in first major labor read",
    "• U.S. dollar surged to 2026 highs amid yen weakness",
    "• Consumer confidence remains elevated despite inflation concerns",
    "• Crude oil stabilized near $70/barrel, removing tail-risk inflation factor",
    "",
    "NYLIM Frame: Economy is slowing but not breaking. Fed is watching and waiting. Fixed annuities and guaranteed products remain relevant."
])

# Slide 3: Notable Earnings
add_slide("Notable Earnings from Last Week", [
    "• Semiconductor stocks: Strong — AI demand exceeds expectations",
    "• Tech sector: Mixed, but infrastructure names outperform",
    "",
    "Talking Point: Strong earnings support the market, but fast prices make expectations harder to beat. Client plans need balance — not because crash is coming, but because discipline wins."
])

# Slide 4: Economic Calendar
add_slide("Economic Reports Calendar: Week Ahead", [
    "Mon 6/29 — Personal Income/Spending: Consumer behavior signal",
    "Tue 6/30 — Case-Shiller Home Prices: Housing market health",
    "Wed 7/1 — ISM Manufacturing: Factory activity",
    "Thu 7/2 — Initial Claims: Weekly layoff data",
    "Fri 7/3 — Markets Closed: Independence Day",
    "",
    "Note: Short week. July 4th holiday = natural opening for retirement planning conversations."
])

# Slide 5: Fed/Rates
add_slide("Fed, Rates & Macro Watch", [
    "• Fed remains patient, data-dependent not calendar-driven",
    "• Rates still high = fixed annuities and whole life guarantees attractive",
    "• Dollar strength affects international investments",
    "• No immediate rate cut expected",
    "",
    "NYLIM Lens: Diversification matters. Megatrends (AI, energy, healthcare) shape winners. Geopolitics = risk management.",
    "",
    "Advisor Angle: Sell planning discipline, not market fear. Volatility gets attention; guarantees create confidence."
])

# Slide 6: Client Talking Points
add_slide("Client Talking Points: What This Means for You", [
    "• Strong first half 2026 — best since 20. Encouraging, but past performance ≠ future results.",
    "• Tech/AI carrying much of the market — fine as long as your plan is diversified.",
    "• Fed patient. Higher rates = guaranteed products worth a serious look for safety money.",
    "• Good time to review: On track? Risk tolerance still appropriate?",
    "• The plan is the point. No long-term decisions based on one headline or quarter."
])

# ========== TECHNIQUE SEGMENT TITLE ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
header.fill.solid()
header.fill.fore_color.rgb = NAVY

section_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.2), Inches(4), Inches(0.6))
tf = section_box.text_frame
p = tf.paragraphs[0]
p.text = "TECHNIQUE TRAINING"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = GOLD

title_box = slide.shapes.add_textbox(Inches(1), Inches(2.8), Inches(11.333), Inches(1.5))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Prospecting for New Clients"
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

sub_box = slide.shapes.add_textbox(Inches(1), Inches(4.2), Inches(11.333), Inches(1))
tf = sub_box.text_frame
p = tf.paragraphs[0]
p.text = "Building Your Pipeline in the First 24 Months"
p.font.size = Pt(24)
p.font.color.rgb = DARK_TEXT
p.alignment = PP_ALIGN.CENTER

add_footer(slide, 7)

# Technique Slides
add_slide("The Prospecting Hierarchy", [
    "Your best use of time, in order:",
    "",
    "1. REFERRALS — People who already trust you or know someone who does",
    "2. SOCIAL MEDIA — Content that demonstrates expertise and attracts interest",
    "3. DOOR-TO-DOOR / COLD CALLING — Direct outreach, highest effort, highest rejection",
    "",
    "The Rule: Spend 80% of prospecting time on levels 1-2. Only use level 3 when 1-2 are depleted."
], is_technique=True)

add_slide("Why Referrals Win", [
    "• Conversion rate: Referral prospects close at 3-5x the rate of cold prospects",
    "• Trust built in: They already know your name and trust the referrer",
    "• Less objection handling: No 'why should I listen to you' barrier",
    "",
    "The Math: Need 10 appointments to close 1 sale?",
    "  • Cold calling: ~100 calls",
    "  • Referrals: ~20 asks"
], is_technique=True)

add_slide("The Referral System (3-Step)", [
    "Step 1: Ask at the right moment",
    "  → After a positive interaction (compliment, thank you, case placed, claim handled)",
    "  → Never ask when something went wrong",
    "",
    "Step 2: Use the exact words",
    "  'I'm looking to help more families like yours. Do you know anyone who might benefit from a conversation about protecting their income or planning for retirement?'",
    "",
    "Step 3: Get two names",
    "  'Who else do you know who might benefit from this? Give me two names and I'll handle the introduction.'"
], is_technique=True)

add_slide("Center of Influence (COI) Strategy", [
    "Who counts as a COI?",
    "  • Accountants, attorneys, real estate agents, financial advisors outside NYL",
    "  • Business owners with employees",
    "  • Pastors, community leaders",
    "",
    "The Approach:",
    "  1. Offer value first (educational workshop, market update, lunch-and-learn)",
    "  2. Build the relationship over 2-3 touchpoints",
    "  3. Then ask: 'Who do you know who could use our services?'"
], is_technique=True)

add_slide("Social Media as a Prospecting Tool", [
    "Platform Priority for New Advisors:",
    "  1. LinkedIn — Professional credibility, connection requests, content",
    "  2. Facebook — Local community groups, personal network",
    "  3. Instagram/TikTok — Only if you're comfortable on video",
    "",
    "What to Post:",
    "  • Market updates (we provide these weekly — share them)",
    "  • Educational content (insurance basics, retirement planning)",
    "  • Client success stories (with permission)",
    "  • Community involvement",
    "",
    "Rule: 80% value, 20% promotion. No hard sells."
], is_technique=True)

add_slide("The Social Media Posting System", [
    "Daily Habits:",
    "  • Monday: Share the weekly market update",
    "  • Wednesday: Educational tip (one concept, one paragraph)",
    "  • Friday: Personal/team win or community photo",
    "",
    "Weekly Target: 3 posts minimum. Consistency beats perfection.",
    "",
    "Lead Generation: Connect with 5 new people per week. Personalize every invite."
], is_technique=True)

add_slide("Door-to-Door — When and How", [
    "When to Use It:",
    "  • New development areas with high homeownership",
    "  • Farming a specific neighborhood",
    "  • Last resort when referrals and social media aren't producing",
    "",
    "The Pitch (30 seconds):",
    "  'Hi, I'm [Name] with New York Life. We're offering free retirement planning reviews in the neighborhood. Do you have 15 minutes for me to show you what you're entitled to?'",
    "",
    "Key Mindset: You're offering value, not asking for charity. Say it with confidence."
], is_technique=True)

add_slide("Cold Calling — The Survival Guide", [
    "The Reality: Cold calling has 1-2% conversion rate. Not efficient for new advisors.",
    "",
    "If You Must:",
    "  • Call businesses, not consumers (higher success rate)",
    "  • Ask for the owner/decision-maker by name",
    "  • Lead with value: 'I'm offering a no-cost retirement planning workshop...'",
    "  • Set appointments, don't sell on the call",
    "",
    "The Script:",
    "  'Hi, this is [Name] with New York Life. We're hosting free retirement planning workshops for business owners. Would you be interested, or know a business owner who would?'"
], is_technique=True)

add_slide("The Weekly Prospecting Calendar", [
    "Minimum Daily Activity Standard:",
    "  • 10 outreach attempts (calls, texts, LinkedIn, door knocks)",
    "  • 3 real conversations (scheduled appointments or meetings)",
    "  • 2 follow-ups (on pending cases or past referrals)",
    "  • 1 accountability check (with manager or peer)",
    "",
    "Weekly Goal: 50 attempts, 15 conversations, 10 follow-ups"
], is_technique=True)

add_slide("Tracking Your Pipeline", [
    "Three Buckets to Monitor Weekly:",
    "",
    "1. LEADS — People you've contacted but haven't engaged",
    "2. PROSPECTS — People who agreed to a conversation",
    "3. OPPORTUNITIES — Cases in progress or pending",
    "",
    "Rule: If a lead hasn't responded in 3 attempts, move them down the list. Don't let dead leads take up mental space."
], is_technique=True)

add_slide("Participant Exercise", [
    "Your Assignment This Week:",
    "",
    "1. REFERRALS: Identify 5 clients/contacts to ask. Write down names and the moment you'll ask.",
    "",
    "2. SOCIAL MEDIA: Schedule your 3 posts for next week. Write down the topic for each.",
    "",
    "3. DOOR-TO-DOOR: Pick one neighborhood or 10 businesses to visit this week.",
    "",
    "Be Specific: Write down names, times, actions. Vague goals fail."
], is_technique=True)

add_slide("Coach's Takeaway", [
    "'Prospecting is not a task you do when you have time.",
    "It's the job.",
    "Everything else — meetings, paperwork, case design — happens because you prospected first.'",
    "",
    "Your Next Action: Before you leave today, send 5 text messages to past clients asking for referrals. Done."
], is_technique=True)

# Save
prs.save(r'C:\Users\dguil\TARS\TARS OUTPUTS\Monday Deck - Market Update + Prospecting (June 29 2026).pptx')
print("PowerPoint saved successfully!")
