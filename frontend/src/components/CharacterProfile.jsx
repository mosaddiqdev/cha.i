import React from "react";
import { ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";
import "./CharacterProfile.css";

const CharacterProfile = ({ character }) => {
  if (!character) return null;

  return (
    <aside className="character-profile">
      <div className="profile-header">
        <Link to="/" className="back-link hover-opacity">
          <ArrowLeft size={20} />
          <span>Back</span>
        </Link>
      </div>

      <div className="profile-content no-scrollbar">
        <div className="profile-image-container">
          <img
            src={character.image}
            alt={character.name}
            className="profile-image"
          />
          <div className="profile-gradient"></div>
        </div>

        <div className="profile-identity">
          <h1 className="profile-name">{character.name}</h1>
          <p className="profile-title">{character.title}</p>
          <p className="profile-desc">{character.description}</p>
        </div>

        <div className="profile-details">
          <div className="detail-section">
            <h3 className="detail-label">Personality</h3>
            <p className="detail-text">{character.personality}</p>
          </div>

          <div className="detail-section">
            <h3 className="detail-label">Expertise</h3>
            <p className="detail-text">{character.domain}</p>
          </div>

          <div className="detail-section">
            <h3 className="detail-label">I can help with...</h3>
            <ul className="use-case-list">
              {character.useCases.map((useCase, index) => (
                <li key={index} className="use-case-item">
                  {useCase}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default CharacterProfile;
