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
                   
            accessories_weight = ""
            loss_perct = ""
            raw_cert = ""
            used_qty = ""
            
            invoice_number = []
            invoice_date = []
            invoice_order_no = []
            net_weight = []
            gross_weight = []
            quantity_type = []
            quantity = []
            goods_description = []
            goods_composition = []
            pkg_no = []
            country_name = []
            country_iso = []
            mode_of_transport = []
            
            article_no = ""
            gender = ""
            po_order_no = ""            
            country_list = []
            
            if pdf_type == "Quality Control Sheet PDF":            
                # qc_table_values = extract_qcValue_from_tables(tables)
                accessories_weight = extract_accessories_weight(text)
                loss_perct = extract_loss_perct(tables)
                raw_cert = extract_raw_cert(tables)
                used_qty = extract_used_qty(tables)

            elif pdf_type == "Invoice PDF":
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
                article_no = extract_article_no(text)
                gender = extract_gender(text)
                po_order_no = extract_order_no_from_po(text)                
                country_list = extract_country_list(text)
            
        # Check the list_lengths of each list
        list_lengths = {
            "invoice_number": len(invoice_number),
            "invoice_date": len(invoice_date),
            "invoice_order_no": len(invoice_order_no),
            "net_weight": len(net_weight),
            "gross_weight": len(gross_weight),
            "quantity_type": len(quantity_type),
            "quantity": len(quantity),
            "goods_description": len(goods_description),
            "goods_composition": len(goods_composition),
            "pkg_no": len(pkg_no),
            "country_name": len(country_name),
            "invoice_country_iso": len(country_iso),
            "mode_of_transport": len(mode_of_transport),
            "po_country_list": len(country_list)
        }

        # Find any lists with a length mismatch
        mismatched_lengths = [key for key, value in list_lengths.items() if value != len(country_iso)]

        if mismatched_lengths:
            print(f"WARNING: Mismatched list lengths: {', '.join(mismatched_lengths)}")
            # return
        else:
            print("DATA EXTRACTION CAN BE DONE")
        
      
    except Exception as e:
        print(f"ERROR: An unexpected error occurred - {e}")

if __name__ == "__main__":
    directory = r'C:\Users\Altersense\Desktop\tc'
    extract_pdf_data(directory)