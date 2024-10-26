import React from "react";
import PropTypes from "prop-types";

// Handles file selection and upload actions
const FileInput = ({ onFileChange, onUpload, loading }) => {
  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 mb-6">
      <input
        type="file"
        accept=".csv, .xls, .xlsx"
        onChange={onFileChange} // Triggers when file is selected
        className="border border-gray-300 rounded-lg p-3 w-full sm:w-auto shadow"
      />
      <button
        onClick={onUpload} // Triggers file upload
        disabled={loading} // Disables button while uploading
        className="bg-blue-500 text-white px-6 py-2 rounded-lg shadow-md hover:bg-blue-600 transition w-full sm:w-auto"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

FileInput.propTypes = {
  onFileChange: PropTypes.func.isRequired,
  onUpload: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
};

export default FileInput;
