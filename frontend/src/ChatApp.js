import React, { useState } from 'react';
import axios from 'axios';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (venueName) => {
    const url = `/${venueName}`;  // Use a relative URL
    console.log('Attempting to fetch from:', url);
    // Immediately add Ari's message to the chat
    setMessages(prevMessages => [...prevMessages, `User: ${venueName}`]);
    
    setIsLoading(true);
    try {
      const response = await axios.get(url);
      const reply = response.data; 
  
      // Add bot's response when it's ready
      setMessages(prevMessages => [...prevMessages, `Bot: ${reply}`]);
    } catch (error) {
      console.error('Error fetching data from backend:', error);
      let errorMessage = 'An error occurred while fetching data.';
      if (error.response) {
        errorMessage = `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No response received from the server. Please check if the backend is running.';
      } else {
        errorMessage = error.message;
      }
      setMessages(prevMessages => [
        ...prevMessages,
        `Error: ${errorMessage}`
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ width: '660px', margin: '0 auto' }}>
      <h2>Product Recommender</h2>
      <MessageList messages={messages} />
      <MessageInput sendMessage={sendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatApp;
