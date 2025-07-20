# md2x - Universal Markdown Converter

[![GitHub](https://img.shields.io/github/license/hongsw/md2tex)](https://github.com/hongsw/md2tex)
[![Python](https://img.shields.io/pypi/pyversions/md2x)](https://pypi.org/project/md2x/)
[![PyPI](https://img.shields.io/pypi/v/md2x)](https://pypi.org/project/md2x/)

Convert Markdown to LaTeX, PDF, HTML, DOCX, and more - optimized for academic papers and ArXiv submissions.

## Features

- 🚀 **Multiple Output Formats**: LaTeX, PDF, HTML, DOCX, EPUB, RST, ArXiv package
- 📚 **Academic Optimized**: Special support for citations, math, tables, and bibliographies
- 📦 **ArXiv Ready**: Generate complete ArXiv submission packages with one command
- 🔄 **Live Preview**: Watch mode for automatic conversion on file changes
- 🎨 **Customizable**: Use custom templates and styling
- 🌍 **Unicode Support**: Full international character support
- 📊 **Table Support**: Convert Markdown tables to proper LaTeX tables
- 🔢 **Math Support**: Inline and display math with LaTeX syntax
- 📖 **Bibliography**: BibTeX integration for citations

## Installation

### Basic Installation
```bash
pip install md2x
```

### Full Installation (with all converters)
```bash
pip install md2x[full]
```

### From Source
```bash
git clone https://github.com/hongsw/md2tex.git
cd md2tex
pip install -e .
```

## Quick Start

### Basic Usage

Convert Markdown to LaTeX:
```bash
md2x paper.md -f tex
```

Convert to PDF:
```bash
md2x paper.md -f pdf
```

Convert to HTML:
```bash
md2x paper.md -f html
```

### ArXiv Submission

Create a complete ArXiv submission package:
```bash
md2x paper.md -f arxiv --bibliography refs.bib --figures figures/
```

This creates:
- `paper_arxiv/` directory with all files
- `paper_arxiv.tar.gz` ready for upload to ArXiv

### Watch Mode

Automatically convert on file changes:
```bash
md2x paper.md -f pdf --watch
```

## Command Line Options

```
Usage: md2x [OPTIONS] INPUT_FILE

Options:
  -f, --format [tex|pdf|html|docx|epub|rst|arxiv]
                                  Output format (default: tex)
  -o, --output PATH               Output file/directory path
  -t, --template PATH             Custom LaTeX template file
  --arxiv                         Use ArXiv-optimized settings
  --french-quotes                 Use French-style quotes
  --unnumbered                    Use unnumbered sections
  --document-class [article|book|report]
                                  LaTeX document class
  --bibliography PATH             BibTeX bibliography file
  --figures PATH                  Directory containing figures
  --metadata PATH                 JSON file with document metadata
  --watch                         Watch for changes and auto-convert
  -v, --verbose                   Verbose output
  --help                          Show this message and exit
```

## Examples

### Academic Paper with Bibliography

```bash
md2x manuscript.md -f pdf \
  --bibliography references.bib \
  --figures images/ \
  --document-class article
```

### Book Conversion

```bash
md2x book.md -f pdf \
  --document-class book \
  --unnumbered \
  --template book-template.tex
```

### HTML with Math Support

```bash
md2x notes.md -f html --watch
```

### Complete ArXiv Package

```bash
md2x paper.md -f arxiv \
  --bibliography refs.bib \
  --figures figures/ \
  --metadata metadata.json
```

## Markdown Extensions

### Tables

```markdown
| Method | Accuracy | Speed |
|--------|----------|-------|
| Our    | 95.2%    | 10ms  |
| Baseline| 87.1%   | 25ms  |
```

### Math

Inline math: `$E = mc^2$`

Display math:
```markdown
$$
\frac{\partial L}{\partial \theta} = \sum_{i=1}^{n} x_i
$$
```

### Citations

```markdown
This was shown in [Ceccarelli2025] and later confirmed [1,2,3].
```

### Metadata (Front Matter)

```markdown
# Specification-Driven Development

**Authors:** Seungwoo Hong  
**Date:** December 2024

## Abstract

Your abstract here...
```

## Template Customization

Create custom LaTeX templates by including these tokens:
- `@@BODYTOKEN@@` - Where the converted content goes
- `@@TITLEBLOCK@@` - Title and author information
- `@@ABSTRACT@@` - Abstract section
- `@@BIBLIOGRAPHY@@` - Bibliography section
- `@@DOCUMENTCLASSTOKEN@@` - Document class

Example template:
```latex
\documentclass[11pt]{@@DOCUMENTCLASSTOKEN@@}
\usepackage{custom-style}

\begin{document}
@@TITLEBLOCK@@
@@ABSTRACT@@
@@BODYTOKEN@@
@@BIBLIOGRAPHY@@
\end{document}
```

## Requirements

### System Requirements

- Python 3.7+
- For PDF: LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- For advanced conversions: Pandoc

### Python Dependencies

- click>=8.0.0
- markdown>=3.0.0
- watchdog>=2.0.0
- pypandoc>=1.6 (optional, for advanced conversions)

## Development

### Setup Development Environment

```bash
git clone https://github.com/hongsw/md2tex.git
cd md2tex
pip install -e .[dev]
```

### Run Tests

```bash
pytest
```

### Code Style

```bash
black .
flake8 .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original md2tex project for the foundation
- Pandoc for advanced document conversion
- ArXiv for documentation on submission requirements

## Roadmap

- [ ] Add support for reveal.js presentations
- [ ] Implement citation style customization
- [ ] Add support for Jupyter notebooks
- [ ] Create GUI version
- [ ] Add cloud conversion API

## Support

- 📧 Email: seungwoo.hong@baryon.ai
- 🐛 Issues: [GitHub Issues](https://github.com/hongsw/md2tex/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/hongsw/md2tex/discussions)