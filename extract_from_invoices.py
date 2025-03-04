import re

def extract_net_weight(text):
    net_weights = re.findall(r'Net Weight:\s+([\d.]+)\s*KG', text)
    if net_weights:
        print("NET WEIGHT",net_weights)
        return net_weights
    else:
        print("Net Weight could not be extracted")
        return None

def extract_gross_weight(text):
    gross_weights = re.findall(r'Gross Weight:\s+([\d.]+)\s*KG', text)
    if gross_weights:    
        print("GROSS WEIGHT", gross_weights)
        return gross_weights
    else:
        print("Gross Weight could not be extracted") 
    
def extract_quantity_type(text):
    match = re.findall(r'(\S+)\s+USD\s+USD', text)
    if match:    
        print("QUANTITY TYPE", match)
        return match
    else:
        print("Quantity Type could not be extracted")
        return None
    
def extract_pkg_no(text):
    match = re.findall(r'(\S+\sCartons)', text)
    if match:    
        print("PKG NO", match)
        return match
    else:
        print("PKG NO could not be extracted")
        return None

        
def extract_invoice_number(text):
    invoice_numbers = re.findall(r'Invoice No:\s*(\d+)', text)
    if invoice_numbers:    
        print("INVOICE NUMBER", invoice_numbers)
        return invoice_numbers
    else:
        print("Invoice Number could not be extracted")
        return None
        
def extract_invoice_date(text):
    invoice_dates = re.findall(r'Invoice Date:\s*(\d{2}-\d{2}-\d{4})', text)
    if invoice_dates:
        print("INVOICE DATE:", invoice_dates)
        return invoice_dates
    else:
        print("Invoice Date could not be extracted")
        return None

def extract_country_name(text):
    # Find the two-letter codes that appear just before 'Port of Loading:'
    matches = re.findall(r'([A-Z]{2})\nPort of Loading:', text)
    
    country_names = []
    
    # For each match, find the line above the two-letter code and extract the country name
    for match in matches:
        # Match the two-letter code and the line immediately above it
        pattern = r'(.*)\n' + match + r'\nPort of Loading:'
        country_match = re.search(pattern, text)
        
        if country_match:
            # If the match is found, append the country name (line above the code)
            country_names.append(country_match.group(1).strip())
    
    if country_names:
        print("COUNTRY NAME", country_names)
        return country_names
    else:
        print("Country Name could not be extracted")
        return None

def extract_quantity(text):
    quantities = re.findall(r'\b(\d+)\s+\d+\.\d+\s+\d+\.\d+\b', text)
    if quantities:    
        print("QUANTITY", quantities)
        return quantities
    else:
        print("Quantity could not be extracted")
        return None

def extract_goods_description(text):
    goods_descriptions = []
    lines = text.split('\n')
    for i in range(len(lines) - 1):  # Adjust to prevent index error
        line = lines[i]
        match = re.search(r'\d+\s+Cartons\s+(.*?)\s+P', line)
        if match:
            goods_description = match.group(1)
            # Check the next line for additional information
            next_line = lines[i + 1]
            if len(next_line.split()) <= 3 and not next_line.strip().split()[-1].isdigit():
                goods_description += " " + next_line  # Append the next line
            goods_descriptions.append(goods_description)
    if goods_descriptions:
        print("GOODS DESCRIPTION", goods_descriptions)
        return goods_descriptions
    else:
        print("Goods Description could not be extracted")
        return None

def extract_goods_composition(text):
    goods_compositions = []
    lines = text.split('\n')
    found_usd_usd = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if 'USD USD' in line:
            found_usd_usd = True
            i += 1
            continue
        if found_usd_usd:
            composition_parts = []
            # Special processing for the first line after "USD USD"
            if i < len(lines):
                words = lines[i].split()
                if len(words) > 3:
                    first_sentence = ' '.join(words[:-3])  # Preserve spaces between words
                else:
                    i += 1
                    if i < len(lines):
                        words = lines[i].split()
                        first_sentence = ' '.join(words[:-3])  # Preserve spaces between words
                
                # Further clean-up for parenthesis within the first sentence
                first_sentence = first_sentence.split('PCS/PACK')[0].split('(')[0].split(')')[0].strip()
                # Strip double quotes if present
                if first_sentence.startswith('"'):
                    first_sentence = first_sentence[1:].strip()
                composition_parts.append(first_sentence)
                i += 1

            # Process subsequent lines
            while i < len(lines) and not lines[i].startswith("Container"):
                current_sentence = lines[i].split('PCS/PACK')[0].split('(')[0].split(')')[0].strip()
                composition_parts.append(current_sentence)
                i += 1
            
            composition = " ".join(composition_parts).strip()
            if "Container" in composition:
                composition = composition.split("Container")[0].strip()
            goods_compositions.append(composition)
            found_usd_usd = False
        else:
            i += 1
    
    if goods_compositions:
        print("GOODS COMPOSITION", goods_compositions)
        return goods_compositions
    else:
        print("Goods Composition could not be extracted")
        return None

def extract_order_no(text):
    order_nos = []
    lines = text.split('\n')
    for line in lines:
        match = re.search(r'H&M Order No: (\d{6}-\d{4})', line)
        if match:
            order_nos.append(match.group(1))
    if order_nos:    
        print("ORDER NO", order_nos)
        return order_nos
    else:
        print("Order No could not be extracted")
        return None

def extract_country_iso(text):
    country_iso_values = re.findall(r'([A-Z]{2})\nPort of Loading:', text)
    if country_iso_values:    
        print("COUNTRY ISO", country_iso_values)
        return country_iso_values
    else :
        print("Country ISO could not be extracted")
        return None

def extract_mode_of_transport(text):
    # Find the sentence that starts with 'Mode of Transport' and the following line
    matches = re.findall(r'Mode of Transport:.*\n([A-Za-z]+)', text)
    
    mode_of_transport = []
    
    # For each match, check if the value on the next line is a single word
    for match in matches:
        # If it matches the condition of being a single word, append to the list
        if len(match.split()) == 1:
            mode_of_transport.append(match.strip())
    
    if mode_of_transport:
        print("MODE OF TRANSPORT:", mode_of_transport)
        return mode_of_transport
    else:
        print("Mode of Transport could not be extracted")
        return None