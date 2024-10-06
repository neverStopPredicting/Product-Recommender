import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatApp = () => {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (venueName) => {
    try {
      // Make a GET request to the FastAPI backend
      const response = await axios.get(`http://127.0.0.1:8000/${venueName}`);
      const reply = response.data; // Assuming the response contains the chat bot's reply
      
      // Update messages with both user input and bot reply
      setMessages((prevMessages) => [...prevMessages, `User: ${venueName}`, `Bot: ${reply}`]);
    } catch (error) {
      console.error('Error fetching data from backend:', error);
      setMessages((prevMessages) => [...prevMessages, `Error: ${error.message}`]);
    }
  };

  return (
    <div style={{ width: '400px', margin: '0 auto' }}>
      <h2>Simple Chat</h2>
      <MessageList messages={messages} />
      <MessageInput sendMessage={sendMessage} />
    </div>
  );
};

export default ChatApp;
