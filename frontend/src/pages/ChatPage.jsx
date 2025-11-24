import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import API from "../services/api";
import CharacterProfile from "../components/CharacterProfile";
import ChatInterface from "../components/ChatInterface";
import ErrorBoundary from "../components/ErrorBoundary";
import Preloader from "../components/Preloader";
import "./ChatPage.css";

const ChatPage = () => {
  const { id } = useParams();
  const [character, setCharacter] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isMobileProfileOpen, setIsMobileProfileOpen] = useState(false);

  useEffect(() => {
    const fetchCharacter = async () => {
      try {
        const data = await API.characters.getById(id);
        setCharacter(data);
      } catch (error) {
        console.error("Failed to fetch character:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCharacter();
  }, [id]);

  const toggleMobileProfile = () => {
    setIsMobileProfileOpen(!isMobileProfileOpen);
  };

  const closeMobileProfile = () => {
    setIsMobileProfileOpen(false);
  };

  if (loading) return <Preloader />;
  if (!character)
    return <div className="error-screen">Character not found</div>;

  return (
    <div className="chat-page-container">
      {/* Overlay for mobile to close profile */}
      <div
        className={`profile-overlay ${isMobileProfileOpen ? "open" : ""}`}
        onClick={closeMobileProfile}
      ></div>

      {/* Left Panel: Character Profile */}
      <div className={`profile-wrapper ${isMobileProfileOpen ? "open" : ""}`}>
        <CharacterProfile character={character} />
      </div>

      {/* Main Panel: Chat Interface */}
      <div className="chat-interface-wrapper">
        <ErrorBoundary>
          <ChatInterface
            character={character}
            onMobileMenuClick={toggleMobileProfile}
          />
        </ErrorBoundary>
      </div>
    </div>
  );
};

export default ChatPage;
