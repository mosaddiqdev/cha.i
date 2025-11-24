import { useEffect, useState } from "react";
import "./ScrollIndicator.css";

const ScrollIndicator = ({ scrollRef, totalItems }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      if (!scrollRef.current) return;

      const { scrollLeft, clientWidth } = scrollRef.current;
      const itemWidth = clientWidth;
      let currentIndex = Math.round(scrollLeft / itemWidth);

      currentIndex = currentIndex - 2;

      if (currentIndex < 0) {
        currentIndex = totalItems + currentIndex;
      } else if (currentIndex >= totalItems) {
        currentIndex = currentIndex - totalItems;
      }

      setActiveIndex(currentIndex);
    };

    const scrollElement = scrollRef.current;
    if (scrollElement) {
      scrollElement.addEventListener("scroll", handleScroll);
      handleScroll();
    }

    return () => {
      if (scrollElement) {
        scrollElement.removeEventListener("scroll", handleScroll);
      }
    };
  }, [scrollRef, totalItems]);

  if (totalItems <= 1) return null;

  return (
    <div className="scroll-indicator">
      {Array.from({ length: totalItems }).map((_, index) => (
        <div
          key={index}
          className={`indicator-dot ${index === activeIndex ? "active" : ""}`}
        />
      ))}
    </div>
  );
};

export default ScrollIndicator;
