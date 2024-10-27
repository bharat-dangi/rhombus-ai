# Dictionary mapping user-friendly data type names to pandas-compatible types
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
