import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";

const API_BASE = "http://localhost:8000";

function App() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/health`).then(async (r) => {
      if (r.ok) setStatus("Backend connected ✅");
      else setStatus("Backend not responding ❌");
    }).catch(() => setStatus("Backend not responding ❌"));
  }, []);

  async function handleSpeak() {
    setAudioUrl("");
    const fd = new FormData();
    fd.append("text", text);

    const res = await fetch(`${API_BASE}/speak`, { method: "POST", body: fd });
    if (!res.ok) {
      alert("Error: " + (await res.text()));
      return;
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setAudioUrl(url);
  }

  return (
    <div className="card">
      <h1>Offline Text → Speech</h1>
      
      <p className={status.includes("✅") ? "ok" : "err"}>{status}</p>
      <textarea
        placeholder="Type something to speak..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <div className="row">
        <button className="primary" onClick={handleSpeak}>Speak</button>
        <button onClick={() => { setText(""); setAudioUrl(""); }}>Clear</button>
      </div>
      {audioUrl && (
        <div>
          <audio controls src={audioUrl}></audio>
          <div className="row">
            <a href={audioUrl} download="speech.mp3">Download MP3</a>
          </div>
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
