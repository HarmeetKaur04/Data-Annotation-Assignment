import json

# Define the template for header extraction
header_template = {
    "Vendor Name": {"rule": "Find 'CPB Software (Germany) GmbH' as the vendor name"},
    "Customer Name": {"rule": "Find the customer name from the section starting with 'Musterkunde AG'"},
    "Invoice Number": {"rule": "Find 'Invoice No' and extract the numeric value following it"},
    "Invoice Date": {"rule": "Find 'Date' and extract the following date in DD/MM/YYYY or MM/DD/YYYY format"},
    "Customer Number": {"rule": "Find 'Customer No' and extract the following numeric value"},
    "Invoice Period": {
        "rule": "Find 'Period' and extract the start and end dates",
        "format": "Start Date - End Date"
    },
    "Total Amount (without VAT)": {"rule": "Find the 'Total Amount' without VAT and extract the value"},
    "VAT": {"rule": "Find 'VAT 19%' and extract the value"},
    "Gross Amount (with VAT)": {"rule": "Find 'Gross Amount incl. VAT' and extract the total"},
    "IBAN": {"rule": "Find 'IBAN' and extract the following alphanumeric string"},
    "BIC": {"rule": "Find 'BIC' and extract the following alphanumeric string"}
}

# Define the template for table extraction (line items)
table_template = {
    "Line Items": {
        "rule": "Find the section with service descriptions and extract rows of line items",
        "columns": {
            "Description": {"rule": "Extract the text from the first column as item/service description"},
            "Quantity": {"rule": "Extract the number of items or services from the second column"},
            "Price": {"rule": "Extract the price per item/service from the third column"},
            "Total Price": {"rule": "Extract the total price for each line item"}
        },
        "multiple_rows": True  # Indicates that the table contains multiple rows of data
    }
}

# Combine header and table templates into one structure
invoice_template = {
    "Header": header_template,
    "Table Data": table_template
}

# Output the template as JSON
json_template = json.dumps(invoice_template, indent=4)

# Simulate writing the JSON template to a file
with open("invoice_template.json", "w") as f:
    f.write(json_template)

# Print the template for verification
print(json_template)