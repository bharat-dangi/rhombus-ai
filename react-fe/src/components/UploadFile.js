import React, { useState } from "react";
import { uploadFile } from "../services/api";
import { mapDataType } from "../utils/dataTypeMapper";
import InferredDataDisplay from "./InferredDataDisplay";
import ErrorMessage from "./ErrorMessage";

// Main component to handle file uploads and data type display
const UploadFile = () => {
  const [file, setFile] = useState(null); // Selected file
  const [inferredData, setInferredData] = useState(null); // Inferred data types
  const [error, setError] = useState(null); // Error message
  const [loading, setLoading] = useState(false); // Loading state

  // Updates selected file state
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
    setInferredData(null);
  };

  // Uploads file and processes data type inference
  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file."); // Shows error if no file selected
      return;
    }

    setLoading(true); // Activates loading state
    setError(null);

    try {
      const data = await uploadFile(file); // Sends file to backend
      const mappedData = Object.fromEntries(
        Object.entries(data.inferred_types).map(([column, dtype]) => [
          column,
          mapDataType(dtype), // Maps backend types to user-friendly names
        ]),
      );
      setInferredData(mappedData); // Updates state with inferred data types
    } catch (error) {
      setError(error.message); // Displays error message on failure
    } finally {
      setLoading(false); // Ends loading state
    }
  };

  // Clears the selected file and resets the state
  const handleRemoveFile = () => {
    setFile(null); // Reset file state
    setInferredData(null); // Clear inferred data
    setError(null); // Clear any error messages
    setLoading(false); // Ensure loading is set to false
    document.getElementById("fileInput").value = null; // Reset file input
  };

  // Updates data type for a specific column
  const handleDataTypeChange = (column, newType) => {
    setInferredData((prev) => ({
      ...prev,
      [column]: newType,
    }));
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100">
      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-3xl mx-4">
        {error && <ErrorMessage message={error} />}{" "}
        {/* Shows error if present */}
        <div className="flex flex-col sm:flex-row items-center gap-4 mb-6">
          <input
            id="fileInput"
            type="file"
            accept=".csv, .xls, .xlsx"
            onChange={handleFileChange}
            className="border border-gray-300 rounded p-2 w-full sm:w-auto"
          />
          <button
            onClick={handleUpload}
            disabled={loading} // Only disable during loading
            className={`px-6 py-2 rounded-lg shadow-md w-full sm:w-auto ${
              loading ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"
            } text-white transition`}
          >
            {loading ? "Uploading..." : "Upload"}
          </button>
          {file && (
            <button
              onClick={handleRemoveFile}
              disabled={loading} // Disables the remove button while loading
              className="px-4 py-2 rounded-lg shadow-md bg-red-500 text-white hover:bg-red-600 transition w-full sm:w-auto"
            >
              Remove File
            </button>
          )}
        </div>
        {inferredData && (
          <InferredDataDisplay
            inferredData={inferredData}
            onDataTypeChange={handleDataTypeChange}
          />
        )}
      </div>
    </div>
  );
};

export default UploadFile;
