import "./TypingIndicator.css";

const TypingIndicator = ({ character }) => {
  return (
    <div className="typing-indicator-container">
      {character && (
        <div className="typing-avatar">
          <img src={character.image} alt={character.name} />
        </div>
      )}
      <div className="typing-bubble">
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
      </div>
    </div>
  );
};

export default TypingIndicator;
