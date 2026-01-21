# CTFAI Brand Skill

Apply Coding the Future with AI (CTFAI) brand styling to any artifact.

## Brand Identity

**Company**: Coding the Future with AI (CTFAI)
**Principal**: Tim Kitchens
**Domain**: AI strategy consulting, implementation, and education

---

## Color Palette

| Name | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Navy | `#1a365d` | `--ctfai-navy` | Primary headers, professional text |
| Orange | `#dd6b20` | `--ctfai-orange` | Accents, CTAs, highlights |
| Blue | `#3182ce` | `--ctfai-blue` | Links, secondary elements |
| Purple | `#6b46c1` | `--ctfai-purple` | Innovation/AI themes |
| Light Gray | `#f7fafc` | `--ctfai-light` | Backgrounds, cards |
| Dark Gray | `#2d3748` | `--ctfai-dark` | Body text |
| White | `#ffffff` | `--ctfai-white` | Clean backgrounds |

**Color Usage Guidelines**:
- Navy for headers and primary brand presence
- Orange sparingly for emphasis (buttons, key callouts, document type labels)
- Blue for interactive elements and links
- Purple for AI/innovation-related content
- Light gray for subtle section backgrounds
- Dark gray for readable body text

---

## Typography

**Primary Font Stack**: `'Inter', 'Segoe UI', system-ui, sans-serif`
**Monospace**: `'JetBrains Mono', 'Fira Code', monospace`

**Hierarchy**:
- H1: 2.5rem, Navy, bold (page titles)
- H2: 1.75rem, Navy, semibold (sections)
- H3: 1.25rem, Dark Gray, semibold (subsections)
- Body: 1rem, Dark Gray, regular
- Small/Caption: 0.875rem, Gray

---

## Visual Patterns

### Document Headers
- Navy background bar spanning full width
- White text for document type (e.g., "STATEMENT OF WORK")
- Logo in top-left corner
- Orange accent line below header (2-4px)

### Section Style
- Navy section titles with orange left border (4px)
- Light gray background for highlighted sections
- Generous whitespace (1.5rem+ between sections)

### Footer Style
- Light gray background
- Centered consultant info
- Orange accent line above footer

### Cards/Boxes
- Subtle shadow: `0 1px 3px rgba(0,0,0,0.1)`
- Rounded corners: `0.5rem`
- Light gray or white background

---

## Voice & Tone

- **Professional** but approachable
- **Confident** without arrogance
- **Clear** and direct - avoid jargon unless speaking to technical audience
- **Forward-looking** - emphasize transformation and possibilities
- Favor active voice

---

## Assets

| Asset | Path | Usage |
|-------|------|-------|
| Logo | `assets/CTF-logo.jpg` | Headers, letterheads, cards |
| Banner | `assets/CTF-banner.png` | Hero sections, landing pages |
| CSS | `assets/brand.css` | Web artifacts (HTML, landing pages) |

**Note**: Place logo and banner files in the `assets/` directory.

---

## Applying the Brand

### For HTML/Web Artifacts
Include `assets/brand.css` or apply these CSS variables:

```css
:root {
  --ctfai-navy: #1a365d;
  --ctfai-orange: #dd6b20;
  --ctfai-blue: #3182ce;
  --ctfai-purple: #6b46c1;
  --ctfai-light: #f7fafc;
  --ctfai-dark: #2d3748;
  --ctfai-white: #ffffff;
}
```

Use the visual patterns described above. See `assets/brand.css` for complete styling.

### For Presentations
- Title slides: Navy background, white text, orange accent
- Content slides: White background, navy headers, dark gray text
- Accent slides: Light gray background with purple/blue highlights
- Include logo on every slide (corner or footer)

### For Documents/Text
- Apply the voice & tone guidelines
- Use section patterns (navy titles, clear hierarchy)
- Include professional signature blocks

---

## PDF Generation

For PDFs requiring fillable fields, use the data-driven renderer:

### Bootstrap (first time only)
```bash
cd skills/ctfai-brand && python scripts/bootstrap.py
```

### Generate PDF
```bash
.venv/bin/python scripts/render_pdf.py --data input.yaml --output document.pdf
```

### Input Format (YAML)
Claude generates this structure based on user needs:

```yaml
title: "Document Title"
doc_type_label: "STATEMENT OF WORK"  # Orange banner text
intro_text: "Optional introductory paragraph..."

header_fields:  # Fields at top of document
  - label: "Client"
    value: ""  # Empty = fillable field
  - label: "Effective Date"
    value: ""
  - label: "Reference Number"
    value: "SOW-2024-001"  # Pre-filled

sections:  # Main content sections
  - title: "Section Title"
    content: "Section body text..."
    items:  # Optional bullet points
      - "Item one"
      - "Item two"
    fillable_area: false  # Set true for fillable text box

  - title: "Another Section"
    content: "More content here."
    fillable_area: true

include_signatures: true  # Add signature block
consultant_name: "Tim Kitchens"
consultant_title: "AI Strategy Consultant"
```

**Renderer applies automatically**:
- Logo in header
- Navy header bar with doc_type_label
- Brand colors and fonts
- Orange accents
- Professional signature blocks
- Fillable form fields where values are empty

---

## Workflow

1. **User requests branded artifact** (SOW, landing page, presentation, etc.)
2. **Interview if needed** - gather content, purpose, audience
3. **Generate directly** when possible:
   - HTML → Write HTML/CSS using brand guidelines
   - Text documents → Apply voice/tone and formatting
4. **Use PDF renderer** when fillable fields or precise PDF formatting needed
5. **Deliver** the branded artifact
