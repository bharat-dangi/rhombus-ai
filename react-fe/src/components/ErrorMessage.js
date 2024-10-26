import React from "react";
import PropTypes from "prop-types";

// Displays an error message in a styled box
const ErrorMessage = ({ message }) => {
  return (
    <div className="bg-red-100 text-red-700 p-4 rounded-lg mb-6 text-center font-medium">
      {message}
    </div>
  );
};

ErrorMessage.propTypes = {
  message: PropTypes.string.isRequired,
};

export default ErrorMessage;
