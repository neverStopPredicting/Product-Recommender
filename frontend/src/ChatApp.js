import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatApp = () => {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (venueName) => {
    try {
      const response = await axios.get(`http://backend:8000/${venueName}`);
      const reply = response.data; // Make sure you're accessing the right property
  
      // Update messages without duplicating User and Bot labels
      setMessages((prevMessages) => [
        ...prevMessages,
        `User: ${venueName}`,  // User input
        `Bot: ${reply}`         // Bot response
      ]);
    } catch (error) {
      console.error('Error fetching data from backend:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        `Error: ${error.message}`  // Handle error
      ]);
    }
  };
  

  return (
    <div style={{ width: '660px', margin: '0 auto' }}>
      <h2>Product Recommender</h2>
      <MessageList messages={messages} />
      <MessageInput sendMessage={sendMessage} />
    </div>
  );
};

export default ChatApp;
