import re
from typing import Dict, List, Tuple

class ArxivMetadata:
    """
    Extract and format metadata for ArXiv submissions
    """
    @staticmethod
    def extract_title(string: str) -> Tuple[str, str]:
        """
        Extract title from markdown and format for LaTeX
        """
        # Look for the first H1 header
        title_match = re.search(r"^#\s+(.+?)$", string, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # Remove the title from the content
            string = re.sub(r"^#\s+.+?$", "", string, count=1, flags=re.MULTILINE)
            return title, string
        return "", string
    
    @staticmethod
    def extract_authors(string: str) -> Tuple[str, str]:
        """
        Extract author information from markdown
        Looking for patterns like **Authors:** or **Author:**
        """
        author_match = re.search(r"\*\*Authors?:\*\*\s*(.+?)(?=\n|$)", string, re.MULTILINE)
        if author_match:
            authors = author_match.group(1).strip()
            # Remove the author line from content
            string = re.sub(r"\*\*Authors?:\*\*\s*.+?(?=\n|$)", "", string, flags=re.MULTILINE)
            return authors, string
        return "", string
    
    @staticmethod
    def extract_abstract(string: str) -> Tuple[str, str]:
        """
        Extract abstract section from markdown
        """
        # Look for ## Abstract section
        abstract_match = re.search(r"^##\s+Abstract\s*\n+([\s\S]+?)(?=^##|\Z)", string, re.MULTILINE)
        if abstract_match:
            abstract = abstract_match.group(1).strip()
            # Remove the abstract section from content
            string = re.sub(r"^##\s+Abstract\s*\n+[\s\S]+?(?=^##|\Z)", "", string, count=1, flags=re.MULTILINE)
            return abstract, string
        return "", string
    
    @staticmethod
    def format_title_block(title: str, authors: str, date: str = "") -> str:
        """
        Format the title block for ArXiv
        """
        title_block = ""
        
        if title:
            title_block += f"\\title{{{title}}}\n"
        
        if authors:
            # Simple author formatting, can be enhanced later
            author_list = authors.split(",")
            if len(author_list) == 1:
                title_block += f"\\author{{{authors.strip()}}}\n"
            else:
                formatted_authors = " \\and ".join([a.strip() for a in author_list])
                title_block += f"\\author{{{formatted_authors}}}\n"
        
        if date:
            title_block += f"\\date{{{date}}}\n"
        else:
            title_block += "\\date{\\today}\n"
        
        title_block += "\n\\maketitle\n"
        
        return title_block


class ArxivTable:
    """
    Convert markdown tables to LaTeX tables
    """
    @staticmethod
    def convert_tables(string: str) -> str:
        """
        Convert markdown tables to LaTeX format
        """
        # Find all tables in the markdown
        table_pattern = r"((?:^\|.+\|$\n)+)"
        tables = re.finditer(table_pattern, string, re.MULTILINE)
        
        for table_match in tables:
            table_text = table_match.group(0)
            latex_table = ArxivTable._convert_single_table(table_text)
            string = string.replace(table_text, latex_table)
        
        return string
    
    @staticmethod
    def _convert_single_table(table_text: str) -> str:
        """
        Convert a single markdown table to LaTeX
        """
        lines = table_text.strip().split('\n')
        if len(lines) < 2:
            return table_text
        
        # Parse the table
        rows = []
        for line in lines:
            # Remove leading and trailing pipes and split
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            rows.append(cells)
        
        # Check if second row is separator
        is_header_separator = all(re.match(r'^[-:]+$', cell.strip()) for cell in rows[1])
        
        if is_header_separator and len(rows) > 2:
            header = rows[0]
            data = rows[2:]
            col_count = len(header)
        else:
            data = rows
            col_count = len(rows[0]) if rows else 0
        
        # Build LaTeX table
        latex = "\\begin{table}[h]\n\\centering\n"
        latex += "\\begin{tabular}{" + "l" * col_count + "}\n"
        latex += "\\toprule\n"
        
        if is_header_separator and len(rows) > 2:
            latex += " & ".join(header) + " \\\\\n"
            latex += "\\midrule\n"
        
        for row in data:
            latex += " & ".join(row) + " \\\\\n"
        
        latex += "\\bottomrule\n"
        latex += "\\end{tabular}\n"
        latex += "\\caption{Table caption}\n"
        latex += "\\label{tab:label}\n"
        latex += "\\end{table}\n"
        
        return latex


class ArxivMath:
    """
    Handle mathematical expressions for ArXiv
    """
    @staticmethod
    def convert_math(string: str) -> str:
        """
        Convert markdown math to LaTeX math
        """
        # Convert display math blocks ($$...$$)
        string = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', string, flags=re.DOTALL)
        
        # Convert inline math ($...$) - already LaTeX compatible
        # but ensure they're not escaped
        string = re.sub(r'(?<!\\)\$([^\$]+?)\$', r'$\1$', string)
        
        return string


class ArxivCitation:
    """
    Handle citations and bibliography for ArXiv
    """
    @staticmethod
    def convert_citations(string: str) -> str:
        """
        Convert markdown-style citations to LaTeX \cite commands
        Looks for patterns like [1], [Ceccarelli2025], etc.
        """
        # Pattern for numeric citations [1], [2,3], [1-3]
        string = re.sub(r'\[(\d+(?:[-,]\d+)*)\]', r'\\cite{\1}', string)
        
        # Pattern for author-year citations [Author2023]
        string = re.sub(r'\[([A-Za-z]+\d{4}[a-z]?)\]', r'\\cite{\1}', string)
        
        return string
    
    @staticmethod
    def extract_bibliography(string: str) -> Tuple[str, str]:
        """
        Extract bibliography section and format for BibTeX
        """
        # Look for References or Bibliography section
        bib_match = re.search(r"^##?\s+(References|Bibliography)\s*\n+([\s\S]+?)(?=^##|\Z)", 
                             string, re.MULTILINE | re.IGNORECASE)
        
        if bib_match:
            bib_content = bib_match.group(2)
            # Remove bibliography from main content
            string = re.sub(r"^##?\s+(References|Bibliography)\s*\n+[\s\S]+?(?=^##|\Z)", 
                           "", string, flags=re.MULTILINE | re.IGNORECASE)
            
            # Convert to BibTeX entries (simplified)
            bibtex = ArxivCitation._convert_to_bibtex(bib_content)
            return bibtex, string
        
        return "", string
    
    @staticmethod
    def _convert_to_bibtex(bib_content: str) -> str:
        """
        Simple conversion of bibliography entries to BibTeX format
        This is a simplified version - could be enhanced
        """
        # For now, just return a bibliography command
        # In a full implementation, this would parse entries and create .bib file
        return "\\bibliography{references}"


class ArxivEnhancedConverter:
    """
    Main converter class that combines all ArXiv-specific conversions
    """
    def __init__(self):
        self.metadata = ArxivMetadata()
        self.table = ArxivTable()
        self.math = ArxivMath()
        self.citation = ArxivCitation()
    
    def convert_for_arxiv(self, string: str, metadata: Dict[str, str] = None) -> Dict[str, str]:
        """
        Perform all ArXiv-specific conversions
        Returns a dictionary with converted components
        """
        result = {}
        
        # Extract metadata
        title, string = self.metadata.extract_title(string)
        authors, string = self.metadata.extract_authors(string)
        abstract, string = self.metadata.extract_abstract(string)
        
        # Format title block
        result['title_block'] = self.metadata.format_title_block(
            title, 
            authors, 
            metadata.get('date', '') if metadata else ''
        )
        
        # Format abstract
        if abstract:
            result['abstract'] = f"\\begin{{abstract}}\n{abstract}\n\\end{{abstract}}\n"
        else:
            result['abstract'] = ""
        
        # Convert content
        string = self.table.convert_tables(string)
        string = self.math.convert_math(string)
        string = self.citation.convert_citations(string)
        
        # Extract bibliography
        bibliography, string = self.citation.extract_bibliography(string)
        result['bibliography'] = bibliography
        
        # Store the processed body
        result['body'] = string
        
        return result