import json
import re

# Define a function to generalize the field extraction rule using regex
def create_general_rule(field_patterns):
    """
    Generate a regex-based rule that can match multiple variations of field names.
    
    Args:
    field_patterns (list of str): A list of possible patterns/field names.
    
    Returns:
    dict: A rule with a regex that matches any of the provided patterns.
    """
    # Join the patterns into a regex pattern that allows slight variations
    joined_patterns = "|".join([re.escape(pattern) for pattern in field_patterns])
    return {"rule": f"Find any of {joined_patterns} and extract the following value"}

# Generalize header extraction rules with variations
header_template = {
    "Vendor Name": create_general_rule(["Vendor", "Supplier", "Company"]),
    "Customer Name": create_general_rule(["Customer", "Client"]),
    "Invoice Number": create_general_rule(["Invoice No", "Invoice #", "Bill No"]),
    "Invoice Date": create_general_rule(["Date", "Invoice Date", "Billing Date"]),
    "Customer Number": create_general_rule(["Customer No", "Client ID", "Account No"]),
    "VAT Number": create_general_rule(["VAT No", "Tax ID"]),
    "Invoice Period": create_general_rule(["Period", "Invoice Period", "Billing Period"]),
    "Bank Details": {
        "IBAN": create_general_rule(["IBAN"]),
        "BIC": create_general_rule(["BIC", "Swift Code"])
    }
}

# Generalize table data extraction rules with column name variations
table_template = {
    "Table": {
        "Service Description": create_general_rule(["Description", "Service", "Item"]),
        "Quantity": create_general_rule(["Quantity", "Qty"]),
        "Unit Price": create_general_rule(["Unit Price", "Price per Item", "Cost"]),
        "Total Amount per Item": create_general_rule(["Total", "Amount", "Line Total"])
    }
}

# Combine header and table templates into the final JSON structure
invoice_template = {
    "Header": header_template,
    "Table": table_template
}

# Optimized caching of frequent patterns
frequent_patterns = {
    "Vendor Name": re.compile(r"(vendor|supplier|company)", re.IGNORECASE),
    "Invoice Number": re.compile(r"(invoice no|invoice #|bill no)", re.IGNORECASE)
    # Add other frequent patterns here for caching
}

# Function to extract data using cached patterns (optimization)
def extract_with_cache(field, text, pattern_cache):
    """
    Extract the data for a given field using cached regex patterns.
    
    Args:
    field (str): The field to extract (e.g., 'Invoice Number').
    text (str): The invoice text to search within.
    pattern_cache (dict): Cached regex patterns for common fields.
    
    Returns:
    str: Extracted value or 'N/A' if not found.
    """
    if field in pattern_cache:
        match = pattern_cache[field].search(text)
        if match:
            return match.group(1).strip()
    return "N/A"

# Convert the generalized template to JSON format
template_json = json.dumps(invoice_template, indent=4)

# Output JSON template (optimized and generalized)
with open("invoice_template_optimized.json", "w") as f:
    f.write(template_json)

# Print the template for verification
print(template_json)