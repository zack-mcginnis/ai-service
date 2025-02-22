import React from 'react';
import { Chat } from './components/Chat.tsx';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Chat Reference App</h1>
      </header>
      <main>
        <Chat />
      </main>
    </div>
  );
}

export default App; 