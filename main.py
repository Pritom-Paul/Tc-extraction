import os
import pandas as pd
import pdfplumber
import re

def extract_text_with_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def extract_tables_with_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                tables.append(table)  # Collect full tables instead of extending rows
    return tables

def classify_pdf(text):
    if text.startswith("INVOICE"):
        return "Invoice PDF"
    elif text.startswith("Purchase Order"):
        return "Purchase Order PDF"
    elif text.startswith("SUSTAINABLE TEXTILE PRODUCTS - QUANTITY CONTROL SHEET"):
        return "Quality Control Sheet PDF"
    return "Unknown PDF"

def extract_qcValue_from_tables(tables):
    qc_table_values = []
    
    # Flatten all table rows
    all_rows = [row for table in tables for row in table if row and any(row)]
    
    if len(all_rows) < 3:
        return None  # Ensure there are enough rows to extract from
    
    target_row = all_rows[-3]  # Select the third-to-last row
    
    if len(target_row) >= 17:  # Ensure the row has enough columns
        return {
            "loss_perct": target_row[7],  # 8th column
            "raw_cert": target_row[14],  # 15th column
            "used_qty": target_row[16].replace(" ", "") # 17th column
        }

    return None

def extract_accessories_weight(text):
    # Pattern to match "Per Pcs Accessories Weight" followed by the number (e.g., "0.0072")
    match = re.search(r"Per Pcs Accessories Weight\s+([0-9]*\.?[0-9]+)", text)
    if match:
        return match.group(1)
    return None

def extract_pdf_data(directory):
    try:
        extracted_values = []
        for pdf_file in os.listdir(directory):
            if pdf_file.lower().endswith(".pdf"):
                pdf_path = os.path.join(directory, pdf_file)
                text = extract_text_with_pdfplumber(pdf_path)

                if text:
                    pdf_type = classify_pdf(text)
                    print(f"{pdf_file}: {pdf_type}")
                    
                    
                    
                    if pdf_type == "Quality Control Sheet PDF":
                        tables = extract_tables_with_pdfplumber(pdf_path)
                        qc_table_values = extract_qcValue_from_tables(tables)
                        accessories_weight = extract_accessories_weight(text)
                        
                        if qc_table_values and accessories_weight:
                            extracted_values.append({
                                **qc_table_values,
                                "accessories_weight": accessories_weight  # Add extracted accessories weight
                            })
                        else:
                            print(f"{pdf_file}: No valid data extracted")
                else:
                    print(f"{pdf_file}: No text extracted")
        
        # Convert extracted_values to a DataFrame
        if extracted_values:
            df = pd.DataFrame(extracted_values)
            print(df)
        else:
            print("No valid data extracted from any PDF.")
                    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    directory = r'C:\Users\Altersense\Desktop\tc'
    extract_pdf_data(directory)