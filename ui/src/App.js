import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/App.css";

import Chatbot from "./components/Chatbot";
import "react-chatbot-kit/build/main.css";

const App = () => {
  return (
    <div className="App">
      <Chatbot />
    </div>
  );
};

export default App;
