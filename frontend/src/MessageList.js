import React from 'react';

const MessageList = ({ messages }) => {
  return (
    <div style={{ height: '300px', overflowY: 'scroll', border: '1px solid #ccc', marginBottom: '10px' }}>
      {messages.map((msg, index) => (
        <div key={index}>
          <strong>User:</strong> {msg}
        </div>
      ))}
    </div>
  );
};

export default MessageList;