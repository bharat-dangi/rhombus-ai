import React from "react";
import PropTypes from "prop-types";

const UpdateTypesButton = ({ onSave }) => (
  <button
    onClick={onSave}
    className="px-4 py-2 mt-4 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-lg"
  >
    Save Changes
  </button>
);

UpdateTypesButton.propTypes = {
  onSave: PropTypes.func.isRequired,
};

export default UpdateTypesButton;
