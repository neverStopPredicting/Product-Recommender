import pysolr
import os
import json
from typing import Dict, Any

# Solr configuration
SOLR_URL = 'http://localhost:8983/solr/catalogues'
SOLR = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)

def index_catalogue_data(folder: str) -> None:
    """
    Indexes all JSON files in the catalogue folder to Solr.

    Args:
        folder (str): The directory containing the JSON files to be indexed.

    Raises:
        FileNotFoundError: If the specified folder does not exist.
        json.JSONDecodeError: If a JSON file is not properly formatted.
        pysolr.SolrError: If there's an error communicating with Solr.

    Note:
        The JSON file is expected to contain an array of objects with the following structure:
        - original_file (str): The name of the original file
        - page_number (int): The page number
        - page_text (str): The text content of the page
    """
    if not os.path.exists(folder):
        raise FileNotFoundError(f"The folder {folder} does not exist.")

    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                
                solr_docs = []
                for page_data in data:
                    solr_doc = create_solr_document(page_data)
                    solr_docs.append(solr_doc)
                
                # Send documents to Solr for indexing
                SOLR.add(solr_docs)
                print(f'Successfully indexed {filename}')
            except json.JSONDecodeError:
                print(f'Error decoding JSON in {filename}. Skipping this file.')
            except pysolr.SolrError as e:
                print(f'Error communicating with Solr while indexing {filename}: {e}')
            except Exception as e:
                print(f'Unexpected error indexing {filename}: {e}')

def create_solr_document(page_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a Solr document from page data.

    Args:
        page_data (Dict[str, Any]): A dictionary containing page data.

    Returns:
        Dict[str, Any]: A dictionary representing a Solr document.
    """
    return {
        'original_file_s': page_data.get('original_file', ''),
        'page_number_i': page_data.get('page_number', 0),
        'page_text_txt': page_data.get('page_text', ''),
    }

if __name__ == "__main__":
    CATALOGUE_DATA_FOLDER = '../data/catalogue_data'
    index_catalogue_data(CATALOGUE_DATA_FOLDER)