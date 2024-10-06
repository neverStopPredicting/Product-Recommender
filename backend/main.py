from fastapi import FastAPI
import requests
import google.generativeai as genai
import os

app = FastAPI()
genai.configure(api_key=os.getenv("API_KEY"))
                
def get_venue_meta(query):
    # Construct the Solr query URL
    query_url = "http://localhost:8983/solr/venue_menu/select"

    # Set up the parameters for the query
    params = {
        'q': query,                 # The query string
        'rows': 1,                  # Limit the number of rows returned to 1
        'wt': 'json',
        'defType': 'edismax',         # Use the edismax query parser
        'qf': 'venue_name_t',        # Specify the field(s) to search
        'mm': '1',               # Specify the response format
    }

    try:
        # Send the GET request to Solr
        response = requests.get(query_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        return data['response']['docs'][0]

    except requests.exceptions.RequestException as e:
        print(f"Error querying Solr: {e}")
        return None

def get_catalogues(query):
    # Construct the Solr query URL
    query_url = "http://localhost:8983/solr/catalogues/select"

    # Set up the parameters for the query
    params = {
        'q': query,                 # The query string
        'rows': 3,                  # Limit the number of rows returned to 1
        'wt': 'json',
        'defType': 'edismax',         # Use the edismax query parser
        'qf': 'page_text_txt',        # Specify the field(s) to search
        'mm': '1',                             # Specify the response format
    }

    try:
        # Send the GET request to Solr
        response = requests.get(query_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        return data['response']['docs']

    except requests.exceptions.RequestException as e:
        print(f"Error querying Solr: {e}")
        return None

def extract_venue_meta(venue_meta, related_catalogues):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
                    
        
    prompt = """ Your task is to follow the instructions below and suggest suitable products from the catalogue for the venue.

    1. List 15 products from the catalogue.
    2. Based on the venue metadata provided to you, and the venue type and the ingredients listed on their menu, pick 5 products from the catalogue to make the suggestion.
    3. Your answer should be based on the template below; please do not add other information e.g. Venue.
    4. Your answer should be based on the Venue metadata and Product Catalogue; please do not create items or names from your own knowledge.
    5. The [original_file] should only show the file name, not the entire file path.

    --------- Response template ---------
    [venue_name] is a [venue_type] venue.
    My suggested products from the [original_file] are:
    1. [product name 1], [product 1 page_number]
    2. [product name 2], [product 2 page_number]
    3. [product name 3], [product 3 page_number]
    4. [product name 4], [product 4 page_number]
    5. [product name 5], [product 5 page_number]
    """
    result = model.generate_content(prompt + ' ' + f'Venue meta data: {venue_meta}, Product Catalogue: {related_catalogues}')
    return result.text

# Define a simple route
@app.get("/{venue_name}")
def read_root(venue_name: str):                        # Example query to get all documents

    venue_meta = get_venue_meta(venue_name)
    query2 = ' '.join(venue_meta['ingredients_txt'])
    related_catalogues = get_catalogues(query2) 
    response = extract_venue_meta(venue_meta, related_catalogues)

    return response