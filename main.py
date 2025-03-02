import os
import pandas as pd
import pdfplumber
import re

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self.extract_text()
        self.tables = self.extract_tables()

    def extract_text(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
        return text

    def extract_tables(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            tables = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    tables.append(table)
        return tables

    def classify_pdf(self):
        if self.text.startswith("INVOICE"):
            return "InvoicePDF"
        elif self.text.startswith("Purchase Order"):
            return "PurchaseOrderPDF"
        elif self.text.startswith("SUSTAINABLE TEXTILE PRODUCTS - QUANTITY CONTROL SHEET"):
            return "QualityControlSheetPDF"
        return "UnknownPDF"

    def extract_data(self):
        raise NotImplementedError("Subclasses should implement this method")

class QualityControlSheetPDFExtractor(PDFExtractor):
    def extract_qcValue_from_tables(self):
        qc_table_values = []
        
        all_rows = [row for table in self.tables for row in table if row and any(row)]
        
        if len(all_rows) < 3:
            return None
        
        target_row = all_rows[-3]
        
        if len(target_row) >= 17:
            return {
                "loss_perct": target_row[7],
                "raw_cert": target_row[14],
                "used_qty": target_row[16].replace(" ", "")
            }
        return None

    def extract_accessories_weight(self):
        match = re.search(r"Per Pcs Accessories Weight\s+([0-9]*\.?[0-9]+)", self.text)
        if match:
            return match.group(1)
        return None

    def extract_data(self):
        qc_table_values = self.extract_qcValue_from_tables()
        accessories_weight = self.extract_accessories_weight()
        
        if qc_table_values and accessories_weight:
            return {
                **qc_table_values,
                "accessories_weight": accessories_weight
            }
        return None

class InvoicePDFExtractor(PDFExtractor):
    def extract_data(self):
        # Implement extraction logic for Invoice PDFs
        pass

class PurchaseOrderPDFExtractor(PDFExtractor):
    def extract_data(self):
        # Implement extraction logic for Purchase Order PDFs
        pass

class PDFExtractorFactory:
    @staticmethod
    def get_extractor(pdf_path):
        extractor = PDFExtractor(pdf_path)
        pdf_type = extractor.classify_pdf()
        
        if pdf_type == "QualityControlSheetPDF":
            return QualityControlSheetPDFExtractor(pdf_path)
        elif pdf_type == "InvoicePDF":
            return InvoicePDFExtractor(pdf_path)
        elif pdf_type == "PurchaseOrderPDF":
            return PurchaseOrderPDFExtractor(pdf_path)
        else:
            return None

def extract_pdf_data(directory):
    try:
        extracted_values = []
        for pdf_file in os.listdir(directory):
            if pdf_file.lower().endswith(".pdf"):
                pdf_path = os.path.join(directory, pdf_file)
                extractor = PDFExtractorFactory.get_extractor(pdf_path)
                
                if extractor:
                    data = extractor.extract_data()
                    if data:
                        extracted_values.append(data)
                #     else:
                #         print(f"{pdf_file}: No valid data extracted")
                # else:
                #     print(f"{pdf_file}: Unsupported PDF type")
        
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