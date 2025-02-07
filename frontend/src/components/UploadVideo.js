import React from "react";

function UploadVideo({ onFileUpload }) {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <div className="card">
      <h3>Upload Files</h3>
      <div className="drop_box">
        <div>
          <h4>Select a file to generate captions</h4>
        </div>
        <p>Files Supported: MOV, MP4</p>
        <input
          type="file"
          id="fileInput"
          accept=".mov,.mp4"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />
        <button
          className="btn"
          onClick={() => document.getElementById("fileInput").click()}
        >
          Upload File
        </button>
      </div>
    </div>
  );
}

export default UploadVideo;
