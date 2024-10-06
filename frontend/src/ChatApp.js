import React, { useState } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatApp = () => {
  const [messages, setMessages] = useState([]);

  const sendMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
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