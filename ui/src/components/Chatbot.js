// src/Chatbot.js
import React, { useState } from "react";
import {
  Box,
  TextField,
  IconButton,
  Typography,
  Paper,
  CircularProgress,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import axios from "axios";
import "../css/Chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async () => {
    if (input.trim()) {
      const userMessage = { text: input, user: "user" };
      setMessages([...messages, userMessage]);
      setInput("");

      setIsTyping(true);
      try {
        const response = await axios.post(
          "http://127.0.0.1:5050/answer-simple",
          {
            message: input,
          },
        );
        console.log("Response from server:", response.data.bot);
        const botMessage = { text: response.data.bot, user: "bot" };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error("Error sending message:", error);
        const errorMessage = {
          text: "Error getting response from the server",
          user: "bot",
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      } finally {
        setIsTyping(false);
      }
    }
  };

  return (
    <Paper elevation={3} className="chatbot-container">
      <Box className="chatbot-messages">
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
      <Box display="flex" alignItems="center" className="chatbot-input">
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
