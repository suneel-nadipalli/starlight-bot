import React, { useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/App.css";
import { v4 as uuidv4 } from "uuid";

import Chatbot from "./components/Chatbot";
import "react-chatbot-kit/build/main.css";

const App = () => {
  useEffect(() => {
    // Check if UUID exists in local storage
    let userUUID = localStorage.getItem("userUUID");
    if (!userUUID) {
      // Generate a new UUID if not found
      userUUID = uuidv4();
      localStorage.setItem("userUUID", userUUID);
      console.log("New user has entered the chat!", userUUID);
    }
    console.log("User has returned!", userUUID);
  }, []);
  return (
    <div className="app-container">
      {/* Explanatory Sidebar */}
      <div className="sidebar">
        <h2>Starbot</h2>
        <p>
          Meet Starbot! A chatbot that can answer different assistance programs
          such as UAP, LIHEAP and others! Here are some questions to get you
          started:
          <br /> <br />
          <ul>
            <li>What is the UAP?</li>
            <li>When did Utility begin to administer the CAP program</li>
            <li>How much of a discount is provided for water/sewer bills?</li>
          </ul>
        </p>
        <p>
          To get started, type your question in the chatbot window and press
          enter
          <br /> <br />
          Starbot is equipped with memory, so feel free to ask follow-up
          questions.
          <br /> <br />
          And don't you worry about accidentally closing the window or
          refreshing it, your chat is here to stay.
          <br /> <br />
          Unless you don't want it to of course, in which case you can reset the
          chat by clicking that trash button.
          <br /> <br />
          <i>
            PS: If you get hit with the following message: "Error getting
            response from the server". Don't worry, it's on us! Just ask agian
            and you should be good to go. If all else fails, contact us at:
            blank
          </i>
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
