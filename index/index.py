import os
import re
import fitz  # PyMuPDF for PDF text extraction
from collections import Counter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    
    # Iterate over all pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    
    return text

# Function to parse questions and ignore the question paper ID
def parse_questions(text):
    # Remove the [Question Paper ID: ...] line
    text = re.sub(r'\[Question Paper ID:.*?\]', '', text, flags=re.DOTALL)
    
    # Find all questions that end with a question mark and are followed by answer choices
    questions = re.findall(r'([^\n]+?\?)\s*\(A\)', text, flags=re.DOTALL)

    # Clean up each question by removing leading/trailing whitespace
    questions = [q.strip() for q in questions]
    
    return questions

# Function to find duplicate questions
def find_duplicate_questions(questions):
    question_counter = Counter(questions)
    duplicates = {q: count for q, count in question_counter.items() if count > 1}
    return duplicates

# Function to create a new PDF with duplicate questions
def create_pdf_with_duplicates(duplicates, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    c.drawString(100, 750, "Duplicate Questions")
    
    # Starting position for questions
    y_position = 730
    
    for question, count in duplicates.items():
        c.drawString(100, y_position, f"Question: {question} - appears {count} times")
        y_position -= 20  # Move down for the next question
        if y_position < 50:  # Create a new page if we run out of space
            c.showPage()
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Duplicate Questions")
            y_position = 730
    
    c.save()

# Main function to process the PDFs in the folder and create a PDF of duplicates
def find_duplicates_in_pdf_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {pdf_path}")

            # Step 1: Extract text from the PDF
            text = extract_text_from_pdf(pdf_path)

            # Step 2: Parse questions, ignoring the question paper ID
            questions = parse_questions(text)

            # Step 3: Find duplicate questions
            duplicates = find_duplicate_questions(questions)

            # Step 4: Print only duplicate question text
            if duplicates:
                print("Duplicate questions found:")
                for question in duplicates:
                    print(f"Duplicate question: {question}")
            else:
                print("No duplicate questions found.")

            # Step 5: Create a new PDF with duplicate questions (if any)
            if duplicates:
                output_pdf_path = os.path.join(folder_path, f"duplicates_{file_name}")
                create_pdf_with_duplicates(duplicates, output_pdf_path)
                print(f"New PDF created with duplicates: {output_pdf_path}")

# Path to the folder containing the PDFs
folder_path = r"C:\Users\bhaskarm\Desktop\PDF manipulate"

# Run the script
find_duplicates_in_pdf_folder(folder_path)