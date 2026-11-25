
import { useEffect, useState } from "react";
import { checkBackend } from "./services/api";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [error, setError] = useState("");

  useEffect(() => {
    checkBackend()
      .then((data) => {
        setBackendStatus(data.status);
      })
      .catch(() => {
        setBackendStatus("Disconnected");
        setError("Could not connect to FastAPI.");
      });
  }, []);

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0b1120",
      color: "#e2e8f0",
      fontFamily: "Arial, sans-serif",
      padding: "40px"
    }}>
      <h1>LegacyMind</h1>

      <p>
        AI-Powered Legacy Code Modernization Platform
      </p>

      <div style={{
        marginTop: "30px",
        padding: "20px",
        background: "#172033",
        borderRadius: "12px",
        maxWidth: "400px"
      }}>
        <h2>Backend Connection</h2>

        <p>
          Status: {backendStatus}
        </p>

        {error && <p>{error}</p>}
      </div>
    </div>
  );
}

export default App;
