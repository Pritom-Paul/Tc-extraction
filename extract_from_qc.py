import pandas as pd
import pdfplumber
import re

def extract_qcValue_from_tables(tables):
    """Extracts QC values from tables."""
    try:
        all_rows = [row for table in tables for row in table if row and any(row)]
        if len(all_rows) < 3:
            return None  # Not enough rows

        target_row = all_rows[-3]  # Third-to-last row
        if len(target_row) >= 17:
            loss_perct = target_row[7]
            raw_cert = target_row[14]
            used_qty = target_row[16].replace(" ", "")
            print( "Loss Perct",loss_perct)
            print( "Raw Cert",raw_cert)
            print( "Used Qty",used_qty)
            return {
                "loss_perct": loss_perct,
                "raw_cert": raw_cert,
                "used_qty": used_qty,
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
