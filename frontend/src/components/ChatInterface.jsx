import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import TypingIndicator from "./TypingIndicator";
import { Send, MoreHorizontal, Trash2, RefreshCw, LogOut } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import "./ChatInterface.css";

const ChatInterface = ({ character, onMobileMenuClick }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const dropdownRef = useRef(null);

  const { logout, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const loadConversation = async () => {
      if (character && user) {
        const storageKey = `chat_${user.id}_${character.id}`;
        const storedConvId = localStorage.getItem(storageKey);

        if (storedConvId) {
          const convId = parseInt(storedConvId);
          setConversationId(convId);

          try {
            const data = await API.chat.getConversation(convId);

            const formattedMessages = data.messages.map((msg) => ({
              id: msg.id,
              sender: msg.role === "user" ? "user" : "character",
              text: msg.content,
              timestamp: new Date(msg.timestamp).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              }),
              status: "sent",
            }));

            setMessages(formattedMessages);
          } catch (error) {
            console.error("Failed to load conversation:", error);
            if (error.message && error.message.includes("not found")) {
              localStorage.removeItem(storageKey);
              setConversationId(null);
            }
          }
        }
      }
    };

    loadConversation();
  }, [character, user]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        textareaRef.current.scrollHeight + "px";
    }
  }, [inputValue]);

  const handleSendMessage = async (e, retryMessage = null) => {
    e?.preventDefault();

    const messageText = retryMessage || inputValue.trim();
    if (!messageText) return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: messageText,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      status: "sending",
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsTyping(true);

    try {
      const response = await API.chat.sendMessage(
        character.id,
        messageText,
        conversationId
      );

      if (response.conversation_id && user) {
        setConversationId(response.conversation_id);
        const storageKey = `chat_${user.id}_${character.id}`;
        localStorage.setItem(storageKey, response.conversation_id.toString());
      }

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === userMessage.id ? { ...msg, status: "sent" } : msg
        )
      );

      const responseMessage = {
        id: Date.now() + 1,
        sender: "character",
        text: response.character_response,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        status: "sent",
        metadata: response.metadata,
      };
      setMessages((prev) => [...prev, responseMessage]);
      setIsTyping(false);
    } catch (error) {
      console.error("Error sending message:", error);

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === userMessage.id
            ? { ...msg, status: "failed", error: error.message }
            : msg
        )
      );

      setIsTyping(false);
    }
  };

  const handleRetryMessage = (message) => {
    setMessages((prev) => prev.filter((msg) => msg.id !== message.id));
    handleSendMessage(null, message.text);
  };

  const handleClearMemory = async () => {
    try {
      await API.chat.clearMemory(character.id);

      if (user) {
        const storageKey = `chat_${user.id}_${character.id}`;
        localStorage.removeItem(storageKey);
      }

      setMessages([]);
      setConversationId(null);
      setShowDropdown(false);
    } catch (error) {
      console.error("Failed to clear memory:", error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  if (!character) return null;

  return (
    <main className="chat-interface">
      <header className="chat-header-minimal">
        <div className="header-content">
          <button className="mobile-menu-trigger" onClick={onMobileMenuClick}>
            <div className="menu-dot"></div>
            <div className="menu-dot"></div>
          </button>
        </div>

        <div className="header-actions-container" ref={dropdownRef}>
          <button
            className={`header-options-btn ${showDropdown ? "active" : ""}`}
            onClick={() => setShowDropdown(!showDropdown)}
          >
            <MoreHorizontal size={20} />
          </button>

          {showDropdown && (
            <div className="dropdown-menu">
              <button
                className="dropdown-item danger"
                onClick={handleClearMemory}
              >
                <Trash2 size={16} />
                <span>Clear Memory</span>
              </button>
              <button className="dropdown-item" onClick={handleLogout}>
                <LogOut size={16} />
                <span>Log Out</span>
              </button>
            </div>
          )}
        </div>
      </header>

      <div className="chat-scroll-area no-scrollbar">
        <div className="chat-content-width">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`message-group ${
                msg.sender === "user" ? "user-group" : "char-group"
              }`}
            >
              {msg.sender === "character" && (
                <div className="message-avatar-small">
                  <img src={character.image} alt={character.name} />
                </div>
              )}
              <div
                className={`message-bubble-premium ${
                  msg.status === "sending" ? "sending" : ""
                } ${msg.status === "failed" ? "failed" : ""}`}
              >
                <div className="markdown-content">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      code({ node, inline, className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || "");
                        return !inline && match ? (
                          <SyntaxHighlighter
                            style={vscDarkPlus}
                            language={match[1]}
                            PreTag="div"
                            {...props}
                          >
                            {String(children).replace(/\n$/, "")}
                          </SyntaxHighlighter>
                        ) : (
                          <code className={className} {...props}>
                            {children}
                          </code>
                        );
                      },
                    }}
                  >
                    {msg.text}
                  </ReactMarkdown>
                </div>
                <div className="message-footer">
                  <span className="message-timestamp">{msg.timestamp}</span>
                  {msg.status === "failed" && (
                    <button
                      onClick={() => handleRetryMessage(msg)}
                      className="retry-message-btn"
                      title="Retry sending"
                    >
                      <RefreshCw size={12} />
                      Retry
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isTyping && <TypingIndicator character={character} />}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="input-wrapper-premium">
        <div className="input-glass-container">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={`Message ${character.name}...`}
            className="chat-textarea"
            rows={1}
          />

          <div className="input-actions">
            <button
              onClick={handleSendMessage}
              className={`send-btn-premium ${
                !inputValue.trim() ? "disabled" : ""
              }`}
              disabled={!inputValue.trim()}
            >
              <Send size={18} />
            </button>
          </div>
        </div>
        <div className="input-footer-text">
          Press Enter to send, Shift + Enter for new line
        </div>
      </div>
    </main>
  );
};

export default ChatInterface;
