import React, { useState, useEffect, useCallback } from 'react';
import styles from './TextSelectionPopup.module.css';

interface TextSelectionPopupProps {
    onAskAI: (selectedText: string) => void;
}

export default function TextSelectionPopup({ onAskAI }: TextSelectionPopupProps) {
    const [isVisible, setIsVisible] = useState(false);
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [selectedText, setSelectedText] = useState('');

    const handleMouseUp = useCallback(() => {
        const selection = window.getSelection();
        const text = selection?.toString().trim();

        if (text && text.length > 0) {
            const range = selection?.getRangeAt(0);
            const rect = range?.getBoundingClientRect();

            if (rect) {
                setPosition({
                    x: rect.left + rect.width / 2,
                    y: rect.top - 10 + window.scrollY
                });
                setSelectedText(text);
                setIsVisible(true);
            }
        } else {
            setIsVisible(false);
        }
    }, []);

    const handleMouseDown = useCallback((e: MouseEvent) => {
        const target = e.target as HTMLElement;
        if (!target.closest(`.${styles.popup}`)) {
            setIsVisible(false);
        }
    }, []);

    useEffect(() => {
        document.addEventListener('mouseup', handleMouseUp);
        document.addEventListener('mousedown', handleMouseDown);

        return () => {
            document.removeEventListener('mouseup', handleMouseUp);
            document.removeEventListener('mousedown', handleMouseDown);
        };
    }, [handleMouseUp, handleMouseDown]);

    const handleAskAI = () => {
        onAskAI(selectedText);
        setIsVisible(false);
        window.getSelection()?.removeAllRanges();
    };

    if (!isVisible) return null;

    return (
        <div
            className={styles.popup}
            style={{
                left: `${position.x}px`,
                top: `${position.y}px`,
            }}
        >
            <button className={styles.askButton} onClick={handleAskAI}>
                <span className={styles.icon}>✨</span>
                Ask AI
            </button>
        </div>
    );
}
