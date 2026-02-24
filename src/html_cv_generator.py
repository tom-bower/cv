#!/usr/bin/env python3
"""
HTML CV Generator - generates CV as static HTML.
"""
from abstract_cv_generator import AbstractCvGenerator


class HtmlCvGenerator(AbstractCvGenerator):
    """
    Generate CV as static HTML.
    
    This class generates a CV as a complete static HTML document with embedded
    CSS and JavaScript for dark mode support. The HTML includes responsive
    design with a sidebar for contact and skills.
    """
    
    def __init__(self, anonymous=False):
        """
        Initialize the HTML CV generator.
        
        Parameters
        ----------
        anonymous : bool, optional
            If True, generates an anonymized CV without personal name. Default is False.
        """
        super().__init__(anonymous)
    
    def escape_text(self, text):
        """
        Escape HTML special characters.
        
        Escapes characters that have special meaning in HTML to ensure they
        are rendered correctly and safely.
        
        Parameters
        ----------
        text : str or other
            The text to escape. If not a string, will be converted to string.
        
        Returns
        -------
        str
            The escaped text safe for HTML.
        """
        if not isinstance(text, str):
            text = str(text)
        
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
        }
        result = text
        for char, replacement in replacements.items():
            result = result.replace(char, replacement)
        return result
    
    def generate_header(self):
        """
        Generate HTML document header with header bar and sidebar.
        
        Creates the HTML structure including the document head with CSS/meta,
        the header bar with name and controls, and begins the sidebar with
        profile information.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        personal = self.cv_data['personal']
        
        # Social links HTML
        social_links = ''.join([
            f'<a href="{link["url"]}" target="_blank" rel="noopener" '
            f'class="social-link" title="{self.escape_text(link["name"])}">'
            f'<i class="{link["icon"]}"></i></a>'
            for link in personal['social']
        ])
        
        # Skills HTML
        skills_html = ''.join([
            f'<li>{self.escape_text(skill)}</li>'
            for skill in self.cv_data['skills']
        ])
        
        self.content = (
            "<!DOCTYPE html>" + "\n"
            '<html lang="en">' + "\n"
            "<head>" + "\n"
            '  <meta charset="UTF-8">' + "\n"
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1.0">' + "\n"
            f"  <title>{self.escape_text(personal['name'])} - CV</title>" + "\n"
            '<link rel="stylesheet" '
            'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/'
            'css/all.min.css">' + "\n"
            '  <link rel="stylesheet" href="css/static-style.css">' + "\n"
            "</head>" + "\n"
            "<body>" + "\n"
            '  <header class="header">' + "\n"
            f"    <h1>{self.escape_text(personal['name'])}</h1>" + "\n"
            '    <div class="header-controls">' + "\n"
            '      <a href="output/CV%20-%20Tom%20Bower.pdf" '
            'class="pdf-download" download="CV - Tom Bower.pdf">'
            '<i class="fas fa-file-pdf"></i> Download PDF</a>' + "\n"
            '      <button id="darkModeBtn" class="dark-mode-button" '
            'title="Toggle dark mode"><i class="fas fa-moon"></i></button>' + "\n"
            "    </div>" + "\n"
            "  </header>" + "\n"
            "\n"
            '  <main class="cv-container">' + "\n"
            '    <aside class="sidebar">' + "\n"
            '      <div class="profile-image-section">' + "\n"
            '        <img src="assets/images/profile.png" '
            'alt="Profile Photo" class="profile-image">' + "\n"
            "      </div>" + "\n"
            "      " + "\n"
            '      <section class="profile-section">' + "\n"
            "        <h2>Profile</h2>" + "\n"
            f'        <p class="summary">'
            f'{self.escape_text(personal["summary"])}</p>' + "\n"
            "      </section>" + "\n"
            "\n"
            '      <section class="contact-section">' + "\n"
            "        <h2>Contact</h2>" + "\n"
            '        <ul class="contact-list">' + "\n"
            f'          <li><i class="fas fa-envelope"></i> '
            f'<a href="mailto:{personal["email"]}">'
            f'{self.escape_text(personal["email"])}</a></li>' + "\n"
            f'          <li><i class="fas fa-phone"></i> '
            f'<a href="tel:{personal["phone"]}">'
            f'{self.escape_text(personal["phone"])}</a></li>' + "\n"
            f'          <li><i class="fas fa-map-marker-alt"></i> '
            f'{self.escape_text(personal["location"])}</li>' + "\n"
            "        </ul>" + "\n"
            '        <div class="social-links">' + "\n"
            f"          {social_links}" + "\n"
            "        </div>" + "\n"
            "      </section>" + "\n"
            "\n"
            '      <section class="skills-section">' + "\n"
            "        <h2>Skills</h2>" + "\n"
            '        <ul class="skills-list">' + "\n"
            f"          {skills_html}" + "\n"
            "        </ul>" + "\n"
            "      </section>" + "\n"
            "    </aside>" + "\n"
            "\n"
            '    <article class="main-content">' + "\n"
        )
    
    def generate_summary(self):
        """
        Generate summary - already in header for HTML.
        
        For HTML, the summary is included in the sidebar during header generation,
        so this method does nothing.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    def generate_experience(self):
        """
        Generate work experience section.
        
        Creates HTML job cards with title, company, dates, and highlights for
        each position.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.content += (
            '      <section class="experience-section">' + "\n"
            "        <h2>Experience</h2>" + "\n"
            '        <div class="experience-list">' + "\n"
            "          " + "\n"
        )
        
        for job in self.cv_data['experience']:
            highlights = ''.join([
                f'<li>{self.escape_text(h)}</li>'
                for h in job['highlights']
            ])
            
            self.content += (
                '        <div class="job-card">' + "\n"
                '          <div class="job-header">' + "\n"
                f'            <div class="job-title"><i class="{job["icon"]}">'
                f'</i> {self.escape_text(job["title"])}</div>' + "\n"
                "          </div>" + "\n"
                '          <div class="job-meta">' + "\n"
                f'            <p class="job-company">'
                f'{self.escape_text(job["company"])}, '
                f'{self.escape_text(job["location"])}</p>' + "\n"
                f'            <span class="job-dates">'
                f'{self.escape_text(job["startDate"])} - '
                f'{self.escape_text(job["endDate"])}</span>' + "\n"
                "          </div>" + "\n"
                f'          <ul class="job-highlights">' + "\n"
                f"            {highlights}" + "\n"
                "          </ul>" + "\n"
                "        </div>" + "\n"
                "        " + "\n"
            )
        
        self.content += (
            "        </div>" + "\n"
            "      </section>" + "\n"
            "\n"
        )
    
    def generate_education(self):
        """
        Generate education section.
        
        Creates HTML cards for each degree/qualification with institution,
        years, and optional grade details.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.content += (
            '      <section class="education-section">' + "\n"
            "        <h2>Education</h2>" + "\n"
            '        <div class="education-list">' + "\n"
            "          " + "\n"
        )
        
        for edu in self.cv_data['education']:
            details_html = ""
            if 'details' in edu and edu['details']:
                details_html = ''.join([
                    f"<li><strong>{self.escape_text(d['subject'])}</strong>: "
                    f"{self.escape_text(d['grade'])}</li>"
                    for d in edu['details']
                ])
                details_html = f"<ul class='education-details'>{details_html}</ul>"
            
            self.content += (
                '        <div class="education-item">' + "\n"
                f'          <div class="edu-degree">'
                f'{self.escape_text(edu["degree"])}</div>' + "\n"
                f'          <div class="edu-institution">'
                f'{self.escape_text(edu["institution"])}</div>' + "\n"
                f'          <div class="edu-years">'
                f'{self.escape_text(edu["years"])}</div>' + "\n"
                f"          {details_html}" + "\n"
                "        </div>" + "\n"
                "        " + "\n"
            )
        
        self.content += (
            "        </div>" + "\n"
            "      </section>" + "\n"
            "\n"
        )
    
    def generate_skills(self):
        """
        Generate skills - already in sidebar for HTML.
        
        For HTML, skills are included in the sidebar during header generation,
        so this method does nothing.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    def generate_publications(self):
        """
        Generate publications section.
        
        Creates an HTML section with formatted publication references including
        authors, year, title, and venue. Skips this section if no publications.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        if not self.cv_data['publications']:
            return
        
        self.content += (
            '      <section class="publications-section">' + "\n"
            "        <h2>Publications</h2>" + "\n"
            '        <div class="publications-list">' + "\n"
        )
        
        for pub in self.cv_data['publications']:
            doi_link = ""
            if 'doi' in pub:
                doi_link = (
                    f"DOI: <a href='https://doi.org/{pub['doi']}' "
                    f"class='pub-link' target='_blank'>"
                    f"{self.escape_text(pub['doi'])}</a>"
                )
            
            self.content += (
                f"          <p><strong>"
                f"{self.escape_text(pub['authors'])}</strong> ({pub['year']}). "
                f"{self.escape_text(pub['title'])}. <em>"
                f"{self.escape_text(pub['venue'])}</em>. {doi_link}</p>" + "\n"
            )
        
        self.content += (
            "        </div>" + "\n"
            "      </section>" + "\n"
            "\n"
        )
    
    def generate_awards(self):
        """
        Generate awards section.
        
        Creates an HTML section with award titles and descriptions.
        Skips this section if no awards exist.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        if not self.cv_data['awards']:
            return
        
        self.content += (
            '      <section class="awards-section">' + "\n"
            "        <h2>Awards and Accreditations</h2>" + "\n"
            '        <div class="awards-list">' + "\n"
        )
        
        for award in self.cv_data['awards']:
            self.content += (
                f"          <p><strong>"
                f"{self.escape_text(award['title'])}</strong> - "
                f"{self.escape_text(award['description'])}</p>" + "\n"
            )
        
        self.content += (
            "        </div>" + "\n"
            "      </section>" + "\n"
            "\n"
        )
    
    def generate_hobbies(self):
        """
        Generate hobbies/interests section.
        
        Creates an HTML section with hobbies displayed as a grid of icon and
        name pairs. Skips this section if no hobbies exist.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        if not self.cv_data['hobbies']:
            return
        
        hobbies_html = ''.join([
            f'<li><i class="{hobby["icon"]}"></i>'
            f'<span>{self.escape_text(hobby["name"])}</span></li>'
            for hobby in self.cv_data['hobbies']
        ])
        
        self.content += (
            '      <section class="hobbies-section">' + "\n"
            "        <h2>Interests</h2>" + "\n"
            '        <ul class="hobbies-list">' + "\n"
            f"          {hobbies_html}" + "\n"
            "        </ul>" + "\n"
            "      </section>" + "\n"
        )
    
    def write_output(self):
        """
        Write HTML to file.
        
        Completes and closes the HTML document, then writes the entire
        content to index.html.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.content += (
            "    </article>" + "\n"
            "  </main>" + "\n"
            "\n"
            '  <footer class="footer">' + "\n"
            "    <p>Generated on 2026-01-24 • "
            '<a href="https://github.com/tom-bower/cv">View on GitHub</a></p>' + "\n"
            "  </footer>" + "\n"
            "\n"
            "  <script>" + "\n"
            "    // Dark mode toggle" + "\n"
            "    const darkModeBtn = document.getElementById('darkModeBtn');" + "\n"
            "    const darkModeIcon = darkModeBtn.querySelector('i');" + "\n"
            "    " + "\n"
            "    // Check for saved dark mode preference or default to dark" + "\n"
            "    const isDarkMode = localStorage.getItem('darkMode') === null" + "\n"
            "      ? true" + "\n"
            "      : localStorage.getItem('darkMode') === \"true\";" + "\n"
            "    " + "\n"
            "    if (isDarkMode) {" + "\n"
            "      document.body.classList.add('dark-mode');" + "\n"
            "      darkModeIcon.classList.remove('fa-moon');" + "\n"
            "      darkModeIcon.classList.add('fa-sun');" + "\n"
            "    }" + "\n"
            "    " + "\n"
            "    darkModeBtn.addEventListener('click', () => {" + "\n"
            "      document.body.classList.toggle('dark-mode');" + "\n"
            "      const isDark = document.body.classList.contains('dark-mode');" + "\n"
            "      localStorage.setItem('darkMode', isDark);" + "\n"
            "      darkModeIcon.classList.toggle('fa-moon');" + "\n"
            "      darkModeIcon.classList.toggle('fa-sun');" + "\n"
            "    });" + "\n"
            "  </script>" + "\n"
            "</body>" + "\n"
            "</html>" + "\n"
        )
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(self.content)
        print("✓ HTML file generated successfully: index.html")
