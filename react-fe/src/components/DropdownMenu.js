import React from "react";
import PropTypes from "prop-types";

const DATA_TYPES = ["Text", "Float", "Integer", "Date", "TimeDelta", "Boolean", "Category", "Complex"];

const DropdownMenu = ({ column, currentType, onTypeChange, isOpen, onToggle }) => {
  const handleTypeSelect = (type) => {
    onTypeChange(column, type);
    onToggle(); // Close dropdown after selection
  };

  return (
    <div className="relative inline-block text-left">
      {/* Three-dot icon for dropdown */}
      <button onClick={onToggle} className="text-gray-500 focus:outline-none">
        &#x22EE; {/* Vertical three dots */}
      </button>

      {/* Dropdown menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-32 bg-white border border-gray-200 rounded-md shadow-lg z-10">
          {DATA_TYPES.map((type) => (
            <button
              key={type}
              onClick={() => handleTypeSelect(type)}
              className={`block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left ${
                type === currentType ? "bg-gray-200 font-semibold" : ""
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

DropdownMenu.propTypes = {
  column: PropTypes.string.isRequired,
  currentType: PropTypes.string.isRequired,
  onTypeChange: PropTypes.func.isRequired,
  isOpen: PropTypes.bool.isRequired,
  onToggle: PropTypes.func.isRequired,
};

export default DropdownMenu;
