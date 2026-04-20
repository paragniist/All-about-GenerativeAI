import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

// Define your endpoints outside the component
const API_ENDPOINTS = {
  CHAT: 'http://localhost:8000/chat' // Adjust to your FastAPI URL
};

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState(null);
  
  // Ref to automatically scroll to the newest message
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle User Session on Mount
  useEffect(() => {
    const storedUserId = localStorage.getItem('chat_user_id');
    if (storedUserId) {
      setUserId(storedUserId);
    } else {
      const newUserId = 'user_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('chat_user_id', newUserId);
      setUserId(newUserId);
    }
  }, []); // Empty array: only runs ONCE on mount

  const handleSendMessage = async (e) => {
    // Prevent form refresh if wrapped in a <form>
    e?.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toLocaleTimeString()
    };

    // Optimistic Update
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(API_ENDPOINTS.CHAT, {
        prompt: userMessage.content,
        user_id: userId
      });

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.data.response,
        timestamp: new Date().toLocaleTimeString(),
        telemetry: {
          tokens: response.data.tokens_used,
          responseTime: response.data.response_time_ms
        }
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('❌ API request failed:', error);
      
      // Add an error message to the UI so the user knows what happened
      const errorMessage = {
        id: Date.now() + 2,
        type: 'error',
        content: "Sorry, I'm having trouble connecting to the server.",
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-window">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.type}`}>
            <p>{msg.content}</p>
            <span className="time">{msg.timestamp}</span>
          </div>
        ))}
        {isLoading && <div className="loader">Assistant is thinking...</div>}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSendMessage} className="input-area">
        <input 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type a message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default Chat;