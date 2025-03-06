import pandas as pd
import pdfplumber
import re


def extract_text_with_pdfplumber(pdf_path):
    """Extracts text from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text if text.strip() else ""
    except Exception as e:
        # print(f"ERROR: Failed to extract text from {pdf_path} - {e}")
        return ""

def extract_tables_with_pdfplumber(pdf_path):
    """Extracts tables from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return [page.extract_table() for page in pdf.pages if page.extract_table()]
    except Exception as e:
        # print(f"ERROR: Failed to extract tables from {pdf_path} - {e}")
        return []

def classify_pdf(text):
    """Classifies a PDF based on its text content."""
    if text.startswith("INVOICE"):
        return "Invoice PDF"
    elif text.startswith("Purchase Order"):
        return "Purchase Order PDF"
    elif text.startswith("SUSTAINABLE TEXTILE PRODUCTS - QUANTITY CONTROL SHEET"):
        return "Quality Control Sheet PDF"
    return "Unknown PDF"