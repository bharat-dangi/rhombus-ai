import axios from "axios";

// Creates an Axios instance with base URL for backend requests
const API = axios.create({
  baseURL: process.env.REACT_APP_BE_URL, // Base URL defined in environment variables
});

// Uploads the selected file to the backend and returns processed data
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file); // Appends file to form data for upload

  try {
    const response = await API.post("upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response?.data; // Returns response data on successful upload
  } catch (error) {
    // Throws error with a descriptive message if upload fails
    throw new Error(error?.response?.data?.message || "File upload failed.");
  }
};

// Fetches previously saved data and schema from the backend
export const fetchData = async () => {
  try {
    const response = await API.get("data/");
    return response?.data; // Returns fetched data on successful response
  } catch (error) {
    // Throws error if data fetching fails
    throw new Error("Failed to fetch data from the backend.");
  }
};

// Sends updated column types to the backend for updating schema
export const updateColumnTypes = async (columnTypes) => {
  try {
    const response = await API.post("update_column_types/", {
      column_types: columnTypes,
    });
    return response?.data; // Returns response on successful type update
  } catch (error) {
    // Throws error if column type update fails
    throw new Error("Failed to update column types.");
  }
};

export default API;
