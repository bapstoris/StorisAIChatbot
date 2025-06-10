'''import fitz

def extract_text_from_pdf(pdf_file_path):
    try:
        doc = fitz.open(pdf_file_path)
        pdf_text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pdf_text += page.get_text("text")
        doc.close()
        return pdf_text
    except Exception as e:
        return f"Error extracting text: {e}"
    
pdf_path = "PDFs/Laptop Setup.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

file = open("LaptopSetup_pdf_text", "w", encoding='utf-8')
file.write(extracted_text) '''

import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_file_path):
    try:
        doc = fitz.open(pdf_file_path)
        pdf_text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pdf_text += page.get_text("text")
        doc.close()
        return pdf_text
    except Exception as e:
        return f"Error extracting text from {pdf_file_path}: {e}"

# Directory containing PDFs
pdf_dir = "PDFs"
output_file = "MainFiles/combined_pdf_text.txt"

all_text = ""

# Loop through all PDF files in the folder
for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        print(f"Extracting from {filename}...")
        text = extract_text_from_pdf(pdf_path)
        all_text += f"\n\n--- Start of {filename} ---\n\n{text}\n\n--- End of {filename} ---\n"

# Write combined text to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"Extraction complete. Combined text saved to {output_file}")