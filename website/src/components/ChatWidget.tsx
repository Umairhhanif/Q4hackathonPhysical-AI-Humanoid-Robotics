import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatWidget.module.css';
import TextSelectionPopup from './TextSelectionPopup';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleChat = async (customQuery?: string) => {
    const queryToSend = customQuery || query;
    if (!queryToSend) return;

    // Add user message
    const userMessage: Message = { role: 'user', content: queryToSend };
    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: queryToSend }),
      });
      const data = await res.json();

      // Add assistant message
      const assistantMessage: Message = { role: 'assistant', content: data.answer };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (e) {
      const errorMessage: Message = { role: 'assistant', content: 'Error connecting to AI. Please try again.' };
      setMessages(prev => [...prev, errorMessage]);
    }
    setLoading(false);
  };

  const handleAskAIFromSelection = (selectedText: string) => {
    setIsOpen(true);
    const questionQuery = `Explain this: "${selectedText.substring(0, 200)}${selectedText.length > 200 ? '...' : ''}"`;
    setTimeout(() => {
      handleChat(questionQuery);
    }, 100);
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <>
      <TextSelectionPopup onAskAI={handleAskAIFromSelection} />

      <div className={styles.widgetContainer}>
        {!isOpen && (
          <button className={styles.floatButton} onClick={() => setIsOpen(true)}>
            ✨ AI Chat
          </button>
        )}
        {isOpen && (
          <div className={styles.chatWindow}>
            <div className={styles.header}>
              <span>Ask the Book</span>
              <div className={styles.headerButtons}>
                {messages.length > 0 && (
                  <button onClick={handleClearChat} title="Clear chat">🗑️</button>
                )}
                <button onClick={() => setIsOpen(false)}>✕</button>
              </div>
            </div>
            <div className={styles.body}>
              {messages.length === 0 && !loading && (
                <div className={styles.placeholder}>
                  👋 Hi! Ask any question about Physical AI and Humanoid Robotics, or select text on the page and click "Ask AI"
                </div>
              )}
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={msg.role === 'user' ? styles.userMessage : styles.assistantMessage}
                >
                  {msg.role === 'user' && <span className={styles.messageLabel}>You</span>}
                  {msg.role === 'assistant' && <span className={styles.messageLabel}>AI</span>}
                  <div className={styles.messageContent}>{msg.content}</div>
                </div>
              ))}
              {loading && (
                <div className={styles.assistantMessage}>
                  <span className={styles.messageLabel}>AI</span>
                  <div className={styles.loading}>✨ Thinking...</div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            <div className={styles.inputArea}>
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !loading && handleChat()}
                placeholder="Ask a question..."
                disabled={loading}
              />
              <button onClick={() => handleChat()} disabled={loading || !query.trim()}>
                {loading ? '...' : 'Send'}
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
