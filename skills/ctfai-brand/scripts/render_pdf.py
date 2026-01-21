#!/usr/bin/env python3
"""
Generic data-driven PDF renderer with CTFAI brand styling.

Accepts YAML/JSON input and generates branded PDFs with fillable fields.
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen import canvas

# Brand colors
NAVY = colors.HexColor("#1a365d")
ORANGE = colors.HexColor("#dd6b20")
BLUE = colors.HexColor("#3182ce")
LIGHT_GRAY = colors.HexColor("#f7fafc")
DARK_GRAY = colors.HexColor("#2d3748")
WHITE = colors.HexColor("#ffffff")

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.75 * inch


def get_styles() -> dict[str, ParagraphStyle]:
    """Create brand-styled paragraph styles."""
    base = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Heading1"],
            fontSize=24,
            textColor=NAVY,
            spaceAfter=12,
            fontName="Helvetica-Bold",
        ),
        "doc_type": ParagraphStyle(
            "DocType",
            fontSize=14,
            textColor=WHITE,
            fontName="Helvetica-Bold",
            alignment=1,  # Center
        ),
        "section_title": ParagraphStyle(
            "SectionTitle",
            parent=base["Heading2"],
            fontSize=14,
            textColor=NAVY,
            spaceBefore=16,
            spaceAfter=8,
            fontName="Helvetica-Bold",
            leftIndent=8,
            borderPadding=4,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=11,
            textColor=DARK_GRAY,
            spaceAfter=8,
            leading=14,
            fontName="Helvetica",
        ),
        "intro": ParagraphStyle(
            "Intro",
            parent=base["Normal"],
            fontSize=11,
            textColor=DARK_GRAY,
            spaceAfter=12,
            leading=14,
            fontName="Helvetica-Oblique",
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontSize=11,
            textColor=DARK_GRAY,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=4,
            fontName="Helvetica",
        ),
        "label": ParagraphStyle(
            "Label",
            fontSize=10,
            textColor=NAVY,
            fontName="Helvetica-Bold",
        ),
        "value": ParagraphStyle(
            "Value",
            fontSize=11,
            textColor=DARK_GRAY,
            fontName="Helvetica",
        ),
        "signature_label": ParagraphStyle(
            "SignatureLabel",
            fontSize=10,
            textColor=DARK_GRAY,
            fontName="Helvetica",
        ),
        "footer": ParagraphStyle(
            "Footer",
            fontSize=9,
            textColor=DARK_GRAY,
            alignment=1,
            fontName="Helvetica",
        ),
    }


class BrandedDocTemplate(BaseDocTemplate):
    """Document template with CTFAI branding."""

    def __init__(self, filename: str, data: dict[str, Any], **kwargs):
        self.data = data
        self.logo_path = kwargs.pop("logo_path", None)
        super().__init__(filename, pagesize=letter, **kwargs)

        # Create frame for content
        frame = Frame(
            MARGIN,
            MARGIN + 0.5 * inch,  # Leave room for footer
            PAGE_WIDTH - 2 * MARGIN,
            PAGE_HEIGHT - 2 * MARGIN - 1.2 * inch,  # Leave room for header
            id="main",
        )
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self._draw_page)])

    def _draw_page(self, canvas: canvas.Canvas, doc):
        """Draw header, footer, and branding on each page."""
        canvas.saveState()

        # Header background
        header_height = 0.8 * inch
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_HEIGHT - header_height, PAGE_WIDTH, header_height, fill=True, stroke=False)

        # Orange accent line
        canvas.setStrokeColor(ORANGE)
        canvas.setLineWidth(3)
        canvas.line(0, PAGE_HEIGHT - header_height, PAGE_WIDTH, PAGE_HEIGHT - header_height)

        # Doc type label in header
        doc_type = self.data.get("doc_type_label", "")
        if doc_type:
            canvas.setFillColor(WHITE)
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 0.5 * inch, doc_type)

        # Logo (if available)
        if self.logo_path and Path(self.logo_path).exists():
            try:
                logo_height = 0.5 * inch
                logo_width = logo_height * 2  # Approximate aspect ratio
                canvas.drawImage(
                    self.logo_path,
                    MARGIN,
                    PAGE_HEIGHT - 0.65 * inch,
                    width=logo_width,
                    height=logo_height,
                    preserveAspectRatio=True,
                    mask="auto",
                )
            except Exception:
                pass  # Skip logo if it fails to load

        # Footer
        canvas.setFillColor(LIGHT_GRAY)
        canvas.rect(0, 0, PAGE_WIDTH, 0.5 * inch, fill=True, stroke=False)

        # Orange line above footer
        canvas.setStrokeColor(ORANGE)
        canvas.setLineWidth(2)
        canvas.line(0, 0.5 * inch, PAGE_WIDTH, 0.5 * inch)

        # Footer text
        canvas.setFillColor(DARK_GRAY)
        canvas.setFont("Helvetica", 9)
        footer_text = "Coding the Future with AI"
        canvas.drawCentredString(PAGE_WIDTH / 2, 0.2 * inch, footer_text)

        # Page number
        canvas.drawRightString(PAGE_WIDTH - MARGIN, 0.2 * inch, f"Page {doc.page}")

        canvas.restoreState()


def create_header_fields_table(fields: list[dict], styles: dict, canvas_obj: canvas.Canvas) -> Table:
    """Create a table of header fields with fillable form fields."""
    if not fields:
        return None

    table_data = []
    field_positions = []

    for i, field in enumerate(fields):
        label = field.get("label", "")
        value = field.get("value", "")

        label_para = Paragraph(f"<b>{label}:</b>", styles["label"])

        if value:
            # Pre-filled value
            value_para = Paragraph(value, styles["value"])
        else:
            # Placeholder for fillable field - will be replaced with form field
            value_para = Paragraph("_" * 40, styles["value"])
            field_positions.append((i, label))

        table_data.append([label_para, value_para])

    table = Table(table_data, colWidths=[1.5 * inch, 4 * inch])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    return table


def create_section(section: dict, styles: dict) -> list:
    """Create flowables for a section."""
    elements = []

    # Section title with orange left border effect
    title = section.get("title", "")
    if title:
        # Create a table with orange left border
        title_para = Paragraph(title, styles["section_title"])
        title_table = Table([[title_para]], colWidths=[PAGE_WIDTH - 2 * MARGIN - 8])
        title_table.setStyle(
            TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("LINEBEFORECOL", (0, 0), (0, -1), 4, ORANGE),
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        elements.append(title_table)
        elements.append(Spacer(1, 8))

    # Section content
    content = section.get("content", "")
    if content:
        elements.append(Paragraph(content, styles["body"]))

    # Bullet items
    items = section.get("items", [])
    for item in items:
        elements.append(Paragraph(f"• {item}", styles["bullet"]))

    # Fillable area indicator
    if section.get("fillable_area"):
        elements.append(Spacer(1, 8))
        box_table = Table([["[Additional notes/details can be added here]"]], colWidths=[PAGE_WIDTH - 2 * MARGIN - 16])
        box_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 1, LIGHT_GRAY),
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                    ("TOPPADDING", (0, 0), (-1, -1), 30),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 30),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#a0aec0")),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        elements.append(box_table)

    elements.append(Spacer(1, 12))
    return elements


def create_signature_block(data: dict, styles: dict) -> list:
    """Create signature block."""
    elements = []

    elements.append(Spacer(1, 24))

    # Signature section title
    sig_title = Paragraph("Signatures", styles["section_title"])
    sig_table = Table([[sig_title]], colWidths=[PAGE_WIDTH - 2 * MARGIN - 8])
    sig_table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("LINEBEFORECOL", (0, 0), (0, -1), 4, ORANGE),
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(sig_table)
    elements.append(Spacer(1, 16))

    # Two-column signature layout
    consultant_name = data.get("consultant_name", "Tim Kitchens")
    consultant_title = data.get("consultant_title", "AI Strategy Consultant")

    sig_data = [
        [
            Paragraph("<b>CONSULTANT</b>", styles["label"]),
            Paragraph("<b>CLIENT</b>", styles["label"]),
        ],
        [
            Paragraph("_" * 35, styles["value"]),
            Paragraph("_" * 35, styles["value"]),
        ],
        [
            Paragraph("Signature", styles["signature_label"]),
            Paragraph("Signature", styles["signature_label"]),
        ],
        [Spacer(1, 12), Spacer(1, 12)],
        [
            Paragraph(consultant_name, styles["value"]),
            Paragraph("_" * 35, styles["value"]),
        ],
        [
            Paragraph("Name", styles["signature_label"]),
            Paragraph("Name", styles["signature_label"]),
        ],
        [Spacer(1, 12), Spacer(1, 12)],
        [
            Paragraph(consultant_title, styles["value"]),
            Paragraph("_" * 35, styles["value"]),
        ],
        [
            Paragraph("Title", styles["signature_label"]),
            Paragraph("Title", styles["signature_label"]),
        ],
        [Spacer(1, 12), Spacer(1, 12)],
        [
            Paragraph("_" * 35, styles["value"]),
            Paragraph("_" * 35, styles["value"]),
        ],
        [
            Paragraph("Date", styles["signature_label"]),
            Paragraph("Date", styles["signature_label"]),
        ],
    ]

    sig_table = Table(sig_data, colWidths=[3 * inch, 3 * inch])
    sig_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    elements.append(sig_table)

    return elements


def render_pdf(data: dict[str, Any], output_path: str, logo_path: str | None = None):
    """Render a branded PDF from data."""
    styles = get_styles()
    elements = []

    # Title
    title = data.get("title", "Document")
    elements.append(Paragraph(title, styles["title"]))
    elements.append(Spacer(1, 8))

    # Intro text
    intro = data.get("intro_text", "")
    if intro:
        elements.append(Paragraph(intro, styles["intro"]))
        elements.append(Spacer(1, 12))

    # Header fields table
    header_fields = data.get("header_fields", [])
    if header_fields:
        table = create_header_fields_table(header_fields, styles, None)
        if table:
            elements.append(table)
            elements.append(Spacer(1, 16))

    # Sections
    sections = data.get("sections", [])
    for section in sections:
        elements.extend(create_section(section, styles))

    # Signature block
    if data.get("include_signatures"):
        elements.extend(create_signature_block(data, styles))

    # Build document
    doc = BrandedDocTemplate(output_path, data, logo_path=logo_path)
    doc.build(elements)


def main():
    parser = argparse.ArgumentParser(description="Render branded PDF from YAML/JSON data")
    parser.add_argument("--data", "-d", required=True, help="Path to YAML/JSON input file")
    parser.add_argument("--output", "-o", required=True, help="Output PDF path")
    parser.add_argument("--logo", "-l", help="Path to logo image (optional)")
    args = parser.parse_args()

    # Load input data
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: Input file not found: {args.data}", file=sys.stderr)
        sys.exit(1)

    with open(data_path) as f:
        if data_path.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(f)
        else:
            import json
            data = json.load(f)

    # Find logo
    logo_path = args.logo
    if not logo_path:
        # Look for logo in assets directory
        script_dir = Path(__file__).parent
        skill_dir = script_dir.parent
        default_logo = skill_dir / "assets" / "CTF-logo.jpg"
        if default_logo.exists():
            logo_path = str(default_logo)

    # Render PDF
    render_pdf(data, args.output, logo_path)
    print(f"PDF generated: {args.output}")


if __name__ == "__main__":
    main()
