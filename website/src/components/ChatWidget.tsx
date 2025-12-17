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

    // Add empty assistant message that will be filled with streaming tokens
    let assistantContent = '';
    setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

    try {
      const { sendChatRequest } = await import('../services/api');

      await sendChatRequest(
        {
          query: queryToSend,
          history: messages.map(m => ({ role: m.role, content: m.content }))
        },
        // onToken - append each token to the assistant message
        (token: string) => {
          assistantContent += token;
          setMessages(prev => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = { role: 'assistant', content: assistantContent };
            return newMessages;
          });
        },
        // onSources - ignore for now
        () => { },
        // onError
        (error: string) => {
          console.error('Chat error:', error);
          setMessages(prev => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = {
              role: 'assistant',
              content: 'Error connecting to AI. Please try again.'
            };
            return newMessages;
          });
        },
        // onComplete
        () => {
          setLoading(false);
        }
      );
    } catch (e) {
      console.error('Chat error:', e);
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          role: 'assistant',
          content: 'Error connecting to AI. Please try again.'
        };
        return newMessages;
      });
      setLoading(false);
    }
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
