import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/App.css";

import Chatbot from "./components/Chatbot";
import "react-chatbot-kit/build/main.css";

const App = () => {
  return (
    <div className="app-container">
      {/* Explanatory Sidebar */}
      <div className="sidebar">
        <h2>Starbot</h2>
        <p>
          Meet Starbot! A chatbot that can answer the various types of questions
          about famous landmarks:
          <br /> <br />
          <ul>
            <li>Basic facts (e.g., "Where is the Eiffel Tower located?")</li>
            <li>
              Historical significance (e.g., "Why is the Great Wall of China
              famous?")
            </li>
            <li>Trivia (e.g., "How tall is the Burj Khalifa?”)</li>
          </ul>
        </p>
        <p>
          To get started, type your question in the chatbot window and press
          enter
          <br /> <br />
          Starbot is equipped with memory, so feel free to ask follow-up
          questions!
          <br /> <br />
          And don't you worry about accidentally closing the window or
          refreshing it, your chat is here to stay!
          <br /> <br />
          Unless you don't want it to of course, in which case you can reset the
          chat by clicking that trash button.
        </p>
      </div>
      {/* Chatbot Component */}
      <div className="chatbot-wrapper">
        <Chatbot />
      </div>
      <div className="empty-column"></div>
    </div>
  );
};

export default App;
