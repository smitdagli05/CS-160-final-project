import React, { useState } from 'react';
import axios from 'axios';
import Navigation from './Navigation';
import './Chat.css';

function Chat() {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSendMessage = async () => {
    try {
      const response = await axios.post('/api/chat', {
        user_input: userInput,
      });
      const botResponse = response.data.response;
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { user: userInput, bot: botResponse },
      ]);
      setUserInput('');
    } catch (error) {
      console.error('Error sending message:', error);
      // Handle error, show an error message to the user
    }
  };

  return (
    <div className="chat-container">
      <div className="header">Chat</div>
      <div className="chat-content">
        <div className="virtual-coach">
          <div className="coach-icon"></div>
          <h3>Virtual Coach</h3>
          <p>Need assistance? Start chatting with your virtual coach!</p>
          <button className="new-chat-button" onClick={() => setChatHistory([])}>
            New Chat
          </button>
        </div>
        <div className="chat-history">
          {chatHistory.map((message, index) => (
            <div key={index} className="message">
              <p className="user-message">{message.user}</p>
              <p className="bot-message">{message.bot}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={userInput}
          onChange={handleInputChange}
          placeholder="Type your message..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
      <Navigation />
    </div>
  );
}

export default Chat;