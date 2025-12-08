import React, { useState, useEffect, useRef } from "react";
import styles from "./ChatWidget.module.css";
import { sendChatRequest, ChatMessage, SourceReference } from "../services/api";

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const toggleChat = () => setIsOpen(!isOpen);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    const handleOpenContext = (e: CustomEvent) => {
      const selectedText = e.detail?.text;
      if (selectedText) {
        setIsOpen(true);
        // We can either auto-send or just pre-fill. 
        // Let's auto-send a message like "Explain this: ..." or just add the context to the next message?
        // Let's add it to a hidden state "pendingContext" or similar, or just prepend to input.
        // User story says: "select that specific text and ask the AI to explain it"
        // So let's pre-fill the input with "Explain this text: ..." and attach the context metadata.
        
        // But our API takes `selected_text` separately. 
        // So we need state for it.
        setInput(`Explain this: "${selectedText.substring(0, 50)}..."`);
        // We should store the full text to send with the request.
        // For MVP, let's just use the input or add a visual indicator that text is selected.
        // We'll add a `selectedContext` state.
      }
    };

    window.addEventListener("openChatWithContext" as any, handleOpenContext);
    return () => window.removeEventListener("openChatWithContext" as any, handleOpenContext);
  }, []);
  
  // New state for selected context
  const [selectedContext, setSelectedContext] = useState<string | null>(null);

  // Update listener to set selectedContext
  useEffect(() => {
    const handleOpenContext = (e: CustomEvent) => {
      const text = e.detail?.text;
      if (text) {
        setIsOpen(true);
        setSelectedContext(text);
        setInput("Explain this selection");
      }
    };
     window.addEventListener("openChatWithContext" as any, handleOpenContext);
    return () => window.removeEventListener("openChatWithContext" as any, handleOpenContext);
  }, []);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg: ChatMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);
    
    // Clear context after sending? Or keep it? Usually clear.
    const contextToSend = selectedContext;
    setSelectedContext(null); 

    const botMsgIndex = messages.length + 1; // Anticipated index
    // Placeholder for bot message
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    let currentResponse = "";

    await sendChatRequest(
      {
        query: userMsg.content,
        selected_text: contextToSend || undefined,
        history: messages,
      },
      (token) => {
        currentResponse += token;
        setMessages((prev) => {
          const newMsgs = [...prev];
          newMsgs[botMsgIndex] = { ...newMsgs[botMsgIndex], content: currentResponse };
          return newMsgs;
        });
      },
      (sources) => {
        // Handle sources display if needed
        // For MVP just appending to message content or storing separately
        // Let's append formatted sources to the bot message content for simplicity
        const sourcesText = `

Sources:
` + sources.map(s => `- ${s.source_file}`).join("\n");
        currentResponse += sourcesText;
         setMessages((prev) => {
          const newMsgs = [...prev];
          newMsgs[botMsgIndex] = { ...newMsgs[botMsgIndex], content: currentResponse };
          return newMsgs;
        });
      },
      (error) => {
        setMessages((prev) => [...prev, { role: "system", content: `Error: ${error}` }]);
        setIsLoading(false);
      },
      () => {
        setIsLoading(false);
      }
    );
  };

  return (
    <>
      <button className={styles.toggleButton} onClick={toggleChat}>
        {isOpen ? "X" : "💬"}
      </button>
      {isOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.header}>
            <span>AI Assistant</span>
            <button onClick={toggleChat} style={{ background: "none", border: "none", color: "white", cursor: "pointer" }}>
              _
            </button>
          </div>
          <div className={styles.messages}>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`${styles.message} ${ 
                  msg.role === "user" ? styles.userMessage : styles.botMessage
                }`}
              >
                {msg.content}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className={styles.inputArea}>
            {selectedContext && (
              <div style={{ fontSize: '10px', color: '#666', padding: '0 0 5px 0', display: 'flex', justifyContent: 'space-between' }}>
                <span>Selected: "{selectedContext.substring(0, 30)}..."</span>
                <button onClick={() => setSelectedContext(null)} style={{ border: 'none', background: 'none', cursor: 'pointer' }}>x</button>
              </div>
            )}
            <div style={{ display: 'flex', gap: '5px' }}>
              <input
                className={styles.input}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="Ask a question..."
                disabled={isLoading}
              />
              <button className={styles.sendButton} onClick={handleSend} disabled={isLoading}>
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;