import pandas as pd
import pdfplumber
import re

# def extract_qcValue_from_tables(tables):
#     """Extracts QC values from tables."""
#     try:
#         all_rows = [row for table in tables for row in table if row and any(row)]
#         if len(all_rows) < 3:
#             return None  # Not enough rows

#         target_row = all_rows[-3]  # Third-to-last row
#         if len(target_row) >= 17:
#             loss_perct = target_row[7]
#             raw_cert = target_row[14]
#             used_qty = target_row[16].replace(" ", "")
#             print( "Loss Perct",loss_perct)
#             print( "Raw Cert",raw_cert)
#             print( "Used Qty",used_qty)
#     except Exception as e:
#         print(f"ERROR: Failed to extract Quality Control Sheet values - {e}")
    
#     return None

def extract_accessories_weight(text):
    """Extracts the 'Per Pcs Accessories Weight' value from the text using regex."""
    try:
        match = re.search(r"Per Pcs Accessories Weight\s+([0-9]*\.?[0-9]+)", text)
        return match.group(1) if match else None
    except Exception as e:
        print(f"ERROR: Failed to extract accessories weight - {e}")
    return None

def extract_loss_perct(tables):
    """Extracts Loss Perct value from tables."""
    try:
        all_rows = [row for table in tables for row in table if row and any(row)]
        if len(all_rows) < 3:
            return None  # Not enough rows

        target_row = all_rows[-3]  # Third-to-last row
        if len(target_row) >= 17:
            loss_perct = target_row[7]
            print("Loss Perct:", loss_perct)
            return loss_perct
    except Exception as e:
        print(f"ERROR: Failed to extract Loss Perct - {e}")
    
    return None


def extract_raw_cert(tables):
    """Extracts Raw Cert value from tables."""
    try:
        all_rows = [row for table in tables for row in table if row and any(row)]
        if len(all_rows) < 3:
            return None  # Not enough rows

        target_row = all_rows[-3]  # Third-to-last row
        if len(target_row) >= 17:
            raw_cert = target_row[14]
            print("Raw Cert:", raw_cert)
            return raw_cert
    except Exception as e:
        print(f"ERROR: Failed to extract Raw Cert - {e}")
    
    return None


def extract_used_qty(tables):
    """Extracts Used Qty value from tables."""
    try:
        all_rows = [row for table in tables for row in table if row and any(row)]
        if len(all_rows) < 3:
            return None  # Not enough rows

        target_row = all_rows[-3]  # Third-to-last row
        if len(target_row) >= 17:
            used_qty = target_row[16].replace(" ", "")
            print("Used Qty:", used_qty)
            return used_qty
    except Exception as e:
        print(f"ERROR: Failed to extract Used Qty - {e}")
    
    return None
