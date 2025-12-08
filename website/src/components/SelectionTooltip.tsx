import React, { useEffect, useState } from 'react';

const SelectionTooltip: React.FC = () => {
  const [position, setPosition] = useState<{ top: number; left: number } | null>(null);
  const [selectedText, setSelectedText] = useState<string>("");

  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      if (!selection || selection.isCollapsed) {
        setPosition(null);
        return;
      }

      const text = selection.toString().trim();
      if (!text) {
        setPosition(null);
        return;
      }

      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      // Show tooltip above the selection
      setPosition({
        top: rect.top + window.scrollY - 40,
        left: rect.left + window.scrollX + (rect.width / 2) - 40,
      });
      setSelectedText(text);
    };

    document.addEventListener("mouseup", handleSelectionChange);
    document.addEventListener("keyup", handleSelectionChange);
    return () => {
      document.removeEventListener("mouseup", handleSelectionChange);
      document.removeEventListener("keyup", handleSelectionChange);
    };
  }, []);

  if (!position) return null;

  const handleAskAI = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent clearing selection
    const event = new CustomEvent("openChatWithContext", { detail: { text: selectedText } });
    window.dispatchEvent(event);
    setPosition(null); // Hide tooltip after click
  };

  return (
    <div
      style={{
        position: 'absolute',
        top: position.top,
        left: position.left,
        zIndex: 2000,
        backgroundColor: 'var(--ifm-color-primary)',
        color: 'white',
        padding: '5px 10px',
        borderRadius: '4px',
        cursor: 'pointer',
        boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
        fontSize: '12px',
        fontWeight: 'bold',
      }}
      onMouseDown={(e) => e.preventDefault()} // Prevent taking focus
      onClick={handleAskAI}
    >
      Ask AI
    </div>
  );
};

export default SelectionTooltip;
