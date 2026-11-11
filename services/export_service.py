"""Readable PDF summaries; Hindi users can export the full UTF-8 text."""
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def make_english_pdf(title: str, summary: str) -> bytes:
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=A4, leftMargin=48, rightMargin=48, topMargin=54, bottomMargin=48)
    header = ParagraphStyle("Header", fontName="Helvetica-Bold", fontSize=18, leading=23, textColor=colors.HexColor("#0D5160"), spaceAfter=18)
    body = ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=16, spaceAfter=7, alignment=TA_LEFT)
    story = [Paragraph("Healthcare Info Assistant", header), Paragraph(escape(title), body), Spacer(1, 15)]
    for line in summary.splitlines():
        line = line.strip().lstrip("#*- ")
        if not line:
            story.append(Spacer(1, 5))
            continue
        # PDF uses base Latin font; Hindi and other non-Latin text are preserved in UTF-8 downloads instead.
        safe = line.encode("latin-1", errors="replace").decode("latin-1")
        story.append(Paragraph(escape(safe), body))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Educational information only. Not a diagnosis or substitute for medical advice. Verify values against the original report.", body))
    doc.build(story)
    return buff.getvalue()
