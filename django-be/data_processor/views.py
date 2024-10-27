from ninja import NinjaAPI, UploadedFile, File
from django.http import JsonResponse
from .services.data_inference import infer_and_convert_data_types
import pandas as pd
import os
import json
from datetime import datetime

# Set DATA_DIR to a directory within your project for persistent storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data_storage")
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize the NinjaAPI instance
api = NinjaAPI()

# Supported data types for conversions
TYPE_MAP = {
    "Text": "object",
    "Float": "float64",
    "Integer": "Int64",
    "Date": "datetime64[ns]",
    "TimeDelta": "timedelta64[ns]",
    "Boolean": "bool",
    "Category": "category",
    "Complex": "complex128"
}

@api.post("/upload/")
def upload_file(request, file: UploadedFile = File(...)):
    """
    API endpoint to upload a file, infer data types, and return inferred types and data.
    """
    file_path = save_uploaded_file(file)
    try:
        data_frame = infer_and_convert_data_types(file_path)
        save_data_to_disk(data_frame)
        
        inferred_types = format_inferred_types(data_frame)
        data = convert_data_to_json_compatible(data_frame.to_dict(orient="records"))
        
        return JsonResponse({
            "inferred_types": inferred_types,
            "data": data,
            "total_count": len(data)
        })
    finally:
        os.remove(file_path)

@api.post("/update_column_types/")
def update_column_types(request):
    """
    Endpoint to update column types based on user selection.
    Expects a JSON payload with a "column_types" dictionary.
    Example: {"Score": "Float"}
    """
    # Parse JSON data from request body
    try:
        body_data = json.loads(request.body)
        column_types = body_data.get("column_types", {})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data."}, status=400)
    
    # Load the data and schema from disk
    with open(os.path.join(DATA_DIR, "data.json"), "r") as data_file:
        data = json.load(data_file)
    data_frame = pd.DataFrame(data)
    
    # Apply the new types based on user input
    for column, new_type in column_types.items():
        if new_type in TYPE_MAP:
            data_frame[column] = data_frame[column].astype(TYPE_MAP[new_type])
    
    # Save the updated data and types back to disk
    save_data_to_disk(data_frame)
    
    # Return the updated schema
    updated_types = format_inferred_types(data_frame)
    return JsonResponse({"inferred_types": updated_types})

def save_uploaded_file(file: UploadedFile) -> str:
    """
    Saves the uploaded file to a temporary location and returns the file path.
    """
    file_path = f"/tmp/{file.name}"
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def format_inferred_types(data_frame: pd.DataFrame) -> dict:
    """
    Formats the inferred types of each column in the DataFrame for JSON compatibility.
    """
    return data_frame.dtypes.apply(lambda x: str(x)).to_dict()

def save_data_to_disk(data_frame: pd.DataFrame):
    """
    Saves the DataFrame and its schema to JSON files on disk.
    """
    data = convert_data_to_json_compatible(
        data_frame.applymap(lambda x: x.isoformat() if isinstance(x, (pd.Timestamp, datetime)) else x).to_dict(orient="records")
    )
    
    inferred_types = format_inferred_types(data_frame)
    
    with open(os.path.join(DATA_DIR, "data.json"), "w") as data_file:
        json.dump(data, data_file, indent=4)
    with open(os.path.join(DATA_DIR, "schema.json"), "w") as schema_file:
        json.dump(inferred_types, schema_file, indent=4)

@api.get("/data/")
def get_data(request):
    """
    Endpoint to retrieve the saved data and inferred schema.
    """
    try:
        with open(os.path.join(DATA_DIR, "data.json"), "r") as data_file:
            data = json.load(data_file)
        
        with open(os.path.join(DATA_DIR, "schema.json"), "r") as schema_file:
            inferred_types = json.load(schema_file)
        
        return JsonResponse({
            "inferred_types": inferred_types,
            "data": data,
            "total_count": len(data)
        })
    except FileNotFoundError:
        return JsonResponse({"error": "No data available"}, status=404)

def convert_data_to_json_compatible(data):
    """
    Converts NaN values to None for JSON serialization compatibility.
    """
    return [{k: (None if pd.isna(v) else v) for k, v in record.items()} for record in data]
