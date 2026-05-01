"""Build a PPTX deck from the SMB Google vs Meta account-setup report."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Brand-ish palette (Google blue / red / yellow / green; Meta blue accent)
G_BLUE = RGBColor(0x42, 0x85, 0xF4)
G_RED = RGBColor(0xEA, 0x43, 0x35)
G_YELLOW = RGBColor(0xFB, 0xBC, 0x05)
G_GREEN = RGBColor(0x34, 0xA8, 0x53)
M_BLUE = RGBColor(0x18, 0x77, 0xF2)
DARK = RGBColor(0x20, 0x21, 0x24)
GREY = RGBColor(0x5F, 0x63, 0x68)
LIGHT = RGBColor(0xF1, 0xF3, 0xF4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height

BLANK = prs.slide_layouts[6]


def add_rect(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
    shp.shadow.inherit = False
    return shp


def add_text(slide, x, y, w, h, text, *, size=18, bold=False, color=DARK, align=PP_ALIGN.LEFT, font="Calibri"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return tb


def add_bullets(slide, x, y, w, h, items, *, size=14, color=DARK, bullet="•"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(4)
        run = p.add_run()
        run.text = f"{bullet}  {item}"
        run.font.name = "Calibri"
        run.font.size = Pt(size)
        run.font.color.rgb = color
    return tb


def add_header(slide, title, kicker=None):
    add_rect(slide, 0, 0, SW, Inches(0.08), G_BLUE)
    if kicker:
        add_text(slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.3),
                 kicker, size=11, bold=True, color=G_BLUE)
    add_text(slide, Inches(0.5), Inches(0.45), Inches(12.3), Inches(0.7),
             title, size=28, bold=True, color=DARK)


def add_footer(slide, page_num, total):
    add_text(slide, Inches(0.5), Inches(7.15), Inches(8), Inches(0.3),
             "SMB Google Ads vs. Meta Ads · Account-Setup Research · 2026-04-30",
             size=9, color=GREY)
    add_text(slide, Inches(12.3), Inches(7.15), Inches(0.8), Inches(0.3),
             f"{page_num} / {total}", size=9, color=GREY, align=PP_ALIGN.RIGHT)


# ---------- Slide 1: Title ----------
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SW, SH, DARK)
add_rect(s, 0, Inches(3.3), SW, Inches(0.04), G_BLUE)
add_text(s, Inches(0.7), Inches(0.7), Inches(11), Inches(0.4),
         "EXECUTIVE BRIEFING · SMB ACQUISITION & ACTIVATION", size=12, bold=True, color=G_YELLOW)
add_text(s, Inches(0.7), Inches(1.4), Inches(12), Inches(2),
         "What an SMB Needs to\nStand Up a Successful\nGoogle Ads vs. Meta Ads Account",
         size=40, bold=True, color=WHITE)
add_text(s, Inches(0.7), Inches(4.1), Inches(12), Inches(1),
         "Where to invest on business.google.com in H2 2026 to reduce SMB time-to-first-value and 30/60/90-day churn",
         size=18, color=LIGHT)
add_text(s, Inches(0.7), Inches(6.4), Inches(6), Inches(0.4),
         "Prepared 2026-04-30  ·  ads-market-research", size=11, color=GREY)
add_text(s, Inches(7), Inches(6.4), Inches(5.7), Inches(0.4),
         "Lifecycle: Acquisition → Activation → Spend → Retention → ROI",
         size=11, color=GREY, align=PP_ALIGN.RIGHT)


# ---------- Slide 2: TL;DR ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "TL;DR — the practical inputs are where SMBs fail", kicker="EXECUTIVE SUMMARY")
add_rect(s, Inches(0.5), Inches(1.4), Inches(12.3), Inches(1.2), LIGHT)
add_text(s, Inches(0.8), Inches(1.55), Inches(11.7), Inches(1),
         "Hard prerequisites for an SMB to run ads on Google or Meta are nearly identical. The PRACTICAL prerequisites — clean tracking, enough budget to survive learning, and creative variety — are where SMBs fail.",
         size=16, bold=True, color=DARK)
bullets = [
    "Meta has been ~12–18 months ahead on AI-default onboarding for ecom SMBs (Advantage+ Shopping adoption +70% YoY in Q4).",
    "Google's 2025 Smart Mode + 2026 pre-built campaigns rollout closes most of the gap on the flow — explicit response to documented SMB onboarding abandonment.",
    "Google's biggest remaining SMB tax: measurement/tracking setup. Implicitly admitted by the $600 conversion-tracking credit incentive.",
    "Meta's biggest tax is the inverse: easy onboarding ≠ durable ROI. Advantage+ new-customer CAC roughly doubled May 2024 → May 2025 in a 55K-campaign analysis.",
    "73% of agency-managed SMB churn is communication-driven, not performance-driven — a plain-English explanation gap, not an algorithm gap.",
]
add_bullets(s, Inches(0.7), Inches(2.9), Inches(12), Inches(4), bullets, size=14)
add_footer(s, 2, 11)


# ---------- Slide 3: PM context ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "What this research informs", kicker="PM CONTEXT")

col_w = Inches(4)
gap = Inches(0.3)
top = Inches(1.5)
height = Inches(5.3)
items = [
    ("Decision", "Where to invest on business.google.com & adjacent surfaces in H2 2026 to reduce SMB time-to-first-value and early-churn.", G_BLUE),
    ("Scope", "SMB-weighted (1–50 employees, owner-operator) · US-first · last 12 months · acquisition→activation→spend.", G_GREEN),
    ("Lens", "Dual: external advertiser experiences AND internal product-marketer tools that may surface externally.", G_RED),
]
for i, (h, body, c) in enumerate(items):
    x = Inches(0.5) + (col_w + gap) * i
    add_rect(s, x, top, col_w, height, LIGHT)
    add_rect(s, x, top, col_w, Inches(0.6), c)
    add_text(s, x + Inches(0.2), top + Inches(0.12), col_w - Inches(0.4), Inches(0.4),
             h.upper(), size=14, bold=True, color=WHITE)
    add_text(s, x + Inches(0.25), top + Inches(0.85), col_w - Inches(0.5), Inches(4),
             body, size=14, color=DARK)
add_footer(s, 3, 11)


# ---------- Slide 4: Side-by-side comparison ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "What an SMB needs to bring vs. what AI manufactures", kicker="LANDSCAPE")

# Two-column comparison
col_w = Inches(6.1)
top = Inches(1.4)
height = Inches(5.5)
left_x = Inches(0.5)
right_x = Inches(6.7)

add_rect(s, left_x, top, col_w, Inches(0.6), G_BLUE)
add_text(s, left_x + Inches(0.2), top + Inches(0.1), col_w - Inches(0.4), Inches(0.4),
         "GOOGLE ADS (2026)", size=16, bold=True, color=WHITE)
add_rect(s, left_x, top + Inches(0.6), col_w, height - Inches(0.6), LIGHT)

add_rect(s, right_x, top, col_w, Inches(0.6), M_BLUE)
add_text(s, right_x + Inches(0.2), top + Inches(0.1), col_w - Inches(0.4), Inches(0.4),
         "META ADS (2026)", size=16, bold=True, color=WHITE)
add_rect(s, right_x, top + Inches(0.6), col_w, height - Inches(0.6), LIGHT)

google_pts = [
    "Setup: Google account + business name + site (optional but expected).",
    "Tracking: Google tag/GTM + enhanced conversions + Consent Mode v2. SINGLE BIGGEST SMB TAX.",
    "Creative: Smart Mode/asset gen can bootstrap from URL + logo; PMax wants 15 headlines + 4 descriptions + multi-format assets.",
    "Targeting: Smart Mode infers from category/location; PMax accelerated by audience signals.",
    "Budget floor (practical): ~$500–$1,500/mo Search; PMax wants ≥10–30 conv/mo.",
    "Onboarding flow: Smart Mode default + pre-built campaigns rolling out late 2025 → early 2026.",
    "Failure modes: missing tracking · thin budget · over-broad match · landing-page mismatch.",
]
add_bullets(s, left_x + Inches(0.25), top + Inches(0.75), col_w - Inches(0.5), Inches(4.6),
            google_pts, size=11.5)

meta_pts = [
    "Setup: Facebook account + Business Manager + Page (required) + IG link (recommended).",
    "Tracking: Meta Pixel + Conversions API (CAPI). CAPI Gateway / partners help non-technical SMBs post-ATT.",
    "Creative: Advantage+ Shopping runs from product feed + a few seed creatives; AI generates variants.",
    "Targeting: Advantage+ uses pixel/CAPI signal + catalog; minimal advertiser input.",
    "Budget floor (practical): ~$1,000–$3,000/mo; Advantage+ ad sets want ~50 conv/wk to exit learning.",
    "Onboarding flow: Advantage+ Campaign Experience default; +70% YoY adoption Q4.",
    "Failure modes: no CAPI fallback · cannibalizing organic · rising new-customer CAC · creative fatigue.",
]
add_bullets(s, right_x + Inches(0.25), top + Inches(0.75), col_w - Inches(0.5), Inches(4.6),
            meta_pts, size=11.5)
add_footer(s, 4, 11)


# ---------- Slide 5: AI/ML angle ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "AI/ML: where Google leads, lags, or should differentiate", kicker="AI ANGLE")

cols = [
    ("WHERE GOOGLE IS AHEAD", G_GREEN, [
        "Unique intent/query signal — no Meta analog.",
        "AI Mode positioned as next ads engine with monetization plan in place.",
        "Multi-product graph: Business Profile + Merchant Center + Analytics + YouTube.",
    ]),
    ("WHERE META IS AHEAD", G_RED, [
        "Default-on AI onboarding for ecom (5-clicks-to-live with feed).",
        "Creative AI maturity (image, video variants, AI sandbox shipped first).",
        "Catalog-first model — faster than Merchant Center for Shopify/Woo.",
    ]),
    ("DIFFERENTIATION GAP", G_BLUE, [
        "In-flow troubleshooting in plain English to a non-marketer — neither does this well.",
        "Weekly 'what happened, what to do' explanation for owner-operators.",
        "SMB-grade incrementality readout — biggest trust-narrative prize.",
    ]),
]
col_w = Inches(4.05)
gap = Inches(0.15)
top = Inches(1.5)
height = Inches(5.3)
for i, (h, c, items) in enumerate(cols):
    x = Inches(0.5) + (col_w + gap) * i
    add_rect(s, x, top, col_w, height, LIGHT)
    add_rect(s, x, top, col_w, Inches(0.55), c)
    add_text(s, x + Inches(0.15), top + Inches(0.1), col_w - Inches(0.3), Inches(0.4),
             h, size=12, bold=True, color=WHITE)
    add_bullets(s, x + Inches(0.15), top + Inches(0.7), col_w - Inches(0.3), Inches(4.5),
                items, size=12)
add_footer(s, 5, 11)


# ---------- Slide 6: Lifecycle view ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "Where each stage of the funnel hurts SMBs today", kicker="LIFECYCLE VIEW")

stages = [
    ("ACQUISITION", G_BLUE, "Google brand wins entry; friction is keeping them past session 1. Boost-from-Business-Profile underused vs. Meta's Page-Boost analog."),
    ("ACTIVATION", G_GREEN, "The battleground. Smart Mode + pre-built campaigns target documented SMB onboarding abandonment. Tracking setup remains the largest activation tax."),
    ("SPEND", G_YELLOW, "Both platforms punish under-budgeted accounts during learning. Practitioners cite $1K–$3K/mo as the realistic SMB floor for either."),
    ("RETENTION", G_RED, "Tracking is the leading indicator. 73% of agency-managed SMB churn is communication-driven — an AI-explanation opportunity."),
    ("ROI", DARK, "Easy onboarding ≠ durable ROI. Advantage+ new-customer CAC ~doubled May'24→May'25 without exclusions. PMax shares the pattern."),
]
top = Inches(1.5)
row_h = Inches(1.0)
for i, (label, c, body) in enumerate(stages):
    y = top + row_h * i + Inches(0.05) * i
    add_rect(s, Inches(0.5), y, Inches(2.3), row_h, c)
    add_text(s, Inches(0.55), y + Inches(0.32), Inches(2.2), Inches(0.5),
             label, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, Inches(2.85), y, Inches(9.95), row_h, LIGHT)
    add_text(s, Inches(3.0), y + Inches(0.22), Inches(9.7), row_h - Inches(0.3),
             body, size=12.5, color=DARK)
add_footer(s, 6, 11)


# ---------- Slide 7: Top 3 PM implications ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "Top 3 PM-actionable implications", kicker="RECOMMENDATIONS")

recs = [
    ("01", "Collapse measurement setup into a one-screen, agent-driven flow.",
     "[Activation] · High impact / Medium effort",
     "Tracking is the single biggest SMB activation tax. The $600 credit shows Google already knows. Detect the SMB's stack (Shopify, WordPress, GA4, GTM) and offer one-click installation BEFORE first campaign launch.",
     G_BLUE),
    ("02", "Ship a 'first 90 days' guided playbook that replaces the agency role most SMBs can't afford.",
     "[Activation, Retention] · High impact / Medium effort",
     "73% of agency SMB churn is communication, not performance. An always-on, plain-English assistant — proactive, in-product + email — that says what happened, what to fix, what to ignore.",
     G_GREEN),
    ("03", "Build a stalled-account diagnostic agent — internal first, then surface externally.",
     "[Spend, Retention] · High impact / Low–Medium effort",
     "Flag the killable failure modes (broken tracking · sub-floor budget · thin creative · landing mismatch) and route accounts to self-serve fix, email nudge, or sales-assist. Canonical internal-then-external pattern.",
     G_RED),
]
top = Inches(1.5)
card_h = Inches(1.7)
gap = Inches(0.15)
for i, (num, title, tag, body, c) in enumerate(recs):
    y = top + (card_h + gap) * i
    add_rect(s, Inches(0.5), y, Inches(12.3), card_h, LIGHT)
    add_rect(s, Inches(0.5), y, Inches(1.0), card_h, c)
    add_text(s, Inches(0.5), y + Inches(0.5), Inches(1.0), Inches(0.7),
             num, size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, Inches(1.7), y + Inches(0.15), Inches(11), Inches(0.45),
             title, size=15, bold=True, color=DARK)
    add_text(s, Inches(1.7), y + Inches(0.6), Inches(11), Inches(0.3),
             tag, size=10.5, bold=True, color=c)
    add_text(s, Inches(1.7), y + Inches(0.9), Inches(11), Inches(0.8),
             body, size=11.5, color=DARK)
add_footer(s, 7, 11)


# ---------- Slide 8: External vs internal framing ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "External advertiser vs. internal-PMM-tool framing", kicker="HOW IT SHIPS")

# Header row
top = Inches(1.5)
row_h = Inches(0.55)
cols_x = [Inches(0.5), Inches(5.5), Inches(8.0), Inches(10.5)]
cols_w = [Inches(5.0), Inches(2.5), Inches(2.5), Inches(2.3)]
headers = ["Recommendation", "Best v1 surface", "Other-surface path", "Pattern"]
for x, w, h in zip(cols_x, cols_w, headers):
    add_rect(s, x, top, w, row_h, DARK)
    add_text(s, x + Inches(0.1), top + Inches(0.13), w - Inches(0.2), row_h - Inches(0.2),
             h, size=12, bold=True, color=WHITE)

rows = [
    ("One-screen measurement setup", "External", "Internal: diagnostic for sales-assist", "Ship-out"),
    ("'First 90 days' guided playbook", "External", "Internal: PMM engagement dashboard", "Ship-out"),
    ("Stalled-account diagnostic agent", "Internal", "External: advertiser 'health check'", "Ship-in-then-out"),
    ("Boost-from-Business-Profile acq.", "External", "Internal: PMM A/B at scale", "Ship-out"),
    ("Catalog-first ecom onboarding", "External", "Internal: partner-integration health", "Ship-out"),
    ("SMB incrementality readout", "Internal", "External once methodology proven", "Ship-in-then-out"),
]
y = top + row_h
for i, row in enumerate(rows):
    fill = WHITE if i % 2 == 0 else LIGHT
    for x, w in zip(cols_x, cols_w):
        add_rect(s, x, y, w, row_h, fill)
    for j, (x, w, val) in enumerate(zip(cols_x, cols_w, row)):
        bold = (j == 0)
        add_text(s, x + Inches(0.1), y + Inches(0.13), w - Inches(0.2), row_h - Inches(0.2),
                 val, size=11, bold=bold, color=DARK)
    y += row_h

add_text(s, Inches(0.5), Inches(6.55), Inches(12.3), Inches(0.5),
         "Pattern: measurement & onboarding flows ship external first; diagnostic & explanation tools ship internal first.",
         size=12, bold=True, color=G_BLUE)
add_footer(s, 8, 11)


# ---------- Slide 9: Risks & what to watch ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "Risks, unknowns, and what to watch", kicker="WATCH LIST")

cols = [
    ("RISKS", G_RED, [
        "AI Mode reshapes the funnel before business.google.com does.",
        "SMB skepticism toward 'AI does it for you' hardens (Marpipe-style data circulating).",
        "Privacy/regulatory step-changes: DMA, EU AI Act, US state privacy.",
    ]),
    ("UNKNOWNS", G_YELLOW, [
        "How much Smart Mode → Expert Mode graduation actually happens.",
        "Real SMB pull of TikTok Symphony, MS Copilot, Criteo GO — they raise the floor even if not winning.",
        "True 90-day retention curves on Smart Mode cohorts.",
    ]),
    ("LEADING INDICATORS", G_GREEN, [
        "AI Mode ad share of Search revenue in earnings.",
        "r/PPC sentiment toward Smart Mode + PMax for SMBs.",
        "Consent Mode v2 enforcement actions; FTC on auto-applied recommendations.",
    ]),
]
col_w = Inches(4.05)
gap = Inches(0.15)
top = Inches(1.5)
height = Inches(5.3)
for i, (h, c, items) in enumerate(cols):
    x = Inches(0.5) + (col_w + gap) * i
    add_rect(s, x, top, col_w, height, LIGHT)
    add_rect(s, x, top, col_w, Inches(0.55), c)
    add_text(s, x + Inches(0.15), top + Inches(0.1), col_w - Inches(0.3), Inches(0.4),
             h, size=12, bold=True, color=WHITE)
    add_bullets(s, x + Inches(0.15), top + Inches(0.7), col_w - Inches(0.3), Inches(4.5),
                items, size=12)
add_footer(s, 9, 11)


# ---------- Slide 10: Sources ----------
s = prs.slides.add_slide(BLANK)
add_header(s, "Sources (selected)", kicker="REFERENCES")

src_left = [
    "1. Google's AI Imperative — MediaPost, Dec 2025",
    "2. Pre-Built Campaigns 2026 Guide — ALM Corp, Jan 2026 (vendor)",
    "3. Google Ads 2025 Year-in-Review — ALM Corp, Jan 2026 (vendor)",
    "4. AI Mode is Google's next ads engine — Search Engine Land, Dec 2025",
    "5. Criteo GO opens to all SMBs — PPC Land, 2025",
    "6. Smart Campaigns benefits & features — Google Ads Help (Google-pub.)",
    "7. Advantage+ Shopping Ultimate Guide — Marpipe, 2025 (vendor; cites 55K-campaign CAC analysis)",
    "8. Advantage+ Shopping setup & results — Stackmatix, 2025",
    "9. Advantage+ Sales Campaigns Guide — Birch, 2025",
    "10. Meta Advantage+ Campaign Experience — Meta for Business (Meta-pub.)",
]
src_right = [
    "11. 2025 Google Ads Conversion Tracking — PPC Mastery, Jan 2025",
    "12. Enhanced Conversions 2025 — Conversios, 2025 (vendor)",
    "13. Google Ads Tracking After Consent Mode v2 — Dataslayer, 2026",
    "14. $600 Conversion Tracking Credit — ALM Corp, 2025 (vendor)",
    "15. Avg Conversion Rate for Google Ads 2026 — First Page Sage, 2026",
    "16. Conversion Benchmarks 2026 — Lever Digital, 2026",
    "17. Maximizing Google Ads Expert Mode — Workshop Digital (agency)",
    "18. Google Ads for a Small Business 2025 — Search Atlas, 2025",
    "19. Unpacking Meta's 2025 Ad Overhaul — IMM, 2025",
    "20. Meta Advantage+ AI updates 2025 — Coinis, 2025",
]
add_bullets(s, Inches(0.5), Inches(1.5), Inches(6.2), Inches(5), src_left, size=10.5, bullet="")
add_bullets(s, Inches(6.9), Inches(1.5), Inches(6), Inches(5), src_right, size=10.5, bullet="")
add_text(s, Inches(0.5), Inches(6.7), Inches(12.3), Inches(0.4),
         "Source quality: items 2, 3, 7, 12, 14, 17 are vendor/agency blogs — directionally useful, commercially motivated. Items 6, 10 are platform-published. Re-verify the 55K-campaign Advantage+ CAC stat before exec usage.",
         size=10, color=GREY)
add_footer(s, 10, 11)


# ---------- Slide 11: Closing ----------
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, SW, SH, DARK)
add_rect(s, 0, Inches(3.7), SW, Inches(0.04), G_YELLOW)
add_text(s, Inches(0.7), Inches(2.3), Inches(12), Inches(1),
         "The win: solve the SMB explanation gap.", size=36, bold=True, color=WHITE)
add_text(s, Inches(0.7), Inches(4.0), Inches(12), Inches(2),
         "Tracking, plain-English explanations, and stalled-account diagnosis are the three\nlevers that compound across the SMB book. Build them once, ship them everywhere\n— external on business.google.com, internal for PMM and sales-assist.",
         size=16, color=LIGHT)
add_text(s, Inches(0.7), Inches(6.6), Inches(12), Inches(0.4),
         "ads-market-research · 2026-04-30", size=11, color=GREY)


out = "/home/user/test/research/2026-04-30-smb-google-vs-meta-account-setup.pptx"
prs.save(out)
print(f"Saved: {out}")
