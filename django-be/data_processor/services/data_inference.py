import pandas as pd
import numpy as np
from typing import Union, IO
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

def infer_and_convert_data_types(file: Union[str, IO], chunk_size=500_000) -> pd.DataFrame:
    """
    Infers and converts data types in a large dataset by processing it in chunks.
    It uses parallel processing to analyze data types for each chunk, then consolidates the results
    to apply final data type conversions.

    Parameters:
    - file (str or IO): Path to the file or an in-memory file object.
    - chunk_size (int): Number of rows per chunk for processing large files.

    Returns:
    - pd.DataFrame: A DataFrame with inferred and converted data types.
    """
    df = load_file(file, chunk_size)
    print("Data types before inference:")
    print(df.dtypes)

    # Process each chunk and gather type counts for each column
    chunks = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]
    type_counts = defaultdict(lambda: defaultdict(int))
    processed_chunks = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(analyze_chunk_types, chunk) for chunk in chunks]
        for future in as_completed(futures):
            chunk_type_info, processed_chunk = future.result()
            processed_chunks.append(processed_chunk)
            update_type_counts(type_counts, chunk_type_info)

    final_types = determine_final_types(type_counts)

    # Concatenate processed chunks and convert columns based on final types
    result_df = pd.concat(processed_chunks, ignore_index=True)
    for col, dtype in final_types.items():
        result_df[col] = safely_convert_column(result_df[col], dtype)

    print("\nData types after inference:")
    print(result_df.dtypes)
    return result_df

def load_file(file: Union[str, IO], chunk_size: int) -> pd.DataFrame:
    """
    Loads a CSV or Excel file in chunks and concatenates them into a single DataFrame.

    Parameters:
    - file (str or IO): Path to the file or an in-memory file object.
    - chunk_size (int): Number of rows per chunk.

    Returns:
    - pd.DataFrame: Loaded DataFrame.
    """
    if isinstance(file, str):
        if file.endswith('.csv'):
            return pd.concat(pd.read_csv(file, chunksize=chunk_size), ignore_index=True)
        else:
            return pd.read_excel(file)
    try:
        return pd.concat(pd.read_csv(file, chunksize=chunk_size), ignore_index=True)
    except Exception:
        return pd.read_excel(file)

def analyze_chunk_types(chunk: pd.DataFrame) -> tuple:
    """
    Analyzes the data types of each column in a chunk.

    Parameters:
    - chunk (pd.DataFrame): A chunk of the DataFrame to analyze.

    Returns:
    - tuple: A dictionary with inferred data types for each column and the processed chunk.
    """
    chunk_types = {}
    processed_chunk = chunk.copy()

    for col in chunk.columns:
        col_data = chunk[col].dropna()
        inferred_type = infer_column_type(col_data)
        chunk_types[col] = inferred_type

    return chunk_types, processed_chunk

def infer_column_type(col_data: pd.Series) -> str:
    """
    Infers the most likely data type of a column based on its values.

    Parameters:
    - col_data (pd.Series): Column data.

    Returns:
    - str: Inferred data type for the column.
    """
    if is_numeric_column(col_data):
        return "float" if col_data.hasnans else "Int64"
    if is_datetime_column(col_data):
        return "datetime64[ns]"
    if is_timedelta_column(col_data):
        return "timedelta64[ns]"
    if is_boolean_column(col_data):
        return "bool"
    if is_complex_column(col_data):
        return "complex"
    if is_categorical_column(col_data):
        return "category"
    return "object"

def safely_convert_column(column: pd.Series, dtype: str) -> pd.Series:
    """
    Safely converts a column to the desired dtype, handling non-compatible values gracefully.

    Parameters:
    - column (pd.Series): Column to convert.
    - dtype (str): Target data type.

    Returns:
    - pd.Series: Converted column.
    """
    if dtype == "Int64":
        numeric_column = pd.to_numeric(column, errors='coerce')
        if numeric_column.dropna().apply(lambda x: isinstance(x, (int, np.integer)) or (isinstance(x, float) and x.is_integer())).all():
            return numeric_column.astype("Int64")
        return numeric_column  # Keep as float if non-integers are present
    elif dtype == "float":
        return pd.to_numeric(column, errors='coerce')
    else:
        return column.astype(dtype)

def update_type_counts(type_counts, chunk_type_info):
    """
    Updates the type counts for each column based on inferred types from each chunk.

    Parameters:
    - type_counts (defaultdict): Accumulated type counts for each column.
    - chunk_type_info (dict): Inferred types for the current chunk.
    """
    for col, inferred_type in chunk_type_info.items():
        type_counts[col][inferred_type] += 1

def determine_final_types(type_counts):
    """
    Determines the final data type for each column based on accumulated type counts.

    Parameters:
    - type_counts (defaultdict): Accumulated type counts for each column.

    Returns:
    - dict: Final inferred types for each column.
    """
    final_types = {}
    for col, type_dict in type_counts.items():
        final_types[col] = max(type_dict, key=type_dict.get)
    return final_types

# Helper functions for type inference
def is_numeric_column(series: pd.Series) -> bool:
    return not pd.to_numeric(series, errors='coerce').isna().all()

def is_datetime_column(series: pd.Series) -> bool:
    """
    Determines if a series can be classified as a datetime type.

    Parameters:
    - series (pd.Series): The data series to check.

    Returns:
    - bool: True if the series can be converted to datetime, False otherwise.
    """
    # First, attempt to convert with inferred format
    try:
        pd.to_datetime(series, infer_datetime_format=True, errors='raise')
        return True
    except (ValueError, TypeError):
        pass  # Continue to specific formats if general inference fails

    # Try specific date formats for finer control
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y%m%d", "%d %b %Y", "%d %B %Y"):
        try:
            pd.to_datetime(series, format=fmt, errors='raise')
            return True
        except (ValueError, TypeError):
            continue

    return False

def is_timedelta_column(series: pd.Series) -> bool:
    return not pd.to_timedelta(series, errors='coerce').isna().all()

def is_boolean_column(series: pd.Series) -> bool:
    unique_vals = series.dropna().unique()
    return set(unique_vals).issubset({0, 1, '0', '1', True, False, 'True', 'False', 'true', 'false'})

def is_categorical_column(series: pd.Series) -> bool:
    unique_ratio = series.nunique() / len(series)
    return unique_ratio < 0.1

def is_complex_column(series: pd.Series) -> bool:
    try:
        series.apply(lambda x: complex(x) if isinstance(x, str) else x).astype('complex')
        return True
    except ValueError:
        return False
