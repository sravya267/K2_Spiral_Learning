// src/components/StatusMessage.js
import React from 'react';
import './StatusMessage.css';

const StatusMessage = ({ message, isError, visible }) => {
  if (!visible) return null;

  return (
    <div className={`status-message ${isError ? 'error' : 'success'}`}>
      {message}
    </div>
  );
};

export default StatusMessage;