import pysolr
import os
import json

solr_url = 'http://localhost:8983/solr/catalogues'
solr = pysolr.Solr(solr_url, always_commit=True, timeout=10)

def index_catalogue_data(folder):
    """
    Indexes all JSON files in the catalogue folder to Solr.

    Parameters:
    folder (str): The directory containing the JSON files to be indexed.

    The JSON file contains:
    - original_file: The name of the original file
    - page_number: The page number
    - page_text: The text content of the page
    """
    
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            file_path = os.path.join(folder, filename)

            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    for page_data in data:
                        # Build Solr documents, mapping fields to dynamic fields
                        solr_doc = {
                            'original_file_s': page_data.get('original_file', ''),
                            'page_number_i': page_data.get('page_number', ''),
                            'page_text_txt': page_data.get('page_text', ''),
                        }

                        # Send document to Solr for indexing
                        solr.add([solr_doc])

                    print(f'Successfully indexed {filename}')

                except Exception as e:
                    print(f'Error indexing {filename}: {e}')


if __name__ == "__main__":
    catalogue_data_folder = '../data/catalogue_data'
    index_catalogue_data(catalogue_data_folder)