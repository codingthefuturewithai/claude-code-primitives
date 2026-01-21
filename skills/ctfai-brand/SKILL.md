---
name: ctfai-brand
description: Apply Coding the Future with AI brand styling. Use this skill when the user asks to create branded content, apply brand colors, style documents with CTFAI branding, or create presentations/websites/themes with company branding.
user-invocable: true
---

# Coding the Future with AI - Brand Guidelines

Apply consistent branding to artifacts including PDFs, PowerPoints, websites, React themes, and more.

## Brand Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Dark Navy | `#1B2838` | 27, 40, 56 | Primary backgrounds |
| Orange | `#F5A623` | 245, 166, 35 | Primary accent, headings, CTAs |
| Iridescent Blue | `#7DD3FC` | 125, 211, 252 | Secondary accent |
| Iridescent Purple | `#C084FC` | 192, 132, 252 | Tertiary accent |
| White | `#FFFFFF` | 255, 255, 255 | Text on dark backgrounds |
| Light Gray | `#F0F5FA` | 240, 245, 250 | Light mode backgrounds |

## Typography

### Headings
- **Font**: Poppins (semibold/bold)
- **Fallback**: Arial, sans-serif
- **Sizes**: H1: 36px, H2: 30px, H3: 24px

### Body Text
- **Font**: System stack (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif)
- **Fallback**: Georgia, serif
- **Size**: 16px, line-height 1.65

## Visual Elements

### Logo
Located at: `assets/CTF-logo.jpg`
- Use on dark backgrounds
- Minimum clear space: 20px around logo

### Banner
Located at: `assets/CTF-banner.png`
- Use for headers, hero sections
- Contains brand name, logo, and decorative elements

### Design Patterns
- Orange diagonal accent lines
- Iridescent wave/gradient backgrounds
- Clean whitespace
- Modern, tech-forward aesthetic

## Brand Voice

**Tone**: Professional yet approachable
**Focus**: Clarity over hype, practical implementation

**Tagline**: "Empowering software development teams, entrepreneurs, and nonprofits with AI tools, knowledge, and strategy"

## Application Guidelines

### React/Web Themes
```css
:root {
  --ctfai-navy: #1B2838;
  --ctfai-orange: #F5A623;
  --ctfai-blue: #7DD3FC;
  --ctfai-purple: #C084FC;
  --ctfai-white: #FFFFFF;
  --ctfai-light: #F0F5FA;
}
```

### PowerPoint/PDF
- Title slides: Dark navy background, orange text
- Content slides: White/light background, navy text
- Accent elements: Orange primary, blue/purple secondary
- Include logo on title and closing slides

### General
- Dark mode: Navy background, white text, orange accents
- Light mode: White/light background, navy text, orange accents
- Always maintain adequate contrast for accessibility
