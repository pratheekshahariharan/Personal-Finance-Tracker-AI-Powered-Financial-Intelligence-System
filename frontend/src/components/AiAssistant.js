import React, { useState, useRef, useEffect } from "react";
import { chatAI } from "../services/api";

const SUGGESTIONS = [
  "How much can I spend on Food today?",
  "Analyze my spending habits",
  "How to reach my vacation goal?",
  "Am I overspending this month?"
];

export default function AiAssistant({ filters }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! I'm your Financial Co-Pilot. I can analyze your transactions, track your goals, and help you save smarter. What's on your mind?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) scrollToBottom();
  }, [messages, isOpen]);

  useEffect(() => {
    const handleTrigger = (e) => {
      setIsOpen(true);
      if (e.detail?.message) {
        handleSend(e.detail.message);
      }
    };
    window.addEventListener("trigger-ai-chat", handleTrigger);
    return () => window.removeEventListener("trigger-ai-chat", handleTrigger);
  }, []);

  const handleSend = async (text = input) => {
    const query = typeof text === "string" ? text : input;
    if (!query.trim()) return;
    
    const userMsg = { role: "user", content: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await chatAI(query, filters?.month, filters?.year);
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.response }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "I'm having trouble connecting to my brain right now. Please try again later!" }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  if (!isOpen) {
    return (
      <button 
        className="ai-fab" 
        onClick={() => setIsOpen(true)}
        style={{ display: "flex", alignItems: "center", gap: 10, padding: "14px 28px" }}
      >
        <span style={{ fontSize: "1.2rem" }}>✨</span>
        <span>Financial Co-Pilot</span>
      </button>
    );
  }

  return (
    <div className="ai-chat-window">
      <div className="ai-chat-header" style={{ background: "var(--primary)", color: "#fff", padding: "12px 16px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: "1.2rem" }}>✨</span>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <span style={{ fontSize: "0.95rem", fontWeight: 700 }}>FinTracker AI</span>
            <span style={{ fontSize: "0.65rem", opacity: 0.9 }}>Your Financial Co-Pilot</span>
          </div>
        </div>
        <button className="ai-close-btn" style={{ color: "#fff", background: "none", border: "none", fontSize: "1.2rem", cursor: "pointer" }} onClick={() => setIsOpen(false)}>✕</button>
      </div>
      
      <div className="ai-chat-body" style={{ flex: 1, padding: "15px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "10px", background: "var(--bg)" }}>
        {messages.map((m, i) => (
          <div key={i} className={`ai-message ${m.role}`}>
            <div className={`ai-bubble ${m.role === 'assistant' ? 'assistant-bubble' : 'user-bubble'}`} 
                 style={{ 
                   background: m.role === 'user' ? 'var(--primary)' : 'var(--surface)',
                   color: m.role === 'user' ? '#fff' : 'var(--text)',
                   borderRadius: "12px",
                   padding: "10px 14px",
                   fontSize: "0.85rem",
                   maxWidth: "85%",
                   marginLeft: m.role === 'user' ? 'auto' : 0,
                   lineHeight: "1.4",
                   border: m.role === 'assistant' ? "1px solid var(--border)" : "none"
                 }}>
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="ai-message assistant">
            <div className="ai-bubble typing" style={{ fontStyle: "italic", opacity: 0.6, fontSize: "0.85rem", color: "var(--text-muted)" }}>Analyzing...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{ padding: "10px 15px 15px", background: "var(--surface)", borderTop: "1px solid var(--border)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
           <button 
             onClick={() => setShowSuggestions(!showSuggestions)}
             style={{ background: "none", border: "none", color: "var(--primary)", fontSize: "0.75rem", fontWeight: "600", cursor: "pointer", padding: 0 }}
           >
             {showSuggestions ? "Hide Suggestions ↑" : "Show Suggestions ↓"}
           </button>
        </div>

        {showSuggestions && (
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 10 }}>
            {SUGGESTIONS.map(s => (
              <button 
                key={s} 
                onClick={() => handleSend(s)}
                style={{ 
                  fontSize: "0.7rem", 
                  padding: "4px 10px", 
                  borderRadius: "12px", 
                  border: "1px solid var(--border)", 
                  background: "transparent", 
                  color: "var(--text-muted)",
                  cursor: "pointer"
                }}
              >
                {s}
              </button>
            ))}
          </div>
        )}

        <div className="ai-chat-footer" style={{ display: "flex", gap: 8 }}>
          <input 
            type="text" 
            value={input} 
            onChange={(e) => setInput(e.target.value)} 
            onKeyDown={handleKeyDown}
            placeholder="Ask me anything..." 
            style={{ 
              flex: 1,
              padding: "10px 14px",
              borderRadius: "10px",
              border: "1px solid var(--border)",
              background: "var(--surface2)",
              color: "var(--text)",
              outline: "none"
            }}
          />
          <button 
            style={{ 
              borderRadius: "10px", 
              width: 40, 
              background: "var(--primary)", 
              color: "#fff", 
              border: "none",
              cursor: "pointer"
            }} 
            onClick={() => handleSend()}
          >
            →
          </button>
        </div>
      </div>
    </div>
  );
}
