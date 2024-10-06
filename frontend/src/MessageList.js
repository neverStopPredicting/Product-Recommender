import React from 'react';

const MessageList = ({ messages }) => {
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
                <strong>Bot:</strong>
                <span dangerouslySetInnerHTML={{ __html: msg.replace("Bot: ", "") }} />
              </>
            )}
          </div>
        ))}
      </div>
    );
  };

export default MessageList;