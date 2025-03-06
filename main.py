import os
import pandas as pd
import pdfplumber
import re
from extract_from_qc import *
from extract_basic import *
from extract_from_invoices import *
from extract_from_po import *
from excel_function import *

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
        extracted_values = {}

        required_pdf_types = {"Quality Control Sheet PDF", "Invoice PDF", "Purchase Order PDF"}
        pdf_type_counts = {key: 0 for key in required_pdf_types}

        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory, pdf_file)
            text = extract_text_with_pdfplumber(pdf_path)
            tables = extract_tables_with_pdfplumber(pdf_path)
            if not text:
                continue  # Skip PDFs with no text
            
            pdf_type = classify_pdf(text)
            if pdf_type in required_pdf_types:
                pdf_type_counts[pdf_type] += 1

            if pdf_type_counts[pdf_type] > 1:
                print(f"ERROR: More than one '{pdf_type}' found. Only one is allowed.")
                return
            
            if pdf_type == "Quality Control Sheet PDF":            
                accessories_weight = extract_accessories_weight(text)
                loss_perct = extract_loss_perct(tables)
                raw_cert = extract_raw_cert(tables)
                used_qty = extract_used_qty(tables)
                extracted_values.update({
                        "accessories_weight": accessories_weight,
                        "loss_perct": loss_perct,
                        "raw_cert": raw_cert,
                        "used_qty": used_qty
                    })
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
                extracted_values.update({
                    "invoice_number": invoice_number,
                    "invoice_date": invoice_date,
                    "invoice_order_no": invoice_order_no,
                    "net_weight": net_weight,
                    "gross_weight": gross_weight,
                    "quantity_type": quantity_type,
                    "quantity": quantity,
                    "goods_description": goods_description,
                    "goods_composition": goods_composition,
                    "pkg_no": pkg_no,
                    "country_name": country_name,
                    "country_iso": country_iso,
                    "mode_of_transport": mode_of_transport
                })
            
            elif pdf_type == "Purchase Order PDF":
                article_no = extract_article_no(text)
                gender = extract_gender(text)
                po_order_no = extract_order_no_from_po(text)                
                country_list = extract_country_list(text)
                extracted_values.update({
                    "article_no": article_no,
                    "gender": gender,
                    "po_order_no": po_order_no,
                    "country_list": country_list
                })
    
        # Ensure exactly one of each required pdf_type is present
        if any(count != 1 for count in pdf_type_counts.values()):
            print(f"ERROR: Invalid PDF count. Each required PDF type must be exactly one.")
            print(f"Current counts: {pdf_type_counts}")
            return
    
        # Check if all lists in extracted_values are of the same length and none are empty
        list_lengths = [len(v) for v in extracted_values.values() if isinstance(v, list)]
        if not list_lengths:
            print("WARNING: No data extracted from PDFs.")
            return
        
        if len(set(list_lengths)) != 1:
            print("ERROR: Extracted lists are not of the same length.")
            return
        
        if any(length == 0 for length in list_lengths):
            print("ERROR: One or more extracted lists are empty.")
            return

        # Check if country_iso (Invoice) matches country_list (PO)
        if "country_iso" in extracted_values and "country_list" in extracted_values:
            country_iso_set = set(extracted_values["country_iso"])
            country_list_set = set(extracted_values["country_list"])
            
            if country_iso_set != country_list_set:
                print("ERROR: Country ISO codes (Invoice) do not match Country List (PO).")
                print(f"Country ISO: {country_iso_set}")
                print(f"Country List: {country_list_set}")
                return
        
        
        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(extracted_values)
        
        # Check if PO Order No matches Invoice Order No for each row
        for index, row in df.iterrows():
            if row["po_order_no"] != row["invoice_order_no"]:
                print(f"ERROR: PO Order No '{row['po_order_no']}' does not match Invoice Order No '{row['invoice_order_no']}' in row {index + 1}.")
                return
            
        # Drop the 'Country ISO' and 'Invoice Order No' columns from the DataFrame
        df = df.drop(columns=["country_iso", "invoice_order_no"])
        # Add a new column "Challan No" to the DataFrame with default value None
        df["challan_consignee"] = None
        df["challan_no"] = None
        df["challan_date"] = None
        
        print(df)
        
        # Save the DataFrame to an Excel file
        # output_file_path = os.path.join(directory, 'invoice_data.xlsx')
        # save_excel(df, 'invoice_data')
        # save_excel(df, output_file_path)
      
    except Exception as e:
        print(f"ERROR: An unexpected error occurred - {e}")

if __name__ == "__main__":
    directory = r'C:\Users\Altersense\Desktop\tc'
    extract_pdf_data(directory)