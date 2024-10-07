import os
import json
from typing import List, Dict, Union
import google.generativeai as genai
from tqdm import tqdm
import time

# Configure the API key for using gemini models
genai.configure(api_key=os.getenv("API_KEY"))

def extract_venue_meta(text: str) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Extract venue metadata from the provided text using Google's Generative AI.

    Args:
        text (str): The input text containing venue information.

    Returns:
        List[Dict[str, Union[str, List[str]]]]: A list of dictionaries containing
        extracted metadata for each venue.

    Raises:
        Exception: If there's an error in generating or parsing the AI response.
    """
    model = genai.GenerativeModel("gemini-1.5-pro-latest",
                                  generation_config={"response_mime_type": "application/json"})
    
    prompt = """
        Extract the meta data (venue_name and ingredients) from the above provided Text, return in JSON format.
        Notes:
        1. The ingredients should be small ingredients that are usually available in Australian grocery stores, do not list dish names here.
        2. Venue type should be either restaurant or deli.
        Use this JSON schema:
        Meta = {'venue_name': str, 'venue_type': str, 'ingredients': list[str]}
        Return: list[Meta]
        """
    
    try:
        result = model.generate_content(text + prompt)
        return json.loads(result.text)
    except Exception as e:
        print(f"Error in extracting venue metadata: {e}")
        raise

def process_files(raw_folder_path: str, menu_folder_path: str) -> None:
    """
    Process text files in the raw folder, extract venue metadata, and save as JSON.

    Args:
        raw_folder_path (str): Path to the folder containing raw text files.
        menu_folder_path (str): Path to the folder where JSON files will be saved.

    Returns:
        None
    """
    for filename in tqdm(os.listdir(raw_folder_path)):
        if filename.endswith(".txt"):
            file_path = os.path.join(raw_folder_path, filename)
            json_filename = filename.replace('.txt', '.json')
            json_file_path = os.path.join(menu_folder_path, json_filename)

            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()

                venue_menu_json = extract_venue_meta(file_content)

                time.sleep(45)

                with open(json_file_path, 'w') as json_file:
                    json.dump(venue_menu_json, json_file, indent=4)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    RAW_FOLDER_PATH = '../data/venue_raw_data'
    MENU_FOLDER_PATH = '../data/venue_menu_data'
    process_files(RAW_FOLDER_PATH, MENU_FOLDER_PATH)