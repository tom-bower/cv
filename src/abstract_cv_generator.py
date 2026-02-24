#!/usr/bin/env python3
"""
Abstract CV Generator with support for multiple output formats (PDF, HTML)
"""
import json
from abc import ABC, abstractmethod
from pathlib import Path


class AbstractCvGenerator(ABC):
    """
    Abstract base class for CV generation in different formats.
    
    This class defines the interface for generating CVs in different output formats.
    Subclasses implement format-specific methods for escaping text, generating sections,
    and writing output.
    """
    
    def __init__(self, anonymous=False):
        """
        Initialize the CV generator.
        
        Parameters
        ----------
        anonymous : bool, optional
            If True, generates an anonymized CV without personal name. Default is False.
        
        Returns
        -------
        None
        """
        self.cv_data = None
        self.content = ""
        self.anonymous = anonymous
    
    def load_cv_data(self):
        """
        Load CV data from JSON file.
        
        Reads the CV data from 'data/cv-data.json' and stores it in self.cv_data.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        
        Raises
        ------
        FileNotFoundError
            If the JSON file does not exist.
        json.JSONDecodeError
            If the JSON file is malformed.
        """
        # Construct path relative to project root
        json_path = Path(__file__).parent.parent / 'data' / 'cv-data.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            self.cv_data = json.load(f)
    
    @abstractmethod
    def escape_text(self, text):
        """
        Escape text for the target format.
        
        Subclasses must implement this to handle format-specific escaping
        (e.g., LaTeX backslashes, HTML entities).
        
        Parameters
        ----------
        text : str
            The text to escape.
        
        Returns
        -------
        str
            The escaped text.
        """
        pass
    
    @abstractmethod
    def generate_header(self):
        """
        Generate header section.
        
        Generates the document header containing personal information.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def generate_summary(self):
        """
        Generate professional summary section.
        
        Generates the professional summary/introduction section.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def generate_experience(self):
        """
        Generate experience section.
        
        Generates the work experience/employment section.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def generate_education(self):
        """
        Generate education section.
        
        Generates the education/qualifications section.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def generate_skills(self):
        """
        Generate skills section.
        
        Generates the technical and soft skills section.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def generate_publications(self):
        """
        Generate publications section.
        
        Generates the academic/professional publications section.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def generate_awards(self):
        """
        Generate awards section.
        
        Generates the awards and recognitions section.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def generate_hobbies(self):
        """
        Generate hobbies/interests section.
        
        Generates the hobbies and personal interests section.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    @abstractmethod
    def write_output(self):
        """
        Write the generated content to output.
        
        Saves or compiles the generated content to the appropriate output format.
        Implementation is format-specific.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass
    
    def generate(self):
        """
        Generate CV by orchestrating all sections in order.
        
        This is the main entry point that loads data and generates all sections
        in the correct order. The section order can be changed by reordering
        the method calls.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        print("Loading CV data...")
        self.load_cv_data()
        
        print(f"Generating {self.__class__.__name__} content...")
        self.generate_header()
        self.generate_summary()
        self.generate_experience()
        self.generate_education()
        self.generate_skills()
        self.generate_publications()
        self.generate_awards()
        self.generate_hobbies()
        
        print("Writing output...")
        self.write_output()
    
    def _get_section_title(self, title):
        """
        Helper method to get escaped section title.
        
        Parameters
        ----------
        title : str
            The section title to escape.
        
        Returns
        -------
        str
            The escaped section title.
        """
        return self.escape_text(title)
