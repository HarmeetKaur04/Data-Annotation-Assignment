import re

# Simple dictionary to convert number words to digits (for common numbers)
word_to_num = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, 
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, 
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, 
    "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100, 
    "thousand": 1000, "million": 1000000
}

def words_to_number(words):
    words = words.lower().replace("-", " ").split()
    result = 0
    current = 0
    for word in words:
        if word in word_to_num:
            scale = word_to_num[word]
            if scale < 100:
                current += scale
            else:
                current *= scale
        elif word == "and":
            continue
        else:
            return None  # Unrecognized word
    return result + current if current else None

def extract_invoice_amount(value_content):
    # Standardize the content to lowercase to handle case variations
    value_content = value_content.lower()
    
    # Look for known formats using regex
    patterns = [
        r"total amount[:\s]*€?\$?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))",  # Matches "Total Amount: 381,12 €"
        r"amount due[:\s]*€?\$?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))",    # Matches "Amount Due: 500,00 €"
        r"amount[:\s]*€?\$?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))",        # Matches "Amount: 1500,00 €"
        r"gross amount incl\. vat[:\s]*€?\$?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))",  # Matches "Gross Amount incl. VAT: 1000,25 €"
    ]
    
    # Try to match any of the patterns
    for pattern in patterns:
        match = re.search(pattern, value_content)
        if match:
            # Replace comma with a dot to correctly interpret the decimal part
            return match.group(1).replace(".", "").replace(",", ".")
    
    # Handling amounts in words, like "Amount: Five Hundred"
    words_pattern = r"amount[:\s]*(\w+.*\w+)"
    match = re.search(words_pattern, value_content)
    if match:
        amount_in_words = match.group(1)
        amount = words_to_number(amount_in_words)
        if amount is not None:
            return str(amount)
    
    # If no amount is found, return "N/A"
    return "N/A"

# Test cases
test_cases = [
    "Total Amount: 381,12 €",
    "Amount Due: 500,00 €",
    "Amount: Five Hundred ",
    "Amount: 1.500,00 €",
    "Gross Amount incl. VAT: 1.000,25 €"
]

# Testing the function
for test in test_cases:
    print(f"Input: {test} -> Extracted Amount: {extract_invoice_amount(test)}")
