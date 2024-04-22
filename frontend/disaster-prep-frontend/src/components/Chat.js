import React, { useState } from 'react';
import axios from 'axios';

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
    <div>
      <h2>Chat</h2>
      <div className="chat-history">
        {chatHistory.map((message, index) => (
          <div key={index}>
            <p>User: {message.user}</p>
            <p>Bot: {message.bot}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={userInput}
        onChange={handleInputChange}
        placeholder="Type your message..."
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
}

export default Chat;