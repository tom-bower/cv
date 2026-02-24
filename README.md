# CV Generator

A version-controlled CV system that generates professional PDF and HTML outputs from a single JSON source. Generated files are committed to the repository and deployed to GitHub Pages via GitHub Actions.

## Architecture

This project uses an object-oriented design with an abstract base class and format-specific generators:

- **`src/abstract_cv_generator.py`** - Defines the generation interface
- **`src/pdf_cv_generator.py`** - Generates PDF via LaTeX
- **`src/html_cv_generator.py`** - Generates static HTML with dark mode
- **`data/cv-data.json`** - Single source of truth for all CV content
- **`css/static-style.css`** - Styling for the HTML version
- **`generate_pdf.py`** - Entry point for PDF generation
- **`generate_html.py`** - Entry point for HTML generation

## Workflow

```
Edit data/cv-data.json
         ↓
Run generate_pdf.py (creates CV - Tom Bower.pdf)
Run generate_html.py (creates index.html)
         ↓
git commit & git push
         ↓
GitHub Actions automatically deploys to GitHub Pages
```

## Quick Start

### 1. Local Setup

**Requirements:**
- Python 3.8+
- LaTeX (for PDF generation)

**Install LaTeX:**

**macOS:**
```bash
brew install --cask mactex
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

**Windows:**
Download and install [MiKTeX](https://miktex.org/)

### 2. Generate Locally

```bash
# Edit your CV data
nano data/cv-data.json

# Generate both formats
python generate_pdf.py      # Creates output/CV - Tom Bower.pdf
python generate_html.py     # Creates index.html

# Generate anonymized PDF (no personal name)
python generate_pdf.py --anon  # Creates output/CV - Anonymous.pdf

# Preview in browser
open index.html             # macOS
xdg-open index.html         # Linux
start index.html            # Windows
```

### 3. Deploy to GitHub

```bash
# Stage the generated files
git add index.html "output/CV - Tom Bower.pdf"

# Commit your changes
git commit -m "Update CV - [description of changes]"

# Push to GitHub
git push origin main

# GitHub Actions will automatically:
# 1. Generate PDF and HTML
# 2. Commit updated files
# 3. Deploy to GitHub Pages at https://thomasb.dev
```

## File Structure

```
.
├── src/
│   ├── abstract_cv_generator.py      # Base class
│   ├── pdf_cv_generator.py           # PDF generator
│   └── html_cv_generator.py          # HTML generator
├── data/
│   └── cv-data.json                  # CV content (edit this)
├── css/
│   └── static-style.css              # HTML styling
├── output/
│   ├── CV - Tom Bower.pdf            # Generated PDF (commit this)
│   ├── cv.tex                        # LaTeX source (temporary)
│   └── cv.log, cv.aux, etc.          # LaTeX artifacts
├── assets/
│   ├── images/
│   │   └── profile.png               # Profile photo
│   └── icons/                        # Favicons
├── generate_pdf.py                   # PDF entry point
├── generate_html.py                  # HTML entry point
├── index.html                        # Generated HTML (commit this)
├── .github/
│   └── workflows/
│       └── generate.yml              # GitHub Actions workflow
└── README.md                         # This file
```

## CV Data Format

Edit `data/cv-data.json` to customize your CV. Structure:

```json
{
  "personal": {
    "name": "Your Name",
    "title": "Your Title",
    "email": "your.email@example.com",
    "phone": "+44 1234 567890",
    "location": "City, Country",
    "summary": "Professional summary...",
    "social": [
      {
        "name": "LinkedIn",
        "url": "https://linkedin.com/in/...",
        "icon": "fab fa-linkedin"
      }
    ]
  },
  "skills": ["Skill 1", "Skill 2", ...],
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "City",
      "startDate": "Month Year",
      "endDate": "Month Year",
      "icon": "fas fa-laptop-code",
      "highlights": ["Achievement 1", "Achievement 2"]
    }
  ],
  "education": [
    {
      "degree": "Degree Name",
      "institution": "University Name",
      "years": "Start - End",
      "details": [
        { "subject": "Subject", "grade": "A" }
      ]
    }
  ],
  "publications": [
    {
      "authors": "Author1, Author2",
      "year": 2024,
      "title": "Paper Title",
      "venue": "Conference/Journal",
      "doi": "10.xxxx/xxxxx",
      "url": "https://..."
    }
  ],
  "awards": [
    {
      "title": "Award Name",
      "description": "Award description",
      "url": "https://..."
    }
  ],
  "hobbies": [
    {
      "name": "Hobby Name",
      "icon": "fas fa-icon-name"
    }
  ]
}
```

See the FontAwesome documentation for available icons: https://fontawesome.com/icons

## Customization

### PDF Styling
Edit LaTeX formatting in `src/pdf_cv_generator.py`:
- Colors: `\definecolor{primary}{RGB}{79,70,229}`
- Fonts: `\documentclass[11pt,a4paper]{article}`
- Spacing: `\vspace{0.2cm}` commands

### HTML Styling
Edit `css/static-style.css`:
- Colors: CSS variables in `:root`
- Dark mode: `body.dark-mode` rules
- Responsive: media queries at bottom

### Anonymous CVs
Generate an anonymized CV without your personal name:
```bash
python generate_pdf.py --anon
```
This creates `CV - Anonymous.pdf` with all content except the personal name in the header.

### Section Order
Change the order in `src/abstract_cv_generator.py`'s `generate()` method by reordering these calls:
```python
self.generate_header()
self.generate_summary()
self.generate_experience()
self.generate_education()
self.generate_skills()
self.generate_publications()
self.generate_awards()
self.generate_hobbies()
```

## GitHub Pages Setup

Your CV is automatically deployed to GitHub Pages. To customize:

1. **Custom domain** - Edit `.github/workflows/generate.yml`:
   ```yaml
   cname: your-domain.com
   ```

2. **Repository settings** - Ensure GitHub Pages is enabled:
   - Settings → Pages → Build and deployment
   - Source: Deploy from a branch
   - Branch: `gh-pages`

## Troubleshooting

**PDF won't generate:**
- Ensure pdflatex is installed: `pdflatex --version`
- Check for LaTeX errors in `output/cv.log`

**HTML not rendering:**
- Verify `css/static-style.css` exists
- Check browser console for JavaScript errors
- Clear browser cache

**Dark mode not working:**
- Ensure JavaScript is enabled
- Check browser localStorage isn't disabled
- Try a different browser

**Files not updating on GitHub:**
- Verify files are in `.gitignore` (they shouldn't be)
- Check GitHub Actions logs for errors
- Manually push changes: `git push origin main`

## Deployment Checklist

- [ ] Edit `data/cv-data.json`
- [ ] Run `python generate_pdf.py`
- [ ] Run `python generate_html.py`
- [ ] Preview `index.html` locally
- [ ] Commit: `git add index.html "output/CV - Tom Bower.pdf"`
- [ ] Push: `git push origin main`
- [ ] Verify at https://thomasb.dev (or your custom domain)

## License

Your CV content is yours. The generation scripts and styling are provided as-is for personal use.
