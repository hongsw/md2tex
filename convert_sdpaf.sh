#!/bin/bash
# Script to convert SDPAF paper using md2x

echo "Converting SDPAF Academic Paper with md2x..."
echo "============================================"

# Set the input file
INPUT="../SDPAF_Academic_Paper.md"
OUTPUT_DIR="sdpaf_output"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Install md2x if not already installed
echo "Installing md2x..."
pip install -e . > /dev/null 2>&1

# Convert to different formats
echo ""
echo "1. Converting to LaTeX..."
python md2x.py "$INPUT" -f tex -o "$OUTPUT_DIR/SDPAF_Paper.tex" --arxiv

echo ""
echo "2. Converting to PDF..."
python md2x.py "$INPUT" -f pdf -o "$OUTPUT_DIR/SDPAF_Paper.pdf" --arxiv

echo ""
echo "3. Converting to HTML..."
python md2x.py "$INPUT" -f html -o "$OUTPUT_DIR/SDPAF_Paper.html"

echo ""
echo "4. Creating ArXiv package..."
python md2x.py "$INPUT" -f arxiv -o "$OUTPUT_DIR/SDPAF_arxiv" \
  --bibliography ../references.bib

echo ""
echo "Conversion complete! Files created in $OUTPUT_DIR/"
echo ""
echo "Files generated:"
ls -la "$OUTPUT_DIR/"

echo ""
echo "To submit to ArXiv:"
echo "1. Review the files in $OUTPUT_DIR/SDPAF_arxiv/"
echo "2. Upload $OUTPUT_DIR/SDPAF_arxiv.tar.gz to ArXiv"
echo "3. Select categories: cs.SE (primary), cs.AI, cs.HC (secondary)"