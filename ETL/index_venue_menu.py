import os
import json
import pysolr

# Initialize Solr connection 
solr_url = 'http://localhost:8983/solr/venue_menu' 
solr = pysolr.Solr(solr_url, always_commit=True, timeout=10)

venue_menu_data_folder = '../data/venue_menu_data'

def index_venue_menu_data(folder):
    # Loop over all files in the directory
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            file_path = os.path.join(folder, filename)

            # Read and parse the JSON file
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)

                    # Build Solr documents, mapping fields to dynamic fields
                    solr_doc = {
                        'venue_name_t': data.get('venue_name', ''),
                        'venue_type_s': data.get('venue_type', ''),
                        'ingredients_txt': data.get('ingredients', ''),
                    }

                    solr.add([solr_doc])

                    print(f'Successfully indexed {filename}')

                except Exception as e:
                    print(f'Error indexing {filename}: {e}')

index_venue_menu_data(venue_menu_data_folder)