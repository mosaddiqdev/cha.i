import { useRef, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../services/api";
import { MessageCircle } from "lucide-react";
import "./Home.css";
import HomeSkeleton from "../components/HomeSkeleton";
import Logo from "../components/Logo";
import ScrollIndicator from "../components/ScrollIndicator";

const Home = () => {
  const scrollRef = useRef(null);
  const scrollTimeout = useRef(null);
  const [characters, setCharacters] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchCharacters = async () => {
      try {
        const data = await API.characters.getAll();
        setCharacters(data);
      } catch (error) {
        console.error("Failed to fetch characters:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCharacters();
  }, []);

  const extendedCharacters =
    characters.length > 0
      ? [...characters.slice(-2), ...characters, ...characters.slice(0, 2)]
      : [];

  useEffect(() => {
    if (scrollRef.current && characters.length > 0) {
      const width = scrollRef.current.clientWidth;
      scrollRef.current.scrollLeft = width * 2;
    }
  }, [characters]);

  const handleScroll = () => {
    if (!scrollRef.current) return;
    if (scrollTimeout.current) {
      clearTimeout(scrollTimeout.current);
    }
    scrollTimeout.current = setTimeout(() => {
      checkScrollPosition();
    }, 150);
  };

  const checkScrollPosition = () => {
    if (!scrollRef.current) return;

    const { scrollLeft, clientWidth } = scrollRef.current;
    const realItemsCount = characters.length;
    const itemWidth = clientWidth;

    const currentIndex = Math.round(scrollLeft / itemWidth);

    if (currentIndex < 2) {
      const newScrollLeft = (currentIndex + realItemsCount) * itemWidth;
      scrollRef.current.style.scrollBehavior = "auto";
      scrollRef.current.scrollLeft = newScrollLeft;
      scrollRef.current.style.scrollBehavior = "";
    } else if (currentIndex >= 2 + realItemsCount) {
      const newScrollLeft = (currentIndex - realItemsCount) * itemWidth;
      scrollRef.current.style.scrollBehavior = "auto";
      scrollRef.current.scrollLeft = newScrollLeft;
      scrollRef.current.style.scrollBehavior = "";
    }
  };

  return (
    <div className="home-container">
      {isLoading ? (
        <HomeSkeleton />
      ) : (
        <>
          <header className="fixed-header">
            <Logo />
          </header>

          <div
            className="horizontal-scroll-wrapper no-scrollbar"
            ref={scrollRef}
            onScroll={handleScroll}
          >
            {extendedCharacters.map((char, index) => (
              <section
                key={`${char.id}-${index}`}
                className="character-section"
              >
                <div className="character-content">
                  <div className="text-content">
                    <h2 className="char-name">{char.name}</h2>
                    <p className="char-title text-accent">{char.title}</p>
                    <p className="char-desc text-secondary">
                      {char.description}
                    </p>

                    <Link
                      to={`/chat/${char.id}`}
                      className="talk-button hover-opacity"
                    >
                      <MessageCircle size={20} />
                      <span>Talk to {char.name}</span>
                    </Link>
                  </div>

                  <div className="image-content">
                    <div className="image-wrapper">
                      <img
                        src={char.image}
                        alt={char.name}
                        className="char-portrait no-select"
                        draggable="false"
                      />
                      <div className="gradient-overlay"></div>
                    </div>
                  </div>
                </div>
              </section>
            ))}
          </div>
          <ScrollIndicator
            scrollRef={scrollRef}
            totalItems={characters.length}
          />
        </>
      )}
    </div>
  );
};

export default Home;
