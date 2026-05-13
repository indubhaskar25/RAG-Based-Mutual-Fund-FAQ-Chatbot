"""
Phase 1: PDF Parser
Extracts text and tabular data from mutual fund PDFs (Factsheets, SIDs).
Note: For this project, Groww HTML pages are the primary source.
      This module is provided for future extensibility with official AMC PDFs.
"""

import fitz  # PyMuPDF
import pdfplumber
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFParser:
    """Extracts text and tabular data from mutual fund PDFs."""

    @staticmethod
    def extract_text(pdf_path: str) -> Optional[str]:
        """Extracts general text using PyMuPDF for fast, layout-aware extraction."""
        try:
            text_content = []
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text_content.append(page.get_text("text"))
            full_text = "\n".join(text_content)
            logger.info(f"Extracted {len(full_text)} chars from {pdf_path}")
            return full_text
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return None

    @staticmethod
    def extract_tables(pdf_path: str) -> List[List[List[str]]]:
        """Extracts tables using pdfplumber — critical for fee and load structures."""
        tables_data = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        cleaned_table = []
                        for row in table:
                            if not row:
                                continue
                            cleaned_row = [
                                cell.replace("\n", " ") if cell else "" for cell in row
                            ]
                            cleaned_table.append(cleaned_row)
                        tables_data.append(cleaned_table)
            logger.info(f"Extracted {len(tables_data)} tables from {pdf_path}")
            return tables_data
        except Exception as e:
            logger.error(f"Error extracting tables from {pdf_path}: {e}")
            return []

    @staticmethod
    def format_table_as_markdown(table: List[List[str]]) -> str:
        """Converts an extracted table into Markdown for better LLM processing."""
        if not table:
            return ""

        md_lines = []
        # Header
        md_lines.append("| " + " | ".join(table[0]) + " |")
        # Separator
        md_lines.append("|" + "|".join(["---"] * len(table[0])) + "|")
        # Body rows
        for row in table[1:]:
            row = row + [""] * (len(table[0]) - len(row))
            md_lines.append("| " + " | ".join(row[: len(table[0])]) + " |")

        return "\n".join(md_lines)
