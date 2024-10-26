import axios from "axios";

// Creates an Axios instance with base URL for backend requests
const API = axios.create({
  baseURL: process.env.REACT_APP_BE_URL,
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

export default API;
