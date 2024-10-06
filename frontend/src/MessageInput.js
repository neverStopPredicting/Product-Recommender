import React, { useState } from 'react';

const MessageInput = ({ sendMessage }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      sendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Type a venue"
        style={{ width: '80%', marginRight: '10px', fontSize: '16px' }}
      />
      <button type="submit">Send</button>
    </form>
  );
};

export default MessageInput;