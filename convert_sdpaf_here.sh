#!/bin/bash
# Convenience script to convert SDPAF paper from md2tex directory

echo "Converting SDPAF Academic Paper..."
echo "================================"

# The paper is in the parent directory
PAPER="../SDPAF_Academic_Paper.md"

# Create output directory
mkdir -p output

# Run conversions
echo "1. Converting to LaTeX..."
python3 md2x.py "$PAPER" -f tex -o output/SDPAF_Paper.tex --arxiv

echo "2. Converting to HTML..."
python3 md2x.py "$PAPER" -f html -o output/SDPAF_Paper.html

echo "3. Converting to PDF..."
python3 md2x.py "$PAPER" -f pdf -o output/SDPAF_Paper.pdf || echo "Note: PDF requires LaTeX"

echo "4. Creating ArXiv package..."
python3 md2x.py "$PAPER" -f arxiv -o output/SDPAF_arxiv --bibliography ../references.bib

echo ""
echo "✅ Done! Check the output/ directory:"
ls -la output/