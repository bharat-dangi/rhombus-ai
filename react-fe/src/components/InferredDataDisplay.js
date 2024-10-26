import React from "react";
import PropTypes from "prop-types";

// Renders a list of inferred data types with dropdowns for type selection
const InferredDataDisplay = ({ inferredData, onDataTypeChange }) => {
  return (
    <div className="mt-8">
      <h3 className="text-xl font-semibold mb-4 text-gray-700">
        Inferred Data Types:
      </h3>
      <ul className="bg-gray-50 p-4 rounded-lg shadow-inner space-y-3">
        {Object.entries(inferredData).map(([column, dType]) => (
          <li key={column} className="flex justify-between items-center">
            <span className="font-medium text-gray-700">{column}:</span>
            <select
              value={dType}
              onChange={(e) => onDataTypeChange(column, e.target.value)} // Handles type change
              className="ml-2 border border-gray-300 rounded-lg p-2 bg-white"
            >
              <option value="Text">Text</option>
              <option value="Integer">Integer</option>
              <option value="Float">Float</option>
              <option value="Date">Date</option>
              <option value="TimeDelta">Time Delta</option>
              <option value="Boolean">Boolean</option>
              <option value="Category">Category</option>
              <option value="Complex">Complex</option>
            </select>
          </li>
        ))}
      </ul>
    </div>
  );
};

InferredDataDisplay.propTypes = {
  inferredData: PropTypes.object.isRequired,
  onDataTypeChange: PropTypes.func.isRequired,
};

export default InferredDataDisplay;
