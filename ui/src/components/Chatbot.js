// src/Chatbot.js
import React, { useState, useEffect } from "react";
import {
  Box,
  TextField,
  IconButton,
  Typography,
  Paper,
  CircularProgress,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import DeleteIcon from "@mui/icons-material/Delete";
import axios from "axios";
import "../css/Chatbot.css";

const Chatbot = () => {
  // Hooks for managing messages, user input, and typing indicator
  const [messages, setMessages] = useState(() => {
    const savedMessages = localStorage.getItem("chatMessages");
    return savedMessages ? JSON.parse(savedMessages) : [];
  });
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  // Hook to persist messages in localStorage
  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
  }, [messages]);

  // Function to send user message and handle bot response
  const sendMessage = async () => {
    if (input.trim()) {
      const userMessage = { text: input, user: "user" };
      setMessages([...messages, userMessage]); // Add user message to state
      setInput(""); // Clear input field

      setIsTyping(true); // Show typing indicator
      try {
        const response = await axios.post(
          "http://127.0.0.1:5050/query_az_rag",
          {
            message: input,
          },
        );
        console.log("Response from server:", response.data.answer);
        console.log("Response from server 2:", response.data.srcs);
        const botMessage = { text: response.data.answer, user: "bot" };
        setMessages((prevMessages) => [...prevMessages, botMessage]); // Add bot response to state
      } catch (error) {
        console.error("Error sending message:", error);
        const errorMessage = {
          text: "Error getting response from the server",
          user: "bot",
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]); // Handle error in message state
      } finally {
        setIsTyping(false); // Hide typing indicator
      }
    }
  };

  // Function to clear chat messages and reset localStorage
  const handleClearMessages = () => {
    localStorage.removeItem("chatMessages"); // Remove messages from localStorage
    setMessages([]); // Clear messages in state
    fetch("http://localhost:5050/az_clear_memory", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => console.log(data)) // Log response from server
      .catch((error) => console.error("Error clearing memory:", error)); // Log error if any
  };

  return (
    <Paper elevation={3} className="chatbot-container">
      <Box className="chatbot-messages">
        {/* Render messages in conversational format */}
        {messages.map((msg, index) => (
          <Typography
            key={index}
            className={`message ${msg.user}`}
            variant="body1"
            component="div"
            sx={{
              backgroundColor: msg.user === "user" ? "#e1f5fe" : "#f1f8e9",
              textAlign: msg.user === "user" ? "right" : "left",
              padding: "8px",
              borderRadius: "8px",
              margin: "5px 0",
              maxWidth: "75%",
              alignSelf: msg.user === "user" ? "flex-end" : "flex-start",
            }}
          >
            {msg.text}
          </Typography>
        ))}
        {/* Show typing indicator when bot is typing */}
        {isTyping && (
          <Box
            display="flex"
            justifyContent="flex-start"
            alignItems="center"
            margin="10px"
          >
            <CircularProgress size={20} />
            <Typography variant="body2" marginLeft="10px">
              Bot is typing...
            </Typography>
          </Box>
        )}
      </Box>
      {/* Input field and buttons for user interaction */}
      <Box display="flex" alignItems="center" className="chatbot-input">
        <IconButton
          color="secondary"
          onClick={handleClearMessages}
          title="Clear Messages"
        >
          <DeleteIcon />
        </IconButton>
        <TextField
          fullWidth
          variant="outlined"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type a message..."
        />
        <IconButton color="primary" onClick={sendMessage}>
          <SendIcon />
        </IconButton>
      </Box>
    </Paper>
  );
};

export default Chatbot;
