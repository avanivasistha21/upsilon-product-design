from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate, KeepTogether, HRFlowable, Flowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


OUT = Path(__file__).resolve().parents[1] / "output" / "pdf" / "Upsilon_Product_Design_Case_Study.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAPER = colors.HexColor("#F7F4EC")
INK = colors.HexColor("#1B293F")
FOREST = colors.HexColor("#1B2D49")
MUTED = colors.HexColor("#566276")
LINE = colors.HexColor("#DADDD9")
LIME = colors.HexColor("#E5B26D")
PALE_GREEN = colors.HexColor("#E7EDF2")
PALE_PEACH = colors.HexColor("#F2E4DA")
SAGE = colors.HexColor("#45648D")
WHITE = colors.white

# Embed the requested Lora + Open Sans families as static instances of the official Google Fonts variable files.
FONT_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"
for _name, _file in [("Lora", "Lora-Regular.ttf"), ("Lora-Bold", "Lora-Bold.ttf"),
                     ("Lora-Italic", "Lora-Italic.ttf"), ("Lora-BoldItalic", "Lora-BoldItalic.ttf"),
                     ("OpenSans", "OpenSans-Regular.ttf"), ("OpenSans-Bold", "OpenSans-Bold.ttf"),
                     ("OpenSans-Italic", "OpenSans-Italic.ttf"), ("OpenSans-BoldItalic", "OpenSans-BoldItalic.ttf")]:
    pdfmetrics.registerFont(TTFont(_name, str(FONT_DIR / _file)))
pdfmetrics.registerFontFamily("Lora", normal="Lora", bold="Lora-Bold", italic="Lora-Italic", boldItalic="Lora-BoldItalic")
pdfmetrics.registerFontFamily("OpenSans", normal="OpenSans", bold="OpenSans-Bold", italic="OpenSans-Italic", boldItalic="OpenSans-BoldItalic")

def build_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="CoverEyebrow", fontName="OpenSans-Bold", fontSize=8, leading=11, textColor=colors.HexColor("#D9E0E7"), tracking=1.2))
    s.add(ParagraphStyle(name="CoverTitle", fontName="Lora", fontSize=32, leading=37, textColor=WHITE, spaceAfter=13))
    s.add(ParagraphStyle(name="CoverSub", fontName="OpenSans", fontSize=11, leading=17, textColor=colors.HexColor("#E1E5EA"), spaceAfter=10))
    s.add(ParagraphStyle(name="Kicker", fontName="OpenSans-Bold", fontSize=8, leading=10, textColor=colors.HexColor("#A74939"), tracking=1))
    s.add(ParagraphStyle(name="H1x", fontName="Lora", fontSize=24, leading=29, textColor=INK, spaceAfter=7))
    s.add(ParagraphStyle(name="H2x", fontName="Lora-Bold", fontSize=13, leading=16, textColor=INK, spaceAfter=4))
    s.add(ParagraphStyle(name="Bodyx", fontName="OpenSans", fontSize=9, leading=14, textColor=MUTED, spaceAfter=5))
    s.add(ParagraphStyle(name="Smallx", fontName="OpenSans", fontSize=7.7, leading=11, textColor=MUTED))
    s.add(ParagraphStyle(name="SmallBold", fontName="OpenSans-Bold", fontSize=7.7, leading=10.5, textColor=INK))
    s.add(ParagraphStyle(name="TableHead", fontName="OpenSans-Bold", fontSize=7.5, leading=9, textColor=WHITE))
    s.add(ParagraphStyle(name="CardTitle", fontName="Lora-Bold", fontSize=10, leading=13, textColor=INK, spaceAfter=3))
    s.add(ParagraphStyle(name="WhiteSmall", fontName="OpenSans", fontSize=8, leading=11, textColor=colors.HexColor("#E1E5EA")))
    s.add(ParagraphStyle(name="Callout", fontName="OpenSans-Bold", fontSize=8, leading=11, textColor=FOREST))
    return s


S = build_styles()


def P(text, style="Bodyx"):
    return Paragraph(text, S[style])


