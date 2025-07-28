import React, { useState } from 'react';
import './FileUpload.css';

const FileUpload = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [textFile, setTextFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [transcriptText, setTranscriptText] = useState('');
  const [summaryText, setSummaryText] = useState('');

  const handleAudioUpload = (e) => {
    setAudioFile(e.target.files[0]);
    setTextFile(null);
  };

  const handleTextUpload = (e) => {
    setTextFile(e.target.files[0]);
    setAudioFile(null);
  };

  const handleSend = async () => {
    if (!audioFile && !textFile) {
      alert("Please upload an audio or text file.");
      return;
    }

    setUploadStatus("⏳ Processing...");
    setTranscriptText('');
    setSummaryText('');

    const formData = new FormData();
    let endpoint = '';

    if (audioFile) {
      formData.append("file", audioFile);
      endpoint = "http://localhost:8000/upload/audio";
    } else if (textFile) {
      formData.append("file", textFile);
      endpoint = "http://localhost:8000/upload/text";
    }

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server response: ${errorText}`);
      }

      const data = await response.json();
      const transcript = data.transcript || '';
      const summary = data.summary || '';

      setUploadStatus("✅ Processed successfully.");
      setTranscriptText(transcript);
      setSummaryText(summary);

      alert("✅ File processed successfully and summary generated!");

    } catch (error) {
      console.error("❌ Error:", error.message);
      setUploadStatus(`❌ Failed to process file. ${error.message}`);
    }
  };

  return (
    <div className="upload-container">
      <h2 className="title">🎙️ Audio/Text Summarizer</h2>

      <div className="upload-section">
        <label className="upload-label">🎧 Upload Audio File</label>
        <input
          type="file"
          accept="audio/*"
          onChange={handleAudioUpload}
          className="file-input"
        />
        {audioFile && <p className="file-name">Selected: {audioFile.name}</p>}
      </div>

      <div className="upload-section">
        <label className="upload-label">📄 Upload Text File</label>
        <input
          type="file"
          accept=".txt"
          onChange={handleTextUpload}
          className="file-input"
        />
        {textFile && <p className="file-name">Selected: {textFile.name}</p>}
      </div>

      <button
        className="send-button"
        style={{ backgroundColor: 'blue', color: 'white', marginTop: '15px' }}
        onClick={handleSend}
      >
        Send Transcript
      </button>

      {uploadStatus && <p className="upload-status">{uploadStatus}</p>}

      {(transcriptText || summaryText) && (
        <div className="result-box">
          {transcriptText && (
            <>
              <h3>📝 Transcript</h3>
              <pre className="result-text">{transcriptText}</pre>
            </>
          )}

          {summaryText && (
            <>
              <h3>📌 Summary</h3>
              <pre className="result-text">{summaryText}</pre>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
