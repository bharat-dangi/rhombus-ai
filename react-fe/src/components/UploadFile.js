import React, { useState, useEffect, useCallback } from "react";
import { uploadFile, fetchData, updateColumnTypes } from "../services/api";
import { mapDataType } from "../utils/dataTypeMapper";
import ErrorMessage from "./ErrorMessage";
import DataTable from "./DataTable";

const UploadFile = () => {
  const [file, setFile] = useState(null);
  const [inferredData, setInferredData] = useState(null);
  const [tableData, setTableData] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [uploadError, setUploadError] = useState(null);
  const [tableError, setTableError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [skip, setSkip] = useState(0); // Initialize skip for pagination
  const limit = 100; // Limit for each batch of data

  // Load initial data and subsequent data on scroll
  const loadData = useCallback(async () => {
    // Stop loading if already loading or if all data has been fetched
    if (loading || (skip >= totalCount && skip > 0)) return;

    setLoading(true);
    setTableError(null);

    try {
      const data = await fetchData(skip, limit); // Pass skip and limit to fetch data
      if (data?.data) {
        const mappedDataTypes = Object.fromEntries(
          Object.entries(data.inferred_types).map(([column, dtype]) => [
            column,
            mapDataType(dtype),
          ]),
        );
        setInferredData(mappedDataTypes);
        setTableData((prevData) => [...prevData, ...data.data]); // Append new data
        setTotalCount(data.total_count);
        setSkip(skip + limit); // Increment skip by limit for next fetch
      }
    } catch (err) {
      console.error("Error fetching data:", err);
      setTableError("Failed to load data.");
    } finally {
      setLoading(false);
    }
  }, [loading, skip, limit, totalCount]);

  useEffect(() => {
    loadData(); // Initial data load
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadError(null);
    setTableError(null);
    setInferredData(null);
    setTableData([]);
    setSkip(0); // Reset skip for new data load
  };

  const handleUpload = async () => {
    if (!file || loading) {
      setUploadError("Please select a file.");
      return;
    }

    setLoading(true);
    setUploadError(null);

    try {
      const data = await uploadFile(file);
      const mappedDataTypes = Object.fromEntries(
        Object.entries(data.inferred_types).map(([column, dtype]) => [
          column,
          mapDataType(dtype),
        ]),
      );
      setInferredData(mappedDataTypes);
      setTableData(data.data);
      setTotalCount(data.total_count);
      setSkip(data.data.length); // Set skip based on initial data length
    } catch (error) {
      setUploadError("Failed to upload file.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleTypeChange = async (column, newType) => {
    setTableError(null); // Clear previous data table error
    setInferredData((prev) => ({ ...prev, [column]: newType }));
    try {
      await updateColumnTypes({ [column]: newType });
    } catch (error) {
      console.error("Failed to update column type:", error);
      setTableError("Failed to update column type."); // Set error for data table
    }
  };

  const handleRemoveFile = () => {
    setFile(null);
    setInferredData(null);
    setTableData([]);
    setUploadError(null);
    setLoading(false);
    setSkip(0); // Reset skip
    document.getElementById("fileInput").value = null; // Clear file input
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 p-4">
      {/* Upload Section */}
      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-3xl mx-4 mb-6">
        <h2 className="text-2xl font-semibold text-center mb-6">
          Upload Your Data File
        </h2>
        {uploadError && <ErrorMessage message={uploadError} />}
        <div className="flex flex-col sm:flex-row items-center gap-4 mb-4">
          <input
            id="fileInput"
            type="file"
            accept=".csv, .xls, .xlsx"
            onChange={handleFileChange}
            className="border border-gray-300 rounded p-2 w-full sm:w-auto"
          />
          <button
            onClick={handleUpload}
            disabled={loading}
            className={`px-6 py-2 rounded-lg shadow-md w-full sm:w-auto ${
              loading ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"
            } text-white transition`}
          >
            {loading ? "Loading..." : "Upload"}
          </button>
          {file && (
            <button
              onClick={handleRemoveFile}
              disabled={loading}
              className="px-4 py-2 rounded-lg shadow-md bg-red-500 text-white hover:bg-red-600 transition w-full sm:w-auto"
            >
              Remove File
            </button>
          )}
        </div>
      </div>

      {/* Data Table Section */}
      {inferredData && (
        <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-4xl mx-4">
          <h3 className="text-xl font-semibold mb-4 text-center">
            Data Table (Total Records: {totalCount})
          </h3>
          <DataTable
            data={tableData}
            inferredData={inferredData}
            onLoadMore={loadData} // Pass loadData to DataTable for infinite scrolling
            loading={loading}
            onTypeChange={handleTypeChange}
          />
          {tableError && <ErrorMessage message={tableError} />}
          {loading && (
            <p className="text-center text-gray-500 mt-4">
              Loading more data...
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default UploadFile;
