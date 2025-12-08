import React from 'react';
import ChatWidget from '../components/ChatWidget';
import SelectionTooltip from '../components/SelectionTooltip';

// Default implementation, that you can customize
export default function Root({children}) {
  return (
    <>
      {children}
      <SelectionTooltip />
      <ChatWidget />
    </>
  );
}