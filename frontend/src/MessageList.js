import React from 'react';

const MessageList = ({ messages }) => {
  const renderMessageLines = (text) => {
    return text.split('\n').map((line, index) => (
      <React.Fragment key={index}>
        {line}
        {index < text.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  return (
    <div style={{ height: '700px', width: '600px', overflowY: 'scroll', border: '1px solid #ccc', marginBottom: '10px' }}>
      {messages.map((msg, index) => (
        <div key={index}>
          {msg.startsWith("User:") ? (
            <>
              <strong>Ari:</strong> {msg.replace("User: ", "")}
            </>
          ) : (
            <>
              <strong>Bot:</strong> {renderMessageLines(msg.replace("Bot: ", ""))}
            </>
          )}
        </div>
      ))}
    </div>
  );
};

export default MessageList;