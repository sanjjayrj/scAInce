import { useState, useEffect } from "react";
import styles from "./LoadingAnimation.module.css";

export default function LoadingAnimation() {
  const messages = [
    "Hold tight, leveling up your learning! 🚀",
    "Just a sec, downloading brain fuel... 🧠",
    "Grinding on some knowledge nuggets... 📚",
    "Warming up the brain, please wait! 💡",
    "Our AI is hitting the books! 🤖📖",
    "Polishing those facts for you! ✨",
    "Calculating the secret sauce of wisdom... 🧪",
    "Fueling up on fun facts and figures... 🔢",
    "Charging your neurons with some serious info! ⚡️",
    "Please stand by, unlocking the mysteries of the universe... 🌌",
    "Connecting to the knowledge network... 🌐",
    "Hold on, the genius is booting up! 🖥️"
  ];

  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMessageIndex((prev) => (prev + 1) % messages.length);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={styles.loadingContainer}>
      <p className={styles.loadingText}>{messages[currentMessageIndex]}</p>
    </div>
  );
}
