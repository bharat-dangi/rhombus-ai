import React from "react";
import PropTypes from "prop-types";
import DropdownMenu from "./DropdownMenu";

const DataTable = ({ data, inferredData, onTypeChange }) => {
  if (!data || data.length === 0) {
    return <p className="text-gray-500 mt-4">No data available.</p>;
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="overflow-y-auto max-h-96">
      {" "}
      {/* Scrollable container for large data */}
      <table className="w-full bg-white border rounded-lg shadow-md">
        <thead className="bg-gray-100 border-b">
          <tr>
            {columns.map((col) => (
              <th
                key={col}
                className="py-3 px-4 text-left font-medium text-gray-700 sticky top-0 bg-gray-100 z-10" // Sticky header styling
              >
                <span className="mr-2">{col}</span>
                <span className="text-sm text-gray-500">
                  ({inferredData[col]})
                </span>
                <DropdownMenu
                  column={col}
                  currentType={inferredData[col]}
                  onTypeChange={onTypeChange}
                />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index} className="border-b hover:bg-gray-50">
              {columns.map((col) => (
                <td key={col} className="py-2 px-4 text-gray-700">
                  {row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

DataTable.propTypes = {
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  inferredData: PropTypes.object.isRequired,
  onTypeChange: PropTypes.func.isRequired,
};

export default DataTable;
