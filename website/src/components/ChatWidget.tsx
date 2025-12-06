import React, { useState } from 'react';
import styles from './ChatWidget.module.css';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChat = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResponse(data.answer);
    } catch (e) {
      setResponse('Error connecting to AI.');
    }
    setLoading(false);
  };

  return (
    <div className={styles.widgetContainer}>
      {!isOpen && (
        <button className={styles.floatButton} onClick={() => setIsOpen(true)}>
          AI Chat
        </button>
      )}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.header}>
            <span>Ask the Book</span>
            <button onClick={() => setIsOpen(false)}>X</button>
          </div>
          <div className={styles.body}>
            {response && <div className={styles.response}>{response}</div>}
            {loading && <div>Thinking...</div>}
          </div>
          <div className={styles.inputArea}>
            <input 
              value={query} 
              onChange={(e) => setQuery(e.target.value)} 
              onKeyDown={(e) => e.key === 'Enter' && handleChat()}
              placeholder="Ask a question..."
            />
            <button onClick={handleChat}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}
