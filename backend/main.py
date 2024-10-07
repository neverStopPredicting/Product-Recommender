from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
import google.generativeai as genai
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify frontend URL here for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google's Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

SOLR_URL = os.getenv("SOLR_URL")

def get_venue_meta(query: str) -> Dict[str, Any]:
    """
    Retrieve venue metadata from Solr based on the given query.

    Args:
        query (str): The venue name to search for.

    Returns:
        Dict[str, Any]: A dictionary containing the venue metadata.

    Raises:
        HTTPException: If there's an error querying Solr or no results are found.
    """
    query_url = SOLR_URL + "venue_menu/select"
    params = {
        'q': query,
        'rows': 1,
        'wt': 'json',
        'defType': 'edismax',
        'qf': 'venue_name_t',
        'mm': '1',
    }

    try:
        response = requests.get(query_url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data['response']['docs']:
            raise HTTPException(status_code=404, detail="Venue not found")
        return data['response']['docs'][0]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error querying Solr: {str(e)}")

def get_catalogues(query: str) -> List[Dict[str, Any]]:
    """
    Retrieve 3 catalogue data from Solr based on the given query.

    Args:
        query (str): The query string to search for in the catalogues.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the catalogue data.

    Raises:
        HTTPException: If there's an error querying Solr.
    """
    query_url = SOLR_URL + "catalogues/select"
    params = {
        'q': query,
        'rows': 3,
        'wt': 'json',
        'defType': 'edismax',
        'qf': 'page_text_txt',
        'mm': '1',
    }

    try:
        response = requests.get(query_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['response']['docs']
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error querying Solr: {str(e)}")

def extract_venue_meta(venue_meta: Dict[str, Any], related_catalogues: List[Dict[str, Any]]) -> str:
    """
    Generate product suggestions for a venue using Google's Generative AI.

    Args:
        venue_meta (Dict[str, Any]): The venue metadata.
        related_catalogues (List[Dict[str, Any]]): The related catalogue data.

    Returns:
        str: HTML-formatted product suggestions.

    Raises:
        HTTPException: If there's an error generating content.
    """
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    
    prompt = """
    Your task is to follow the instructions below and suggest suitable products from the catalogue for the venue.

    1. List 15 products from the catalogue.
    2. Based on the venue metadata provided to you, and the venue type and the ingredients listed on their menu, pick 5 products from the catalogue to make the suggestion.
    3. Your answer should be based on the template below; please do not add other information e.g. Venue.
    4. Your answer should be based on the Venue metadata and Product Catalogue; please do not create items or names from your own knowledge.
    5. The [original_file] should only show the file name, not the entire file path.
    6. Your response should be HTML, e.g. using <br /> for newline.

    --------- Response template ---------
    [venue_name] is a [venue_type] venue.
    My suggested products from the [original_file] are:
    1. [product name 1], [product 1 page_number]
    2. [product name 2], [product 2 page_number]
    3. [product name 3], [product 3 page_number]
    4. [product name 4], [product 4 page_number]
    5. [product name 5], [product 5 page_number]
    """
    
    try:
        result = model.generate_content(prompt + ' ' + f'Venue meta data: {venue_meta}, Product Catalogue: {related_catalogues}')
        return result.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@app.get("/{venue_name}")
async def get_venue_suggestions(venue_name: str) -> str:
    """
    Generate product suggestions for a given venue.

    Args:
        venue_name (str): The name of the venue to generate suggestions for.

    Returns:
        str: HTML-formatted product suggestions.

    Raises:
        HTTPException: If there's an error in any step of the process.
    """
    venue_meta = get_venue_meta(venue_name)
    query2 = ' '.join(venue_meta['ingredients_txt'])
    related_catalogues = get_catalogues(query2)
    response = extract_venue_meta(venue_meta, related_catalogues)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)