from ninja import NinjaAPI, UploadedFile, File
from django.http import JsonResponse
from .services.data_inference import infer_and_convert_data_types
import os

# Initialize the NinjaAPI instance
api = NinjaAPI()

@api.post("/upload/")
def upload_file(request, file: UploadedFile = File(...)):
    """
    API endpoint to upload a CSV or Excel file, infer data types, and return the inferred types.

    Steps:
    - Save the uploaded file temporarily for processing.
    - Pass the file to the inference function to detect data types.
    - Clean up by deleting the temporary file.
    - Return inferred data types as a JSON response.
    """
    # Step 1: Temporarily save the uploaded file
    file_path = save_uploaded_file(file)
    
    # Step 2: Perform data type inference
    inferred_data = infer_and_convert_data_types(file_path)
    
    # Step 3: Convert data types to a JSON-serializable format
    inferred_data = format_inferred_data(inferred_data)
    
    # Step 4: Clean up the temporary file
    os.remove(file_path)
    
    return JsonResponse({"inferred_types": inferred_data})

def save_uploaded_file(file: UploadedFile) -> str:
    """
    Saves the uploaded file to a temporary location.

    Parameters:
    - file (UploadedFile): The uploaded file object from the request.

    Returns:
    - str: The file path where the file is saved.
    """
    file_path = f"/tmp/{file.name}"
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def format_inferred_data(data_frame) -> dict:
    """
    Converts the inferred data types of a DataFrame to a dictionary for JSON response.

    Parameters:
    - data_frame (pd.DataFrame): The DataFrame with inferred data types.

    Returns:
    - dict: A dictionary where keys are column names and values are inferred data types as strings.
    """
    return data_frame.dtypes.apply(lambda x: str(x)).to_dict()
