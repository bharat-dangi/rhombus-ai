import React from "react";
import UploadFile from "./components/UploadFile";

// Main application component
function App() {
  return (
    <div className="App">
      <header className="bg-blue-600 text-white text-3xl font-bold p-4 text-center shadow-md">
        Data Type Inference App
      </header>
      <main className="p-4">
        <UploadFile /> {/* Upload and display inferred data */}
      </main>
    </div>
  );
}

export default App;
