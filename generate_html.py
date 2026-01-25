#!/usr/bin/env python3
"""
Generate static HTML CV from JSON data
"""
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from html_cv_generator import HtmlCvGenerator

def main():
    try:
        generator = HtmlCvGenerator()
        generator.generate()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
