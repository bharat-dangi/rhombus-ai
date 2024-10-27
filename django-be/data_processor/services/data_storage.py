import os
import json
import pandas as pd
from datetime import datetime, timedelta
from .helpers import format_inferred_types, convert_data_to_json_compatible

# Define storage directory for persistent data storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data_storage")
os.makedirs(DATA_DIR, exist_ok=True)

def save_uploaded_file(file) -> str:
    """
    Temporarily saves an uploaded file to disk for processing.
    
    Parameters:
    - file (UploadedFile): File object from the request
    
    Returns:
    - str: Path to the saved file
    """
    file_path = f"/tmp/{file.name}"
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def save_data_to_disk(data_frame: pd.DataFrame):
    """
    Saves the data and inferred types of a DataFrame to disk as JSON files.
    
    Parameters:
    - data_frame (pd.DataFrame): DataFrame to save
    
    Files Saved:
    - data.json: Contains row data in JSON format
    - schema.json: Contains inferred column types in JSON format
    """
    data = convert_data_to_json_compatible(data_frame.to_dict(orient="records"))
    inferred_types = format_inferred_types(data_frame)
    
    with open(os.path.join(DATA_DIR, "data.json"), "w") as data_file:
        json.dump(data, data_file, indent=4)
    with open(os.path.join(DATA_DIR, "schema.json"), "w") as schema_file:
        json.dump(inferred_types, schema_file, indent=4)

def load_data_from_disk():
    """
    Loads saved data and inferred types from disk.
    
    Returns:
    - tuple: (data, inferred_types) where each is loaded from JSON if available
    """
    try:
        with open(os.path.join(DATA_DIR, "data.json"), "r") as data_file:
            data = json.load(data_file)
        
        with open(os.path.join(DATA_DIR, "schema.json"), "r") as schema_file:
            inferred_types = json.load(schema_file)
        
        return data, inferred_types
    except FileNotFoundError:
        return None, None
