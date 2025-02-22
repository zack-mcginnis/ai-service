import React, { useState } from 'react';
import './Chat.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface Provider {
  id: string;
  name: string;
  models: string[];
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const providers: Provider[] = [
  {
    id: 'openai',
    name: 'OpenAI',
    models: ['gpt-4', 'gpt-3.5-turbo'],
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    models: ['claude-3-opus-20240229', 'claude-3-sonnet-20240229'],
  },
  {
    id: 'gemini',
    name: 'Google Gemini',
    models: ['gemini-pro'],
  },
  {
    id: 'deepseek',
    name: 'Deepseek',
    models: ['deepseek-r1:1.5b'],
  },
];

export const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [provider, setProvider] = useState(providers[0].id);
  const [model, setModel] = useState(providers[0].models[0]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_URL}/generate?` +
        new URLSearchParams({
          input: input,
          provider: provider,
          ai_model: model,
        })
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.output,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setError(error instanceof Error ? error.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="model-selector">
        <select value={provider} onChange={(e) => {
          setProvider(e.target.value);
          setModel(providers.find(p => p.id === e.target.value)?.models[0] || '');
        }}>
          {providers.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
        <select value={model} onChange={(e) => setModel(e.target.value)}>
          {providers.find(p => p.id === provider)?.models.map(m => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>

      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.content}
          </div>
        ))}
        {isLoading && <div className="loading">Thinking...</div>}
        {error && <div className="error">Error: {error}</div>}
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  );
}; 