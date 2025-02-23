"use client";

import { useState, useEffect, useRef } from "react";
import BotReply from "./botReplies/BotReply"; // << NEW
import styles from "./ChatBox.module.css";
import LoadingAnimation from "./LoadingAnimation";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollTo(0, chatRef.current.scrollHeight);
  }, [messages]);

  const handleSend = async () => {
    if (isLoading || !userInput.trim()) return;

    setIsLoading(true);
    // 1. Add user's message
    const newUserMessage = { sender: "user", type: "text", content: userInput };
    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);

    // 2. Call LLM API
    try {
      const res = await fetch("/api/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chatHistory: updatedMessages, prompt: userInput })
      });

      const data = await res.json();
      // data => { sender: 'bot', type: 'video', content: '...' } for example

      setMessages((prev) => [...prev, { sender: "bot", ...data }]);
      setIsLoading(false);

    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", type: "text", content: "Error fetching response." }
      ]);
    }

    // Clear input
    setUserInput("");
  };

  const handleStartQuiz = () => {
    if (messages.length === 0) return;

    const quizMessage = {
      sender: "bot",
      type: "quiz",
      content: messages,
    };
    console.log("Quiz message:", quizMessage);

    setMessages((prev) => [...prev, quizMessage]);
  };

  return (
    <div className={styles.chatContainer}>
      {/* Chat Window */}
      <div ref={chatRef} className={styles.chatMessages}>
        {messages.map((msg, idx) => {
          if (msg.sender === "user") {
            // User message styling
            return (
              <div
                key={idx}
                className={`${styles.message} ${styles.userMessage}`}
              >
                {msg.content}
              </div>
            );
          } else if (msg.sender === "bot") {
            console.log("Bot message:", msg, idx);
            // Bot message => Let BotReply handle it
            return (
              <BotReply key={idx} message={msg} />
            );
          } else {
            // Fallback
            return <div key={idx}>Unknown sender: {msg.sender}</div>;
          }
        })}
        {isLoading && <LoadingAnimation />}
      </div>

      {/* Input Box (Sticky) */}
      <div className={styles.inputContainer}>
        <input
          type="text"
          className={styles.inputBox}
          placeholder="Type your message..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button className={styles.sendButton} onClick={handleSend}>
          Send
        </button>

        <button
          className={styles.quizButton}
          onClick={handleStartQuiz}
          disabled={messages.length === 0}
          title={
            messages.length === 0
              ? "You need some chat history before starting a quiz"
              : "Start Quiz"
          }
        >
          Start Quiz
        </button>
      </div>
    </div>
  );
}
