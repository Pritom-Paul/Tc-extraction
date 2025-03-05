import re

def extract_article_no(text):
    # Find the line that ends with 'Qty/Article' and capture the next line
    match = re.search(r'Qty/Article\s*\n(\d+)', text)
    
    if match:
        article_no = match.group(1)  # Extract the first number in the next line
        print("ARTICLE NUMBER:", article_no)
        return article_no
    else:
        print("ARTICLE NUMBER NOT FOUND")
        return None

def extract_gender(text):
    # Find the line that contains 'Customs Customer Group:'
    gender_pattern = r"Customs Customer Group:\s+(.+)"
    match = re.search(gender_pattern, text)
    if match:
        gender = match.group(1)
        print("GENDER:", gender)
        return gender
    else:
        print("GENDER NOT FOUND")
        return None

def extract_order_no_from_po(text):
    # Find the line that contains 'Order No:'
    order_no_pattern = r"Order No:\s*(\d+-\d+)"
    match = re.search(order_no_pattern, text)
    if match:
        order_no = match.group(1)
        print("ORDER NUMBER FROM PO:", order_no)
        return order_no
    else:
        print("ORDER NUMBER FROM PO NOT FOUND")
        return None