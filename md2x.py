#!/usr/bin/env python3
"""
md2x - Universal Markdown Converter
Convert Markdown to various formats: LaTeX, PDF, HTML, DOCX, etc.
Optimized for academic papers and ArXiv submissions
"""

import click
import os
import re
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, List
import json
import tempfile
import sys

from utils.converters import MDSimple, MDQuote, MDList, MDCode, MDCleaner, MDReference, MDHeader
from utils.arxiv_converters import ArxivEnhancedConverter
from utils.errors_warnings import InputException, Warnings


class UniversalConverter:
    """Main converter class that handles all format conversions"""
    
    def __init__(self):
        self.arxiv_converter = ArxivEnhancedConverter()
        self.supported_formats = {
            'tex': 'LaTeX document',
            'pdf': 'PDF document (requires LaTeX)',
            'html': 'HTML document',
            'docx': 'Word document',
            'epub': 'EPUB book',
            'rst': 'reStructuredText',
            'arxiv': 'ArXiv-ready LaTeX package'
        }
    
    def convert_to_tex(self, content: str, options: Dict) -> str:
        """Convert markdown to LaTeX"""
        # Use existing md2tex converters
        data = MDCode.block_code(content)
        data, codedict = MDCleaner.prepare_markdown(data)
        data = MDQuote.inline_quote(data, options.get('french_quote', False))
        data = MDQuote.block_quote(data)
        data = MDList.unordered_l(data)
        data = MDList.ordered_l(data)
        data = MDReference.footnote(data)
        data = MDHeader.convert(data, options.get('unnumbered', False), 
                               options.get('document_class', 'article'))
        data = MDSimple.convert(data)
        data = MDCleaner.clean_tex(data, codedict)
        
        # Apply ArXiv enhancements if needed
        if options.get('arxiv_mode', False):
            arxiv_result = self.arxiv_converter.convert_for_arxiv(data, options.get('metadata'))
            
            # Use ArXiv template
            template_path = options.get('template')
            if not template_path:
                # Get the directory of this script
                import os
                script_dir = os.path.dirname(os.path.abspath(__file__))
                template_path = os.path.join(script_dir, 'utils', 'arxiv_template.tex')
            
            with open(template_path, 'r') as f:
                template = f.read()
            
            # Replace tokens
            tex_content = template.replace('@@BODYTOKEN@@', arxiv_result['body'])
            tex_content = tex_content.replace('@@TITLEBLOCK@@', arxiv_result['title_block'])
            tex_content = tex_content.replace('@@ABSTRACT@@', arxiv_result['abstract'])
            tex_content = tex_content.replace('@@BIBLIOGRAPHY@@', arxiv_result['bibliography'])
            tex_content = tex_content.replace('@@DOCUMENTCLASSTOKEN@@', 
                                            options.get('document_class', 'article'))
            
            return tex_content
        
        return data
    
    def convert_to_pdf(self, content: str, options: Dict, output_path: str) -> bool:
        """Convert markdown to PDF via LaTeX"""
        # First convert to TeX
        tex_content = self.convert_to_tex(content, options)
        
        # Create temporary directory for LaTeX compilation
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_file = os.path.join(tmpdir, 'document.tex')
            
            # Write TeX content
            with open(tex_file, 'w') as f:
                f.write(tex_content)
            
            # Copy any required files (images, bibliography, etc.)
            if options.get('resources_dir'):
                for file in Path(options['resources_dir']).glob('*'):
                    shutil.copy(file, tmpdir)
            
            # Compile LaTeX to PDF
            try:
                # Run pdflatex multiple times for references
                for _ in range(3):
                    result = subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', 'document.tex'],
                        cwd=tmpdir,
                        capture_output=True,
                        text=False,
                        encoding=None
                    )
                    if result.returncode != 0:
                        click.echo(f"pdflatex error: {result.stderr}", err=True)
                        # Save log file for debugging
                        log_file = os.path.join(tmpdir, 'document.log')
                        if os.path.exists(log_file):
                            with open(log_file, 'r', encoding='latin-1') as f:
                                click.echo("LaTeX log:", err=True)
                                click.echo(f.read()[-2000:], err=True)  # Last 2000 chars of log
                
                # Run bibtex if bibliography exists
                if '\\bibliography' in tex_content or '\\addbibresource' in tex_content:
                    subprocess.run(['bibtex', 'document'], cwd=tmpdir, capture_output=True, text=False, encoding=None)
                    # Run pdflatex again after bibtex
                    for _ in range(2):
                        subprocess.run(
                            ['pdflatex', '-interaction=nonstopmode', 'document.tex'],
                            cwd=tmpdir,
                            capture_output=True,
                            text=False,
                            encoding=None
                        )
                
                # Copy PDF to output location
                pdf_file = os.path.join(tmpdir, 'document.pdf')
                if os.path.exists(pdf_file):
                    shutil.copy(pdf_file, output_path)
                    return True
                else:
                    click.echo("Error: PDF generation failed", err=True)
                    return False
                    
            except FileNotFoundError:
                click.echo("Error: pdflatex not found. Please install a LaTeX distribution.", err=True)
                return False
    
    def convert_to_html(self, content: str, options: Dict) -> str:
        """Convert markdown to HTML using pandoc"""
        try:
            # Use pandoc for high-quality HTML conversion
            result = subprocess.run(
                ['pandoc', '-f', 'markdown', '-t', 'html5', '--standalone',
                 '--mathjax', '--highlight-style=pygments'],
                input=content,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except FileNotFoundError:
            click.echo("Warning: pandoc not found. Using basic HTML conversion.", err=True)
            # Fallback to basic conversion
            try:
                import markdown
                return markdown.markdown(content, extensions=['extra', 'codehilite', 'toc'])
            except ImportError:
                # Ultra-basic HTML conversion
                html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Document</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        code {{ background: #f4f4f4; padding: 2px 4px; }}
    </style>
</head>
<body>
{content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}
</body>
</html>"""
                return html
        except subprocess.CalledProcessError as e:
            click.echo(f"Error in pandoc conversion: {e.stderr}", err=True)
            return ""
    
    def convert_to_docx(self, content: str, options: Dict, output_path: str) -> bool:
        """Convert markdown to DOCX using pandoc"""
        try:
            result = subprocess.run(
                ['pandoc', '-f', 'markdown', '-t', 'docx', '-o', output_path],
                input=content,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except FileNotFoundError:
            click.echo("Error: pandoc not found. Please install pandoc for DOCX conversion.", err=True)
            return False
        except subprocess.CalledProcessError as e:
            click.echo(f"Error in DOCX conversion: {e.stderr}", err=True)
            return False
    
    def convert_to_arxiv(self, content: str, options: Dict, output_dir: str) -> bool:
        """Create ArXiv-ready submission package"""
        # Set ArXiv mode
        options['arxiv_mode'] = True
        
        # Convert to TeX
        tex_content = self.convert_to_tex(content, options)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Write main.tex
        tex_file = os.path.join(output_dir, 'main.tex')
        with open(tex_file, 'w') as f:
            f.write(tex_content)
        
        # Create bibliography file if needed
        if options.get('bibliography'):
            bib_file = os.path.join(output_dir, 'references.bib')
            shutil.copy(options['bibliography'], bib_file)
        
        # Copy figures if any
        if options.get('figures_dir'):
            for fig in Path(options['figures_dir']).glob('*'):
                if fig.suffix in ['.png', '.jpg', '.pdf', '.eps']:
                    shutil.copy(fig, output_dir)
        
        # Try to compile to generate .bbl file
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Copy files to temp dir
                for file in Path(output_dir).glob('*'):
                    shutil.copy(file, tmpdir)
                
                # Compile
                subprocess.run(['pdflatex', 'main.tex'], cwd=tmpdir, capture_output=True, check=True)
                if os.path.exists(os.path.join(tmpdir, 'references.bib')):
                    subprocess.run(['bibtex', 'main'], cwd=tmpdir, capture_output=True)
                    subprocess.run(['pdflatex', 'main.tex'], cwd=tmpdir, capture_output=True)
                
                # Copy .bbl file back
                bbl_file = os.path.join(tmpdir, 'main.bbl')
                if os.path.exists(bbl_file):
                    shutil.copy(bbl_file, output_dir)
        except (FileNotFoundError, subprocess.CalledProcessError):
            click.echo("Note: pdflatex not available, skipping .bbl generation", err=False)
        
        # Remove .bib file (ArXiv uses .bbl)
        bib_path = os.path.join(output_dir, 'references.bib')
        if os.path.exists(bib_path):
            os.remove(bib_path)
        
        # Create tar archive
        tar_file = f"{output_dir}.tar.gz"
        subprocess.run(['tar', '-czf', tar_file, '-C', os.path.dirname(output_dir), 
                       os.path.basename(output_dir)], check=True)
        
        click.echo(f"ArXiv package created: {tar_file}")
        return True


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-f', '--format', 'output_format', 
              type=click.Choice(['tex', 'pdf', 'html', 'docx', 'epub', 'rst', 'arxiv']),
              default='tex',
              help='Output format (default: tex)')
@click.option('-o', '--output', 'output_path',
              help='Output file/directory path')
@click.option('-t', '--template', 
              help='Custom LaTeX template file')
@click.option('--arxiv', is_flag=True,
              help='Use ArXiv-optimized settings')
@click.option('--french-quotes', is_flag=True,
              help='Use French-style quotes')
@click.option('--unnumbered', is_flag=True,
              help='Use unnumbered sections')
@click.option('--document-class', default='article',
              type=click.Choice(['article', 'book', 'report']),
              help='LaTeX document class')
@click.option('--bibliography', type=click.Path(exists=True),
              help='BibTeX bibliography file')
@click.option('--figures', 'figures_dir', type=click.Path(exists=True),
              help='Directory containing figures')
@click.option('--metadata', type=click.Path(exists=True),
              help='JSON file with document metadata')
@click.option('--watch', is_flag=True,
              help='Watch for changes and auto-convert')
@click.option('-v', '--verbose', is_flag=True,
              help='Verbose output')
def md2x(input_file, output_format, output_path, template, arxiv, 
         french_quotes, unnumbered, document_class, bibliography,
         figures_dir, metadata, watch, verbose):
    """
    md2x - Universal Markdown Converter
    
    Convert Markdown files to various formats optimized for academic use.
    
    Examples:
        md2x paper.md -f pdf
        md2x paper.md -f arxiv -o submission/
        md2x paper.md -f html --watch
    """
    
    converter = UniversalConverter()
    
    # Load metadata if provided
    metadata_dict = {}
    if metadata:
        with open(metadata, 'r') as f:
            metadata_dict = json.load(f)
    
    # Prepare options
    options = {
        'french_quote': french_quotes,
        'unnumbered': unnumbered,
        'document_class': document_class,
        'arxiv_mode': arxiv,
        'bibliography': bibliography,
        'figures_dir': figures_dir,
        'metadata': metadata_dict,
        'template': template,
        'verbose': verbose
    }
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine output path if not specified
    if not output_path:
        base_name = Path(input_file).stem
        if output_format == 'arxiv':
            output_path = f"{base_name}_arxiv"
        elif output_format in ['tex', 'pdf', 'html', 'docx']:
            output_path = f"{base_name}.{output_format}"
        else:
            output_path = f"{base_name}_output"
    
    # Convert based on format
    if verbose:
        click.echo(f"Converting {input_file} to {output_format}...")
    
    success = False
    
    if output_format == 'tex':
        tex_content = converter.convert_to_tex(content, options)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        success = True
        
    elif output_format == 'pdf':
        success = converter.convert_to_pdf(content, options, output_path)
        
    elif output_format == 'html':
        html_content = converter.convert_to_html(content, options)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        success = True
        
    elif output_format == 'docx':
        success = converter.convert_to_docx(content, options, output_path)
        
    elif output_format == 'arxiv':
        success = converter.convert_to_arxiv(content, options, output_path)
    
    else:
        click.echo(f"Format {output_format} not yet implemented", err=True)
    
    if success:
        click.echo(f"✓ Conversion successful: {output_path}")
    else:
        click.echo("✗ Conversion failed", err=True)
        return 1
    
    # Watch mode
    if watch:
        click.echo(f"Watching {input_file} for changes... (Ctrl+C to stop)")
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class ChangeHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path == input_file:
                    click.echo(f"\nFile changed, reconverting...")
                    # Recursive call to md2x
                    ctx = click.get_current_context()
                    ctx.invoke(md2x, input_file=input_file, 
                             output_format=output_format,
                             output_path=output_path,
                             template=template,
                             arxiv=arxiv,
                             french_quotes=french_quotes,
                             unnumbered=unnumbered,
                             document_class=document_class,
                             bibliography=bibliography,
                             figures_dir=figures_dir,
                             metadata=metadata,
                             watch=False,
                             verbose=verbose)
        
        handler = ChangeHandler()
        observer = Observer()
        observer.schedule(handler, path=os.path.dirname(input_file) or '.', recursive=False)
        observer.start()
        
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            click.echo("\nStopped watching.")
        observer.join()


if __name__ == '__main__':
    md2x()