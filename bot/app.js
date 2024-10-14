import React, { useState } from "react";
import Chatbot from "./components/Chatbot";
import "./App.css";

function App() {
  const [lightMode, setLightMode] = useState(true);

  const toggleTheme = () => {
    setLightMode((prevMode) => !prevMode);
  };

  return (
    <div className={`app ${lightMode ? "light-mode" : "dark-mode"}`}>
      <header className="app-header">
        <h1>Document Processor</h1>
        <label className="theme-switch">
          <input type="checkbox" onChange={toggleTheme} />
          <span>Switch to {lightMode ? "Dark" : "Light"} Mode</span>
        </label>
      </header>
      <Chatbot lightMode={lightMode} />
    </div>
  );
}

export default App;
