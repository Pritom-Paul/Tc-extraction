import os
import pandas as pd
import pdfplumber
import re
from extract_from_qc import *
from extract_basic import *
from extract_from_invoices import *
from extract_from_po import *

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
            tables = extract_tables_with_pdfplumber(pdf_path)
            if not text:
                continue  # Skip PDFs with no text
            
            pdf_type = classify_pdf(text)
            
            if pdf_type == "Quality Control Sheet PDF":            
                qc_table_values = extract_qcValue_from_tables(tables)
                accessories_weight = extract_accessories_weight(text)

            elif pdf_type == "Invoice PDF":
                # print(text)
                invoice_number = extract_invoice_number(text)
                invoice_date = extract_invoice_date(text)
                invoice_order_no = extract_order_no_from_invoice(text)
                net_weight = extract_net_weight(text)
                gross_weight = extract_gross_weight(text)
                quantity_type = extract_quantity_type(text)
                quantity = extract_quantity(text)
                goods_description = extract_goods_description(text)
                goods_composition = extract_goods_composition(text)
                pkg_no = extract_pkg_no(text)
                country_name = extract_country_name(text)
                country_iso = extract_country_iso(text)
                mode_of_transport = extract_mode_of_transport(text)
            
            elif pdf_type == "Purchase Order PDF":
                # print(text)
                article_no = extract_article_no(text)
                gender = extract_gender(text)
                po_order_no = extract_order_no_from_po(text)                
                
    except Exception as e:
        print(f"ERROR: An unexpected error occurred - {e}")

if __name__ == "__main__":
    directory = r'C:\Users\Altersense\Desktop\tc'
    extract_pdf_data(directory)