import pandas as pd
from datetime import datetime, timedelta

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
    Converts DataFrame data to JSON-compatible format by handling NaNs,
    Timestamp, Timedelta, and complex numbers.
    
    Parameters:
    - data (list of dict): List of records (dicts) where each record represents a row
    
    Returns:
    - list of dict: JSON-compatible list of records with NaNs replaced by None
    """
    def json_compatible(value):
        if pd.isna(value):
            return None
        elif isinstance(value, (pd.Timestamp, datetime)):
            return value.isoformat()
        elif isinstance(value, timedelta):
            return str(value)
        elif isinstance(value, complex):
            return str(value)  # Convert complex numbers to string
        else:
            return value
    
    return [{k: json_compatible(v) for k, v in record.items()} for record in data]
