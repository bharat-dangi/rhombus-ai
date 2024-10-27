import React, { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";
import DropdownMenu from "./DropdownMenu";

const DataTable = ({
  data,
  inferredData,
  onLoadMore,
  loading,
  onTypeChange,
}) => {
  const [openDropdown, setOpenDropdown] = useState(null); // Track which dropdown is open
  const tableContainerRef = useRef(null);

  // Toggle dropdown for a specific column
  const handleToggleDropdown = (column) => {
    setOpenDropdown((prev) => (prev === column ? null : column)); // Close if already open
  };

  // Infinite scroll within the table container
  useEffect(() => {
    const handleScroll = () => {
      if (!tableContainerRef.current || loading) return;

      const { scrollTop, scrollHeight, clientHeight } =
        tableContainerRef.current;
      if (scrollTop + clientHeight >= scrollHeight - 50) {
        onLoadMore();
      }
    };

    const container = tableContainerRef.current;
    container.addEventListener("scroll", handleScroll);
    return () => container.removeEventListener("scroll", handleScroll);
  }, [onLoadMore, loading]);

  if (!data || data.length === 0) {
    return <p className="text-gray-500 mt-4">No data available.</p>;
  }

  const columns = Object.keys(data[0]);

  return (
    <div ref={tableContainerRef} className="overflow-y-auto max-h-96">
      <table className="w-full bg-white border rounded-lg shadow-md">
        <thead className="bg-gray-100 border-b sticky top-0">
          <tr>
            {columns.map((col) => (
              <th
                key={col}
                className="py-3 px-4 text-left font-medium text-gray-700 sticky top-0 bg-gray-100 z-10"
              >
                <span className="mr-2">{col}</span>
                <span className="text-sm text-gray-500">
                  ({inferredData[col]})
                </span>
                <DropdownMenu
                  column={col}
                  currentType={inferredData[col]}
                  onTypeChange={onTypeChange}
                  isOpen={openDropdown === col} // Open only for current column
                  onToggle={() => handleToggleDropdown(col)} // Toggle open/close
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
  onLoadMore: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
  onTypeChange: PropTypes.func.isRequired,
};

export default DataTable;
