
import React, { useState } from "react";
import Chat from "./components/chat";
import './App.css'
function App() {
  const [activeView, setActiveView] = useState("chat");

  // Handle sidebar navigation
  const handleViewChange = (view) => {
    setActiveView(view);
    console.log(`Switched to ${view} view`);
  };

  return (
    <div className="app">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">🤖</div>
            <h2>AI Chat</h2>
          </div>

          <div className="session-info">
            <div className="session-badge">
              <span className="session-icon">🤖</span>
              <div className="session-details">
                <span className="session-title">AI Chat Agent</span>
                <span className="session-id">
                  Session: {Math.random().toString(36).substr(2, 12)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Buttons */}
        <nav className="sidebar-nav">
          <button
            className={`nav-item ${activeView === "chat" ? "active" : ""}`}
            onClick={() => handleViewChange("chat")}
          >
            💬 Chat
          </button>

          <button
            className={`nav-item ${activeView === "about" ? "active" : ""}`}
            onClick={() => handleViewChange("about")}
          >
            ℹ️ About
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {activeView === "chat" && <Chat />}

        {activeView === "about" && (
          <div className="about">
            <h2>About</h2>
            <p>This is an AI Chat application built with React and FastAPI.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
