#!/usr/bin/env python3
"""
Generate CV as PDF via LaTeX
"""
import sys
import argparse
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from pdf_cv_generator import PdfCvGenerator

def main():
    parser = argparse.ArgumentParser(
        description='Generate CV as PDF from JSON data'
    )
    parser.add_argument(
        '--anon',
        action='store_true',
        help='Generate anonymized CV without personal name'
    )
    args = parser.parse_args()
    
    try:
        generator = PdfCvGenerator(anonymous=args.anon)
        generator.generate()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nMake sure you have pdflatex installed:")
        print("  Windows: Install MiKTeX (https://miktex.org/)")
        print("  macOS: Install MacTeX (https://www.tug.org/mactex/)")
        print("  Linux: sudo apt-get install texlive-latex-base texlive-fonts-recommended")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