class BrandMark(Flowable):
    def __init__(self, width=34, height=34, dark=False):
        super().__init__(); self.width = width; self.height = height; self.dark = dark

    def draw(self):
        c = self.canv
        main = LIME if self.dark else FOREST
        accent = colors.HexColor("#B94E3B")
        c.setStrokeColor(colors.HexColor("#8793A5")); c.setLineWidth(1.3)
        c.line(6, 15, 22, 23); c.line(6, 15, 22, 7)
        for x, y, color in [(6, 15, main), (22, 23, accent), (22, 7, accent)]:
            c.setFillColor(color); c.circle(x, y, 3.7, fill=1, stroke=0)


def cover_page(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(FOREST); canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#425673")); canvas.setLineWidth(.7)
    for r in (112, 168, 224): canvas.circle(w - 64, h - 163, r, stroke=1, fill=0)
    canvas.setFillColor(colors.HexColor("#293E5E")); canvas.circle(w - 64, h - 163, 52, stroke=0, fill=1)
    canvas.setFillColor(LIME); canvas.circle(w - 64, h - 163, 4, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#C45C43")); canvas.circle(w - 88, h - 146, 3, stroke=0, fill=1); canvas.circle(w - 39, h - 180, 3, stroke=0, fill=1)
    BrandMark(34, 34, True).drawOn(canvas, 47*mm, h - 38*mm)
    canvas.setFillColor(WHITE); canvas.setFont("OpenSans-Bold", 20); canvas.drawString(62*mm, h - 27*mm, "upsilon")
    canvas.setFillColor(LIME); canvas.drawString(82*mm, h - 27*mm, ".")
    canvas.setFillColor(colors.HexColor("#D9E0E7")); canvas.setFont("OpenSans-Bold", 8); canvas.drawString(23*mm, h - 91*mm, "PRODUCT DESIGN  /  REDESIGN CASE STUDY")
    canvas.setFillColor(WHITE); canvas.setFont("Lora", 32)
    canvas.drawString(23*mm, h - 112*mm, "Fundraising is hard.")
    canvas.drawString(23*mm, h - 127*mm, "Finding the right fit")
    canvas.drawString(23*mm, h - 142*mm, "shouldn't be.")
    canvas.setFillColor(colors.HexColor("#E5B26D")); canvas.setFont("Lora-Italic", 19); canvas.drawString(23*mm, h - 157*mm, "Find. Figure. Fund.")
    canvas.setFillColor(colors.HexColor("#E1E5EA")); canvas.setFont("OpenSans", 10)
    canvas.drawString(23*mm, h - 177*mm, "A clearer way for founders and investors to meet")
    canvas.drawString(23*mm, h - 183*mm, "with intent, context, and visible reasons.")
    canvas.setStrokeColor(colors.HexColor("#526781")); canvas.line(23*mm, 48*mm, w - 23*mm, 48*mm)
    canvas.setFillColor(colors.HexColor("#D9E0E7")); canvas.setFont("OpenSans", 8)
    canvas.drawString(23*mm, 39*mm, "SCOPE   Brand direction  /  Landing page  /  Founder match flow  /  Investor discovery")
    canvas.drawString(23*mm, 32*mm, "A responsive concept; sample profiles and match data are illustrative.")
    canvas.restoreState()


def body_page(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(PAPER); canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(FOREST); canvas.rect(0, h - 13*mm, w, 13*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE); canvas.setFont("OpenSans-Bold", 9); canvas.drawString(19*mm, h - 8.5*mm, "upsilon")
    canvas.setFillColor(LIME); canvas.drawString(29.5*mm, h - 8.5*mm, ".")
    canvas.setFillColor(colors.HexColor("#D9E0E7")); canvas.setFont("OpenSans", 7); canvas.drawRightString(w - 19*mm, h - 8.5*mm, "A CLEARER WAY TO FIND FIT")
    canvas.setStrokeColor(LINE); canvas.line(19*mm, 16*mm, w - 19*mm, 16*mm)
    canvas.setFillColor(MUTED); canvas.setFont("OpenSans", 7); canvas.drawString(19*mm, 10.5*mm, "UPSILON  /  PRODUCT DESIGN CONCEPT  /  20 OCT 2026")
    canvas.drawRightString(w - 19*mm, 10.5*mm, f"{doc.page - 1:02d}")
    canvas.restoreState()


class CaseDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(str(filename), pagesize=A4, leftMargin=19*mm, rightMargin=19*mm, topMargin=22*mm, bottomMargin=21*mm,
                         title="Upsilon Product Design Case Study", author="Product design concept")
        cover_frame = Frame(20*mm, 19*mm, A4[0]-40*mm, A4[1]-38*mm, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        body_frame = Frame(19*mm, 20*mm, A4[0]-38*mm, A4[1]-43*mm, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="cover", frames=cover_frame, onPage=cover_page), PageTemplate(id="body", frames=body_frame, onPage=body_page)])


def section_head(num, title, intro):
    return [P(num + "  /  REVIEW", "Kicker"), Spacer(1, 4*mm), P(title, "H1x"), P(intro, "Bodyx"), Spacer(1, 3*mm)]


def card(title, body, fill=WHITE, width=84*mm):
    t = Table([[P(title, "CardTitle")], [P(body, "Smallx")]], colWidths=[width])
    t.setStyle(TableStyle([("BACKGROUND", (0,0),(-1,-1), fill), ("BOX", (0,0),(-1,-1), .5, LINE), ("LEFTPADDING", (0,0),(-1,-1), 9), ("RIGHTPADDING", (0,0),(-1,-1), 9), ("TOPPADDING", (0,0),(-1,0), 8), ("BOTTOMPADDING", (0,-1),(-1,-1), 8), ("TOPPADDING", (0,1),(-1,1), 1), ("BOTTOMPADDING", (0,0),(-1,0), 2)]))
    return t


def audit_table():
    rows = [[P("HEURISTIC FINDING", "TableHead"), P("WHY IT MATTERS", "TableHead"), P("PUBLIC-PAGE EVIDENCE", "TableHead")]]
    data = [
        ("01  Promise competes with feature breadth", "A time-poor visitor needs one clear outcome and next step.", "Homepage introduces matching, grants, profiles, dashboards and deal rooms across the page."),
        ("02  Shared entry for two different jobs", "Founders seek focus and credibility; investors seek control and signal.", "Role-specific journeys appear after shared positioning and feature content."),
        ("03  AI score needs an explanation", "An unexplained score can read as false precision.", "AI relevance and fit criteria are promoted, but the result's interpretation is not immediately clear."),
        ("04  Social proof lacks decision context", "Trust depends on what is verified, recent and relevant.", "Network profiles and founder stories have limited visible cues for verification and freshness."),
        ("05  Discovery is not a funding promise", "Financial decisions need honest boundaries between discovery and funding.", "Matching, fundraising progress and deal-room outcomes sit near one another without a prominent caveat."),
        ("06  Long page weakens scan points", "Small-screen and assistive-technology users need clear structure and orientation.", "Network, dashboards, matching, deal rooms, FAQs and features form a lengthy sequence; full accessibility audit remains open."),
    ]
    for a,b,c in data: rows.append([P(a,"SmallBold"),P(b,"Smallx"),P(c,"Smallx")])
    t=Table(rows, colWidths=[49*mm,53*mm,70*mm], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),FOREST),("GRID",(0,0),(-1,-1),.45,LINE),("BACKGROUND",(0,1),(-1,-1),WHITE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    return t


def palette_table():
    colors_data = [
        ("Midnight", "#1B293F", INK, "Primary text"),
        ("Navy", "#1B2D49", FOREST, "Primary action"),
        ("Vermilion", "#B94E3B", colors.HexColor("#B94E3B"), "Action accent"),
        ("Warm paper", "#F7F4EC", PAPER, "Neutral canvas"),
    ]
    cells=[]
    for name,hx,col,use in colors_data:
        swatch=Table([[""]],colWidths=[18*mm],rowHeights=[10*mm]); swatch.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),col),("BOX",(0,0),(-1,-1),.4,LINE)]))
        cells.append([swatch, P(f"<b>{name}</b><br/>{hx}<br/>{use}","Smallx")])
    t=Table([cells],colWidths=[43*mm]*4)
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3)]))
    return t


