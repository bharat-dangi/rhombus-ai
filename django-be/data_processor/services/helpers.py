import pandas as pd

def format_inferred_types(data_frame: pd.DataFrame) -> dict:
    """
    Formats the inferred data types of each column in a DataFrame.
    
    Parameters:
    - data_frame (pd.DataFrame): DataFrame with columns whose types are to be inferred
    
    Returns:
    - dict: Dictionary where keys are column names and values are data types as strings
    """
    return data_frame.dtypes.apply(lambda x: str(x)).to_dict()

def convert_data_to_json_compatible(data):
    """
    Converts DataFrame data to JSON-compatible format by handling NaNs.
    
    Parameters:
    - data (list of dict): List of records (dicts) where each record represents a row
    
    Returns:
    - list of dict: JSON-compatible list of records with NaNs replaced by None
    """
    return [{k: (None if pd.isna(v) else v) for k, v in record.items()} for record in data]
