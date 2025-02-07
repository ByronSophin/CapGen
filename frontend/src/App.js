import React, { useState } from "react";
import DownloadVideo from "./components/DownloadVideo";
import PreviewVideo from "./components/PreviewVideo";
import UploadVideo from "./components/UploadVideo";
import "./styles.css";

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [captionedVideoUrl, setCaptionedVideoUrl] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = (file) => {
    setVideoFile(file);
    setCaptionedVideoUrl(null); // Reset captioned video URL
  };

  const handleGenerateCaptions = async () => {
    if (!videoFile) return;

    setIsProcessing(true);

    const formData = new FormData();
    formData.append("file", videoFile);

    try {
      const response = await fetch("http://localhost:8000/transcribe/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setCaptionedVideoUrl(data.output_path);
      } else {
        console.error("Error generating captions");
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>
          <span id="cap">Cap</span>
          <span id="gen">Gen</span>
        </h1>
      </header>
      <div className="container">
        <UploadVideo onFileUpload={handleFileUpload} />
        {videoFile && (
          <PreviewVideo
            videoFile={videoFile}
            onGenerateCaptions={handleGenerateCaptions}
            isProcessing={isProcessing}
          />
        )}
        {captionedVideoUrl && (
          <DownloadVideo captionedVideoUrl={captionedVideoUrl} />
        )}
      </div>
    </div>
  );
}

export default App;