def build_story():
    story=[Spacer(1, 1), NextPageTemplate("body"), PageBreak(), P("01  /  AUDIT", "Kicker"), Spacer(1, 4*mm), P("What a new visitor has to figure out.", "H1x"), P("A heuristic desk review of the public homepage at upsilonbyaks.com, using the content and structure available on 20 Oct 2026. The notes below are observed design concerns, not measured conversion problems.","Bodyx"), Spacer(1,3*mm), audit_table(), Spacer(1,4*mm)]
    note=Table([[P("EVIDENCE NOTE  /  The case-study web page includes annotated reconstructions of the reviewed page areas, not captured screenshots. Original screenshot capture and a complete accessibility audit remain outstanding validation work.","Smallx")]],colWidths=[172*mm])
    note.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE_PEACH),("BOX",(0,0),(-1,-1),.5,colors.HexColor("#E3D2C3")),("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    story += [note, Spacer(1,3*mm), P("Source: <link href='https://www.upsilonbyaks.com/' color='#355A3E'>upsilonbyaks.com</link>. Review basis: public homepage copy and hierarchy; private analytics and user interviews were not available.","Smallx"), PageBreak()]

    story += section_head("02", "Founders need focus. Investors need current evidence.", "The personas below are design hypotheses, not interview findings. They create a testable starting point for the two entry paths.")
    founder=card("FOUNDER  /  JOB STORY", "When I am preparing a round with limited time and network, I want a short list of investors that fit my stage and thesis, with visible reasons and next steps, so I can make informed introductions without sending the same pitch everywhere.", PALE_GREEN,84*mm)
    investor=card("INVESTOR  /  JOB STORY", "When deal flow exceeds my capacity, I want teams aligned with my stated criteria and signals about what is current or missing, so I can decide whether to take a closer look without being pushed into a conversation.",PALE_PEACH,84*mm)
    t=Table([[founder,investor]],colWidths=[86*mm,86*mm]);t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),4)])); story += [t,Spacer(1,4*mm)]
    story += [P("WHAT THE DESIGN ASSUMES", "H2x"), P("Founders need a focused path to relevant investors and honest expectations. Investors need a quick read of thesis fit and the provenance of profile details. Both should remain in control of whether an introduction happens.","Bodyx"), Spacer(1,2*mm), P("BRAND DIRECTION  /  Considered, clear, and quietly distinctive.","Kicker"), Spacer(1,2*mm), P("The three-point mark joins founder context and investor intent at the point of introduction. The web prototype and this PDF use Lora for editorial headings and Open Sans for clear interface reading. The official font files are embedded for consistent rendering.","Bodyx"), palette_table(), Spacer(1,3*mm)]
    contrast_rows=[[P("CORE CONTRAST PAIR", "SmallBold"),P("RATIO", "SmallBold"),P("USE", "SmallBold")],
                   [P("Midnight #1B293F / Paper #F7F4EC","Smallx"),P("13.31:1 · AAA","Smallx"),P("Body + headlines","Smallx")],
                   [P("White / Navy #1B2D49","Smallx"),P("13.83:1 · AAA","Smallx"),P("Primary button","Smallx")],
                   [P("Slate #566276 / Paper #F7F4EC","Smallx"),P("5.61:1 · AA","Smallx"),P("Secondary copy","Smallx")]]
    ct=Table(contrast_rows,colWidths=[75*mm,37*mm,60*mm]);ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),PALE_GREEN),("GRID",(0,0),(-1,-1),.35,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story += [ct, Spacer(1,2*mm), P("Contrast values are calculated for the stated hex pairs; review all rendered states and text sizes before production.","Smallx"),PageBreak()]

    story += section_head("03", "The redesign makes fit legible.", "The landing page names a concrete founder outcome, separates the two audiences, and lets the match flow show its work before asking anyone to connect.")
    decisions=[
        ("LANDING  /  One promise, two doors", "A direct founder CTA and a distinct investor entry replace a generic platform journey. The page explains how the product works in three steps."),
        ("FOUNDER MATCH  /  Evidence before labels", "Stage, sector, geography and cheque overlap appear as explicit signals. Thesis freshness and the limits of a fit label stay visible."),
        ("INVESTOR DISCOVERY  /  Context before contact", "Investor criteria sit alongside founder opportunities. Founder-reported information is identified for independent review."),
        ("FOUNDER PROFILE  /  Progressive disclosure", "Four short steps collect company context, raise details, preferences and a review, with privacy language close to sensitive fields."),
    ]
    for i,(title,body) in enumerate(decisions):
        story += [card(title,body,WHITE,172*mm),Spacer(1,2.5*mm)]
    story += [Spacer(1,2*mm),P("BEFORE  →  AFTER", "Kicker"),Spacer(1,2*mm)]
    mapping=[[P("BEFORE", "TableHead"),P("DESIGN RESPONSE", "TableHead")],
             [P("Many product claims compete for attention.","Smallx"),P("One clear outcome leads; features follow a short explanation of the journey.","Smallx")],
             [P("Both audiences enter through a broad shared pitch.","Smallx"),P("Founder and investor paths each name a different job and action.","Smallx")],
             [P("Score and AI language feel opaque.","Smallx"),P("Four visible fit signals plus a plain-language limitation note.","Smallx")],
             [P("Discovery language sits near fundraising outcomes.","Smallx"),P("Mutual interest is framed as an introduction, never a promise of capital.","Smallx")]]
    mt=Table(mapping,colWidths=[77*mm,95*mm]);mt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),FOREST),("GRID",(0,0),(-1,-1),.4,LINE),("BACKGROUND",(0,1),(-1,-1),WHITE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    story += [mt,PageBreak()]

    story += section_head("04", "A small system carries the same signals.", "The landing page and product flows share a compact starter system: clear hierarchy, deliberate color roles, direct actions and reason-first cards.")
    comps=[[P("COMPONENT", "TableHead"),P("DEFAULT", "TableHead"),P("INTERACTION / STATE", "TableHead"),P("ROLE", "TableHead")],
           [P("Primary button","SmallBold"),P("Navy fill, white text","Smallx"),P("Hover lift; disabled state shown","Smallx"),P("Commit / continue","Smallx")],
           [P("Secondary button","SmallBold"),P("White fill, line border","Smallx"),P("Visible focus ring on fields","Smallx"),P("Explore / edit","Smallx")],
           [P("Text input","SmallBold"),P("Label above; helper below","Smallx"),P("Focus border and halo","Smallx"),P("Progressive profile","Smallx")],
           [P("Match card","SmallBold"),P("Fit + signals + freshness","Smallx"),P("Save state; prototype CTA","Smallx"),P("Explain the why","Smallx")],
           [P("Tags","SmallBold"),P("Neutral filters / status","Smallx"),P("Selected state with border","Smallx"),P("Scan + refine","Smallx")]]
    comp=Table(comps,colWidths=[37*mm,47*mm,49*mm,39*mm]);comp.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),FOREST),("GRID",(0,0),(-1,-1),.4,LINE),("BACKGROUND",(0,1),(-1,-1),WHITE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    story += [comp,Spacer(1,6*mm),P("WHAT I WOULD VALIDATE NEXT", "Kicker"),Spacer(1,2*mm)]
    validate=[
        ("Talk with 2–3 founders and 2–3 investors", "Ask what proof they need before trusting a suggested match; test whether the visible reasons change that confidence."),
        ("Confirm the introduction consent model", "Define exactly what an introduction request sends, whose interest is visible, and how a user can pause or withdraw."),
        ("Verify profile provenance and freshness", "Agree which information is verified, what is founder-reported, and how often investor criteria are refreshed."),
        ("Audit accessibility in a real prototype", "Check keyboard order, screen-reader labels, zoom, color contrast and touch targets across desktop and mobile."),
    ]
    for title,body in validate: story += [P("<b>"+title+"</b>  /  "+body,"Bodyx")]
    story += [Spacer(1,3*mm)]
    ai=Table([[P("AI USE  /  AI assisted public-page research synthesis, copy drafting and front-end implementation. No interviews, private product analytics, live investor data or actual matching backend were used for this concept.","Smallx")]],colWidths=[172*mm])
    ai.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE_GREEN),("BOX",(0,0),(-1,-1),.5,colors.HexColor("#D4E0CF")),("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    story += [ai,Spacer(1,4*mm),P("Explore the responsive prototype in index.html. Founder matches, investor profiles, scores and dates are illustrative; the introduction action is a prototype interaction and sends no message.","Smallx")]
    return story


if __name__ == "__main__":
    doc=CaseDoc(OUT)
    doc.build(build_story())
    print(OUT)
