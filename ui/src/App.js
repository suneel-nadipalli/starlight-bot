import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/App.css";

import Chatbot from "./components/Chatbot";
import "react-chatbot-kit/build/main.css";

const App = () => {
  return (
    <div className="app-container">
      <div className="sidebar">Sidebar</div>
      <div className="chatbot-wrapper">
        <Chatbot />
      </div>
      <div className="empty-column"></div>
    </div>
  );
};

export default App;
