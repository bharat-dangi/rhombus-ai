// src/services/api.js
import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_BE_URL,
});

// Uploads the selected file to the backend and returns processed data
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await API.post("/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response?.data;
  } catch (error) {
    throw new Error(error?.response?.data?.message || "File upload failed.");
  }
};

// Fetches paginated data from the backend using skip and limit
export const fetchData = async (skip = 0, limit = 100) => {
  try {
    const response = await API.get(`/data?skip=${skip}&limit=${limit}`);
    return response?.data;
  } catch (error) {
    throw new Error(error?.response?.data?.message || "Failed to fetch data.");
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
