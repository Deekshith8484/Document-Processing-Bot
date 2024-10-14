import React from "react";

const FileUpload = ({ onFileUpload }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <div className="file-upload">
      <input type="file" id="file-upload" onChange={handleFileChange} />
    </div>
  );
};

export default FileUpload;
