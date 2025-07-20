# Makefile for md2x - Universal Markdown Converter

.PHONY: help install dev test clean build publish arxiv pdf html all

# Default target
help:
	@echo "md2x - Universal Markdown Converter"
	@echo ""
	@echo "Available targets:"
	@echo "  install     Install md2x"
	@echo "  dev         Install in development mode"
	@echo "  test        Run tests"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build distribution packages"
	@echo "  publish     Publish to PyPI"
	@echo ""
	@echo "Conversion targets (requires INPUT=filename.md):"
	@echo "  pdf         Convert to PDF"
	@echo "  html        Convert to HTML"
	@echo "  arxiv       Create ArXiv package"
	@echo "  all         Convert to all formats"
	@echo ""
	@echo "Example: make pdf INPUT=paper.md"

# Installation targets
install:
	pip install -e .

dev:
	pip install -e .[dev,full]

# Testing
test:
	pytest tests/ -v --cov=md2x

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	find . -type f -name ".DS_Store" -delete

# Building
build: clean
	python3 setup.py sdist bdist_wheel

# Publishing
publish: build
	python3 -m twine upload dist/*

# Conversion targets
pdf:
ifndef INPUT
	$(error INPUT is not set. Usage: make pdf INPUT=filename.md)
endif
	python3 md2x.py $(INPUT) -f pdf

html:
ifndef INPUT
	$(error INPUT is not set. Usage: make html INPUT=filename.md)
endif
	python3 md2x.py $(INPUT) -f html

arxiv:
ifndef INPUT
	$(error INPUT is not set. Usage: make arxiv INPUT=filename.md)
endif
	python3 md2x.py $(INPUT) -f arxiv

tex:
ifndef INPUT
	$(error INPUT is not set. Usage: make tex INPUT=filename.md)
endif
	python3 md2x.py $(INPUT) -f tex

all:
ifndef INPUT
	$(error INPUT is not set. Usage: make all INPUT=filename.md)
endif
	@echo "Converting $(INPUT) to all formats..."
	python3 md2x.py $(INPUT) -f tex -o $(basename $(INPUT)).tex
	python3 md2x.py $(INPUT) -f pdf -o $(basename $(INPUT)).pdf
	python3 md2x.py $(INPUT) -f html -o $(basename $(INPUT)).html
	python3 md2x.py $(INPUT) -f arxiv -o $(basename $(INPUT))_arxiv
	@echo "All conversions complete!"

# Development helpers
format:
	black .
	isort .

lint:
	flake8 .
	pylint md2x.py utils/

type-check:
	mypy md2x.py

# Documentation
docs:
	cd docs && make html

serve-docs:
	cd docs/_build/html && python -m http.server

# Example usage
example:
	@echo "Converting example paper..."
	python3 md2x.py examples/sample_paper.md -f pdf --watch

# Installation check
check:
	@echo "Checking md2x installation..."
	@which md2x || echo "md2x not found in PATH"
	@echo ""
	@echo "Python version:"
	@python3 --version
	@echo ""
	@echo "Checking dependencies..."
	@pip3 list | grep -E "(click|markdown|watchdog|pypandoc)" || echo "Some dependencies missing"
	@echo ""
	@echo "Checking LaTeX..."
	@which pdflatex || echo "pdflatex not found - PDF conversion will not work"
	@echo ""
	@echo "Checking pandoc..."
	@which pandoc || echo "pandoc not found - some conversions will be limited"