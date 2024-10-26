// Maps backend-inferred data types to user-friendly names for display in the frontend.
export const mapDataType = (dType) => {
  switch (dType) {
    case "object":
      return "Text";
    case "float32":
    case "float64":
      return "Float";
    case "int8":
    case "int16":
    case "int32":
    case "int64":
      return "Integer";
    case "datetime64[ns]":
      return "Date";
    case ("timedelta[ns]", "timedelta64[ns]"):
      return "TimeDelta";
    case "bool":
      return "Boolean";
    case "category":
      return "Category";
    case "complex128":
      return "Complex";
    default:
      return "Text"; // Default for unknown types
  }
};
