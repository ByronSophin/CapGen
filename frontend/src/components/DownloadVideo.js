import React from "react";

function DownloadVideo({ captionedVideoUrl }) {
  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = captionedVideoUrl;
    link.download = captionedVideoUrl.split("/").pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="preview">
      <h2>Preview Captioned Video</h2>
      <video src={captionedVideoUrl} controls />
      <div className="generate">
        <button className="btn" onClick={handleDownload}>
          Download Video
        </button>
      </div>
    </div>
  );
}

export default DownloadVideo;
