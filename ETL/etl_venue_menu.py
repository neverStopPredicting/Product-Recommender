import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("API_KEY"))

def extract_venue_meta(text):
    model = genai.GenerativeModel("gemini-1.5-pro-latest",
                                generation_config={"response_mime_type": "application/json"})
        
    prompt = """ Extract the meta data (venue_name and ingredients) from the above provided Text, return in JSON format.
    Notes: 
    1. The ingredients should be small ingredients that usually available in the Australian brochure stores, do not list dish names here.
    2. Venue type should be either restaurant or deli. 
    Use this JSON schema:
    Meta = {'venue_name': str, 'venue_type': str, 'ingredients': list[str]}
    Return: list[Meta]
    """
    result = model.generate_content(text+prompt)
    return json.loads(result.text)


if __name__ == "__main__":

    raw_folder_path = '../data/venue_raw_data'
    menu_folder_path = '../data/venue_menu_data'

    for filename in os.listdir(raw_folder_path):
        # Check if the file is a .txt file
        if filename.endswith(".txt"):
            file_path = os.path.join(raw_folder_path, filename)
            
            # Open and read the content of the file
            with open(file_path, 'r') as file:
                file_content = file.read()
            
            # Extract venue meta
            venue_menu_json = extract_venue_meta(file_content)
            json_filename = filename.replace('.txt', '.json')
            json_file_path = os.path.join(menu_folder_path, json_filename)
            
            # Save the content as a JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(venue_menu_json, json_file, indent=4)
            print('Processed: ', filename)