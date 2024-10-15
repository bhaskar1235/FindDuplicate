import os
import fitz  # PyMuPDF for PDF manipulation
import pytesseract
from PIL import Image

# Set the path to the Tesseract executable manually
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\bhaskarm\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Function to perform OCR on a PDF and save the new OCR PDF
def save_pdf_with_ocr(pdf_path, output_pdf_path):
    doc = fitz.open(pdf_path)  # Open the original PDF
    new_doc = fitz.open()  # Create a new blank PDF for OCR

    # Iterate through all pages and perform OCR
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()  # Get the image representation of the page

        # Create a new page in the output PDF with the same dimensions
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(new_page.rect, pixmap=pix)  # Insert the original image of the page

        # Convert the page to an image and apply OCR to extract text
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = pytesseract.image_to_string(img)
        print(ocr_text);

        # Add OCR text to the page as a selectable layer
        if ocr_text.strip():
            new_page.insert_text((10, 10), ocr_text, fontsize=12, color=(0, 0, 0), overlay=True)

    # Save the new PDF with OCR text
    new_doc.save(output_pdf_path)
    new_doc.close()
    doc.close()
    print(f"OCR PDF saved as: {output_pdf_path}")

# Main function to process the PDFs in a folder
def convert_pdf_folder_to_ocr(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {pdf_path}")

            # Save the OCR-converted PDF in the same folder
            ocr_output_path = os.path.join(folder_path, f"OCR_{file_name}")
            save_pdf_with_ocr(pdf_path, ocr_output_path)

# Path to the folder containing the PDFs
folder_path = r"C:\\Users\\bhaskarm\Desktop\\PDF manipulate"

# Run the script
convert_pdf_folder_to_ocr(folder_path)
