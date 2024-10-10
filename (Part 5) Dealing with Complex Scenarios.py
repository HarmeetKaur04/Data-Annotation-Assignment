import re
import json

# Dummy function to simulate reading multiple pages from a PDF
def extract_text_from_pdf(file_path):
    # Simulating multi-page text extraction
    page_1 = "Invoice No: 12345\nDate: 01.03.2024\nVendor: CPB Software\n"
    page_2 = "Service Description | Quantity | Unit Price | Total\nBasic Service | 1 | 100.00 € | 100.00 €\nExtended Service | Continued on next line\nDescription | 2 | 150.00 € | 300.00 €"
    return [page_1, page_2]

# Function to handle multi-page and multi-line extraction
def process_multi_page_invoice(text_pages):
    extracted_data = {}
    
    # Multi-page header extraction (assuming headers are on the first page)
    header_page = text_pages[0]
    try:
        extracted_data['Invoice Number'] = re.search(r'Invoice No:\s*(\d+)', header_page).group(1)
        extracted_data['Invoice Date'] = re.search(r'Date:\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4})', header_page).group(1)
        extracted_data['Vendor Name'] = re.search(r'Vendor:\s*(.+)', header_page).group(1)
    except AttributeError:
        # Fallback if headers are missing
        extracted_data['Invoice Number'] = "N/A"
        extracted_data['Invoice Date'] = "N/A"
        extracted_data['Vendor Name'] = "N/A"

    # Handle table extraction across multiple pages
    table_data = []
    for page in text_pages:
        try:
            # Find table rows using a regex or a pattern for row data
            rows = re.findall(r'([a-zA-Z\s]+)\|\s*(\d+)\s*\|\s*([0-9,\.]+ €)\s*\|\s*([0-9,\.]+ €)', page)
            for row in rows:
                table_data.append({
                    "Description": row[0].strip(),
                    "Quantity": row[1].strip(),
                    "Unit Price": row[2].strip(),
                    "Total": row[3].strip()
                })
        except Exception as e:
            print(f"Error while extracting table data on this page: {str(e)}")

    # Handle multi-line rows (merge rows when needed)
    processed_table_data = []
    i = 0
    while i < len(table_data):
        if "Continued" in table_data[i]["Description"]:
            if i + 1 < len(table_data):
                # Merge with the next row if available
                merged_row = {
                    "Description": table_data[i]["Description"].replace("Continued", "").strip() + " " + table_data[i + 1]["Description"].strip(),
                    "Quantity": table_data[i + 1]["Quantity"],
                    "Unit Price": table_data[i + 1]["Unit Price"],
                    "Total": table_data[i + 1]["Total"]
                }
                processed_table_data.append(merged_row)
                # Skip the next row since it's merged
                i += 2
            else:
                # If no next row to merge, log the issue and skip
                print(f"Warning: Last row marked 'Continued' but no row to merge with.")
                i += 1
        else:
            # Normal row, append as-is
            processed_table_data.append(table_data[i])
            i += 1

    extracted_data['Table'] = processed_table_data
    return extracted_data

# Advanced error handling for missing data
def extract_with_error_handling(text, field_name, regex_pattern):
    try:
        return re.search(regex_pattern, text).group(1)
    except AttributeError:
        print(f"Error: {field_name} not found, returning fallback value 'N/A'")
        return "N/A"

# Process a complex invoice (multi-page, multi-line)
pdf_text = extract_text_from_pdf("sample-invoice.pdf")
extracted_invoice_data = process_multi_page_invoice(pdf_text)

# Print the extracted data in JSON format
print(json.dumps(extracted_invoice_data, indent=4))

# Example of error handling for field extraction
invoice_text = "Sample Invoice\nDate: Missing"
invoice_date = extract_with_error_handling(invoice_text, "Invoice Date", r"Date:\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4})")
print(f"Extracted Invoice Date: {invoice_date}")
