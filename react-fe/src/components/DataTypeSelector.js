import React from "react";
import PropTypes from "prop-types";

// Data types available for selection
const DATA_TYPES = [
  "Text",
  "Float",
  "Integer",
  "Date",
  "TimeDelta",
  "Boolean",
  "Category",
  "Complex",
];

const DataTypeSelector = ({ column, currentType, onChange }) => (
  <div className="flex items-center mb-4">
    <span className="mr-2 font-medium">{column}:</span>
    <select
      value={currentType}
      onChange={(e) => onChange(column, e.target.value)}
      className="border border-gray-300 rounded-lg p-2 bg-white"
    >
      {DATA_TYPES.map((type) => (
        <option key={type} value={type}>
          {type}
        </option>
      ))}
    </select>
  </div>
);

DataTypeSelector.propTypes = {
  column: PropTypes.string.isRequired,
  currentType: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
};

export default DataTypeSelector;
