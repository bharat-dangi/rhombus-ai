from ninja import Router, UploadedFile, File
from django.http import JsonResponse
from ..services.data_inference import infer_and_convert_data_types
from ..services.data_storage import save_data_to_disk, load_data_from_disk, save_uploaded_file
from ..services.helpers import format_inferred_types, convert_data_to_json_compatible
from .types import TYPE_MAP
import pandas as pd
import json
import os

# Initialize Router instance for API endpoints
router = Router()

@router.post("/upload/")
def upload_file(request, file: UploadedFile = File(...)):
    """
    Endpoint to handle file uploads, infer data types, and save to disk.
    
    Parameters:
    - file (UploadedFile): CSV or Excel file to upload and process
    
    Returns:
    - JsonResponse: Contains inferred data types, initial data, total count, and next skip index
    """
    file_path = save_uploaded_file(file)
    try:
        data_frame = infer_and_convert_data_types(file_path)
        save_data_to_disk(data_frame)
        
        inferred_types = format_inferred_types(data_frame)
        data = convert_data_to_json_compatible(data_frame.to_dict(orient="records"))
        
        return JsonResponse({
            "inferred_types": inferred_types,
            "data": data[:100],  # Return first 100 rows initially
            "total_count": len(data),
            "next_skip": 100
        })
    finally:
        os.remove(file_path)  # Clean up the temporary file

@router.get("/data")
def get_data(request, skip: int = 0, limit: int = 100):
    """
    Endpoint to fetch a paginated subset of data and inferred schema.
    
    Parameters:
    - skip (int): Number of records to skip for pagination
    - limit (int): Maximum number of records to return
    
    Returns:
    - JsonResponse: Contains paginated data, inferred types, total count, and next skip index
    """
    data, inferred_types = load_data_from_disk()
    if data is None or inferred_types is None:
        return JsonResponse({"error": "No data available"}, status=404)

    paginated_data = data[skip:skip + limit]
    next_skip = skip + limit if skip + limit < len(data) else None

    return JsonResponse({
        "inferred_types": inferred_types,
        "data": paginated_data,
        "total_count": len(data),
        "next_skip": next_skip
    })

@router.post("/update_column_types/")
def update_column_types(request):
    """
    Endpoint to update data types for specified columns based on user input.
    
    Request Body:
    - JSON containing a "column_types" dictionary, e.g., {"Score": "Float"}
    
    Returns:
    - JsonResponse: Contains updated inferred types after type conversions
    """
    try:
        body_data = json.loads(request.body)
        column_types = body_data.get("column_types", {})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data."}, status=400)

    data, inferred_types = load_data_from_disk()
    if data is None or inferred_types is None:
        return JsonResponse({"error": "No data available"}, status=404)

    data_frame = pd.DataFrame(data)

    # Apply specified column types
    for column, new_type in column_types.items():
        if new_type in TYPE_MAP:
            try:
                data_frame[column] = data_frame[column].astype(TYPE_MAP[new_type])
            except Exception as e:
                return JsonResponse({"error": f"Failed to convert {column} to {new_type}: {str(e)}"}, status=400)

    # Save updated data and types
    save_data_to_disk(data_frame)
    updated_types = format_inferred_types(data_frame)
    return JsonResponse({"inferred_types": updated_types})
