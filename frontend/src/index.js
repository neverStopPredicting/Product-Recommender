import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import ChatApp from './ChatApp';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ChatApp />
  </React.StrictMode>
);