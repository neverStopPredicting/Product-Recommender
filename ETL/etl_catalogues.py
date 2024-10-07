import pdfplumber
import json
from typing import List, Dict


def extract_products_from_pdf(pdf_file_path: str, json_file_path: str) -> None:
    """
    Extract text from a PDF file and save it as JSON.

    This function reads a PDF file, extracts text from each page,
    and saves the extracted data as a JSON file. Each page's data
    is stored as a dictionary within a list.

    Args:
        pdf_file_path (str): Path to the input PDF file.
        json_file_path (str): Path where the output JSON file will be saved.

    Raises:
        Exception: If any error occurs during the extraction or saving process.

    Returns:
        None
    """
    try:
        pdf_data: List[Dict[str, str]] = []
        with pdfplumber.open(pdf_file_path) as pdf:
            # Extract text from each page
            for page_number, page in enumerate(pdf.pages):
                text = page.extract_text()
                # Create a dictionary for each page
                page_data = {
                    'original_file': pdf_file_path,
                    'page_number': page_number + 1,
                    'page_text': text.replace('\n', ' ') if text else ''
                }
                pdf_data.append(page_data)

        with open(json_file_path, 'w') as json_file:
            json.dump(pdf_data, json_file, indent=4)
        
        print(f'Text extracted and saved to {json_file_path}')
    except Exception as e:
        print(f'An error occurred: {e}')
        raise


if __name__ == "__main__":
    PDF_FILE_PATH = '../data/catalogue_data/PremierQualityFoodsBrochure2021.pdf'
    JSON_FILE_PATH = '../data/catalogue_data/catalogue.json'
    extract_products_from_pdf(PDF_FILE_PATH, JSON_FILE_PATH)