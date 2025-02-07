import React from "react";

function PreviewVideo({ videoFile, onGenerateCaptions, isProcessing }) {
  const videoUrl = URL.createObjectURL(videoFile);

  return (
    <div className="preview">
      <h2>Preview</h2>
      <video src={videoUrl} controls />
      <div className="generate">
        <button
          className="btn"
          onClick={onGenerateCaptions}
          disabled={isProcessing}
        >
          {isProcessing ? "Generating Captions..." : "Generate Captions"}
        </button>
      </div>
    </div>
  );
}

export default PreviewVideo;
