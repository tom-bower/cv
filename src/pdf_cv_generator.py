#!/usr/bin/env python3
"""
PDF CV Generator - generates CV as PDF via LaTeX.
"""
import subprocess
import sys
from pathlib import Path
from abstract_cv_generator import AbstractCvGenerator


class PdfCvGenerator(AbstractCvGenerator):
    """
    Generate CV as PDF via LaTeX.
    
    This class generates a professional CV in PDF format by creating a LaTeX
    document and compiling it to PDF using pdflatex. Each section is generated
    with appropriate LaTeX formatting.
    """
    
    def __init__(self, anonymous=False):
        """
        Initialize the PDF CV generator.
        
        Parameters
        ----------
        anonymous : bool, optional
            If True, generates an anonymized CV without personal name. Default is False.
        """
        super().__init__(anonymous)
    
    def escape_text(self, text):
        """
        Escape special LaTeX characters.
        
        Escapes characters that have special meaning in LaTeX to ensure they
        are rendered correctly in the output. The backslash is escaped first
        to avoid double-escaping.
        
        Parameters
        ----------
        text : str or other
            The text to escape. If not a string, will be converted to string.
        
        Returns
        -------
        str
            The escaped text safe for LaTeX.
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Must escape backslash first to avoid double-escaping
        replacements = [
            ('\\', r'\textbackslash{}'),
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('_', r'\_'),
            ('{', r'\{'),
            ('}', r'\}'),
            ('~', r'\textasciitilde{}'),
            ('^', r'\textasciicircum{}'),
        ]
        
        result = text
        for char, replacement in replacements:
            result = result.replace(char, replacement)
        return result
    
    def generate_header(self):
        """
        Generate LaTeX document header and personal information.
        
        Creates the LaTeX document preamble, page setup, and header with
        name, email, phone, and location.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        personal = self.cv_data['personal']
        
        self.content = (
            r"\documentclass[11pt,a4paper]{article}" + "\n"
            r"\usepackage[margin=0.5in]{geometry}" + "\n"
            r"\usepackage{hyperref}" + "\n"
            r"\usepackage{xcolor}" + "\n"
            r"\usepackage{array}" + "\n"
            r"\usepackage{enumitem}" + "\n"
            "\n"
            r"% Define colors" + "\n"
            r"\definecolor{primary}{RGB}{79,70,229}" + "\n"
            r"\definecolor{darkgray}{RGB}{75,75,75}" + "\n"
            "\n"
            r"% Header styling" + "\n"
            r"\pagestyle{empty}" + "\n"
            "\n"
            r"\begin{document}" + "\n"
            "\n"
            r"% Header" + "\n"
            r"\begin{center}" + "\n"
        )
        
        # Only include name and contact info if not anonymous
        if not self.anonymous:
            self.content += (
                r"{\Large \textbf{" + self.escape_text(personal['name']) + r"}}\\" + "\n"
                r"\vspace{0.1cm}" + "\n"
                r"{\small " + self.escape_text(personal['email']) + r" $|$ " +
                self.escape_text(personal['phone']) + r" $|$ " +
                self.escape_text(personal['location']) + r"}\\" + "\n"
                r"\vspace{0.15cm}" + "\n"
                r"\hrule" + "\n"
            )
        
        self.content += (
            r"\end{center}" + "\n"
            "\n"
        )
    
    def generate_summary(self):
        """
        Generate professional summary section.
        
        Adds the professional summary text below the header.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        personal = self.cv_data['personal']
        
        self.content += (
            r"% Professional Summary" + "\n"
            r"\vspace{0.2cm}" + "\n"
            r"{\small " + self.escape_text(personal['summary']) + r"}" + "\n"
            "\n"
        )
    
    def generate_experience(self):
        """
        Generate work experience section.
        
        Creates a formatted section with job titles, companies, dates, and
        highlights for each position.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.content += (
            "\n"
            r"\section*{EXPERIENCE}" + "\n"
            r"\vspace{-0.3cm}" + "\n"
            r"\hrule" + "\n"
            r"\vspace{0.2cm}" + "\n"
            "\n"
        )
        
        for job in self.cv_data['experience']:
            self.content += (
                r"\noindent" + "\n"
                r"\textbf{" + self.escape_text(job['title']) + r"} \hfill {\small " +
                self.escape_text(job['startDate']) + r" -- " +
                self.escape_text(job['endDate']) + r"}\\" + "\n"
                r"{\small \textit{" + self.escape_text(job['company']) + r", " +
                self.escape_text(job['location']) + r"}}" + "\n"
                r"\vspace{0.15cm}" + "\n"
            )
            
            for highlight in job['highlights']:
                self.content += (
                    r"\begin{itemize}[leftmargin=0.25in,topsep=-0.1cm,partopsep=0pt]" + "\n"
                    r"\item {\small " + self.escape_text(highlight) + r"}" + "\n"
                    r"\end{itemize}" + "\n"
                )
            
            self.content += r"\vspace{0.25cm}" + "\n"
    
    def generate_education(self):
        """
        Generate education section.
        
        Creates a formatted section with degrees, institutions, years, and
        grades for each qualification. A-level grades are displayed in a
        borderless table format.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.content += (
            "\n"
            r"\section*{EDUCATION}" + "\n"
            r"\vspace{-0.3cm}" + "\n"
            r"\hrule" + "\n"
            r"\vspace{0.2cm}" + "\n"
            "\n"
        )
        
        for edu in self.cv_data['education']:
            self.content += (
                r"\noindent" + "\n"
                r"\textbf{" + self.escape_text(edu['degree']) + r"} \hfill {\small " +
                self.escape_text(edu['years']) + r"}\\" + "\n"
                r"{\small " + self.escape_text(edu['institution']) + r"}" + "\n"
                r"\vspace{0.15cm}" + "\n"
            )
            
            if 'details' in edu and edu['details']:
                num_cols = len(edu['details'])
                self.content += (
                    r"\\" + "\n"
                    r"\vspace{0.05cm}" + "\n"
                    r"\begin{tabular}{*{" + str(num_cols) + r"}{c}}" + "\n"
                )
                
                # Top row: subjects
                subjects = [
                    self.escape_text(detail['subject'])
                    for detail in edu['details']
                ]
                self.content += " & ".join(subjects) + r" \\" + "\n"
                
                # Bottom row: grades
                grades = [
                    self.escape_text(detail['grade'])
                    for detail in edu['details']
                ]
                self.content += " & ".join(grades) + "\n"
                self.content += r"\end{tabular}" + "\n"
            
            self.content += "\n" + r"\vspace{0.1cm}" + "\n"
    
    def generate_skills(self):
        """
        Generate skills section.
        
        Creates a formatted section with a comma-separated list of technical
        and soft skills.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.content += (
            "\n"
            r"\section*{SKILLS}" + "\n"
            r"\vspace{-0.3cm}" + "\n"
            r"\hrule" + "\n"
            r"\vspace{0.2cm}" + "\n"
            "\n"
            r"\noindent" + "\n"
        )
        
        skills_text = ", ".join([
            self.escape_text(skill) for skill in self.cv_data['skills']
        ])
        
        self.content += r"{\small " + skills_text + r"}" + "\n" + "\n"
    
    def generate_publications(self):
        """
        Generate publications section.
        
        Creates a formatted section with academic and professional publications.
        Skips this section if no publications exist.
        
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
            "\n"
            r"\section*{PUBLICATIONS}" + "\n"
            r"\vspace{-0.3cm}" + "\n"
            r"\hrule" + "\n"
            r"\vspace{0.2cm}" + "\n"
            "\n"
        )
        
        for pub in self.cv_data['publications']:
            self.content += (
                r"\noindent" + "\n"
                r"{\small \textbf{" + self.escape_text(pub['authors']) +
                r"} (" + str(pub['year']) + r"). " +
                self.escape_text(pub['title']) + r". \textit{" +
                self.escape_text(pub['venue']) + r"}\vspace{0.05cm}\\" + "\n"
            )
        
        self.content += "\n"
    
    def generate_awards(self):
        """
        Generate awards section.
        
        Creates a formatted section with awards and recognitions.
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
            "\n"
            r"\section*{AWARDS AND ACCREDITATIONS}" + "\n"
            r"\vspace{-0.3cm}" + "\n"
            r"\hrule" + "\n"
            r"\vspace{0.2cm}" + "\n"
            "\n"
        )
        
        for award in self.cv_data['awards']:
            self.content += (
                r"\noindent" + "\n"
                r"{\small \textbf{" + self.escape_text(award['title']) +
                r"} -- " + self.escape_text(award['description']) + r"}\\" + "\n"
            )
    
    def generate_hobbies(self):
        """
        Generate hobbies/interests section.
        
        Creates a formatted section with personal interests displayed as a
        bulleted list. Skips this section if no hobbies exist.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        if not self.cv_data['hobbies']:
            return
        
        self.content += (
            "\n"
            r"\section*{INTERESTS}" + "\n"
            r"\vspace{-0.3cm}" + "\n"
            r"\hrule" + "\n"
            r"\vspace{0.2cm}" + "\n"
            "\n"
            r"\begin{itemize}[leftmargin=0.25in,topsep=0pt,partopsep=0pt]" + "\n"
        )
        
        for hobby in self.cv_data['hobbies']:
            self.content += (
                r"\item {\small " + self.escape_text(hobby['name']) + r"}" + "\n"
            )
        
        self.content += r"\end{itemize}" + "\n" + "\n"
    
    def write_output(self):
        """
        Write LaTeX to file and compile to PDF.
        
        Closes the LaTeX document, writes it to cv.tex, and compiles it to PDF
        using pdflatex. The output PDF is named "CV - Tom Bower.pdf".
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        
        Raises
        ------
        FileNotFoundError
            If pdflatex is not installed on the system.
        SystemExit
            If LaTeX compilation fails.
        """
        # Close LaTeX document
        self.content += "\n" + r"\end{document}" + "\n"
        
        # Write LaTeX file
        output_path = Path('output') / 'cv.tex'
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.content)
        print(f"LaTeX file written to {output_path}")
        
        # Compile to PDF
        print("Compiling to PDF...")
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory=output',
             str(output_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Rename PDF with name or anonymize
            source_pdf = Path('output') / 'cv.pdf'
            if self.anonymous:
                target_pdf = Path('output') / 'CV - Anonymous.pdf'
            else:
                personal_name = self.cv_data['personal']['name']
                target_pdf = Path('output') / f'CV - {personal_name}.pdf'
            if source_pdf.exists():
                source_pdf.replace(target_pdf)
            print(f"✓ PDF generated successfully: {target_pdf}")
        else:
            print("LaTeX compilation failed:")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)
