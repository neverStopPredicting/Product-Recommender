import os
import json
import pysolr
from typing import Dict, Any

# Solr configuration
SOLR_URL = 'http://localhost:8983/solr/venue_menu'
SOLR = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)

# Data folder configuration
VENUE_MENU_DATA_FOLDER = '../data/venue_menu_data'

def index_venue_menu_data(folder: str) -> None:
    """
    Indexes all JSON files in the venue menu folder to Solr.

    Args:
        folder (str): The directory containing the JSON files to be indexed.

    Raises:
        FileNotFoundError: If the specified folder does not exist.
        json.JSONDecodeError: If a JSON file is not properly formatted.
        pysolr.SolrError: If there's an error communicating with Solr.

    Note:
        The JSON file is expected to contain an object with the following structure:
        - venue_name (str): The name of the venue
        - venue_type (str): The type of the venue
        - ingredients (list): A list of ingredients
    """
    if not os.path.exists(folder):
        raise FileNotFoundError(f"The folder {folder} does not exist.")

    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                
                solr_doc = create_solr_document(data)
                SOLR.add([solr_doc])
                print(f'Successfully indexed {filename}')
            except json.JSONDecodeError:
                print(f'Error decoding JSON in {filename}. Skipping this file.')
            except pysolr.SolrError as e:
                print(f'Error communicating with Solr while indexing {filename}: {e}')
            except Exception as e:
                print(f'Unexpected error indexing {filename}: {e}')

def create_solr_document(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a Solr document from venue menu data.

    Args:
        data (Dict[str, Any]): A dictionary containing venue menu data.

    Returns:
        Dict[str, Any]: A dictionary representing a Solr document.
    """
    return {
        'venue_name_t': data.get('venue_name', ''),
        'venue_type_s': data.get('venue_type', ''),
        'ingredients_txt': data.get('ingredients', []),
    }

if __name__ == "__main__":
    index_venue_menu_data(VENUE_MENU_DATA_FOLDER)