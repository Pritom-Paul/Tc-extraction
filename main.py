import os
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
        print(f"ERROR: Failed to extract text from {pdf_path} - {e}")
        return ""

def extract_tables_with_pdfplumber(pdf_path):
    """Extracts tables from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return [page.extract_table() for page in pdf.pages if page.extract_table()]
    except Exception as e:
        print(f"ERROR: Failed to extract tables from {pdf_path} - {e}")
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

def extract_qcValue_from_tables(tables):
    """Extracts QC values from tables."""
    try:
        all_rows = [row for table in tables for row in table if row and any(row)]
        if len(all_rows) < 3:
            return None  # Not enough rows

        target_row = all_rows[-3]  # Third-to-last row
        if len(target_row) >= 17:
            return {
                "loss_perct": target_row[7],
                "raw_cert": target_row[14],
                "used_qty": target_row[16].replace(" ", ""),
            }
    except Exception as e:
        print(f"ERROR: Failed to extract Quality Control Sheet values - {e}")
    
    return None

def extract_accessories_weight(text):
    """Extracts the 'Per Pcs Accessories Weight' value from the text using regex."""
    try:
        match = re.search(r"Per Pcs Accessories Weight\s+([0-9]*\.?[0-9]+)", text)
        return match.group(1) if match else None
    except Exception as e:
        print(f"ERROR: Failed to extract accessories weight - {e}")
    return None

def extract_pdf_data(directory):
    """Extracts data from PDFs in a directory and compiles results into a DataFrame."""
    try:
        if not os.path.exists(directory):
            print(f"ERROR: Directory does not exist - {directory}")
            return
        
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith(".pdf")]
        if not pdf_files:
            print(f"WARNING: No PDF files found in directory - {directory}")
            return
        
        print(f"INFO: Processing {len(pdf_files)} PDFs in directory {directory}")
        extracted_values = []

        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory, pdf_file)
            text = extract_text_with_pdfplumber(pdf_path)
            if not text:
                continue  # Skip PDFs with no text
            
            pdf_type = classify_pdf(text)
            if pdf_type == "Quality Control Sheet PDF":
                tables = extract_tables_with_pdfplumber(pdf_path)
                qc_table_values = extract_qcValue_from_tables(tables)
                accessories_weight = extract_accessories_weight(text)

                if qc_table_values and accessories_weight:
                    qc_table_values["accessories_weight"] = accessories_weight
                    extracted_values.append(qc_table_values)

        if extracted_values:
            df = pd.DataFrame(extracted_values)
            print("\nINFO: Final extracted data:")
            print(df)
        else:
            print("\nWARNING: No valid data extracted from any PDF.")

    except Exception as e:
        print(f"ERROR: An unexpected error occurred - {e}")

if __name__ == "__main__":
    directory = r'C:\Users\Altersense\Desktop\tc'
    extract_pdf_data(directory)