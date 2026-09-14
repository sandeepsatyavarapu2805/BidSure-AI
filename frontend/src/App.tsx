import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState("Checking backend...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/health", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => setStatus(`Backend: ${data.status}`))
      .catch(() => setStatus("Backend unavailable"));
  }, []);

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>BidSure AI</h1>
      <p>{status}</p>
    </main>
  );
}

export default App;