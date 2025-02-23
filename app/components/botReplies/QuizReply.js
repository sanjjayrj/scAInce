// app/components/botReplies/QuizReply.js
import { useState, useEffect } from "react";
import styles from "./QuizReply.module.css";

export default function QuizReply({ chatHistory }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Store user-selected answers: key = question index, value = selected option index
  const [answers, setAnswers] = useState({});
  // Whether the user has submitted their answers
  const [submitted, setSubmitted] = useState(false);
  // Score
  const [score, setScore] = useState(null);

  useEffect(() => {
    async function generateQuiz() {
      try {
        const response = await fetch("/api/generateQuiz", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ chatHistory }),
        });

        if (!response.ok) {
          throw new Error("Failed to generate quiz");
        }

        const data = await response.json();
        // Expecting data.questions to be an array of quiz questions
        setQuestions(data.questions);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    generateQuiz();
  }, [chatHistory]);

  const handleOptionChange = (questionIndex, optionIndex) => {
    setAnswers({ ...answers, [questionIndex]: optionIndex });
  };

  const handleSubmit = () => {
    let localScore = 0;
    questions.forEach((q, idx) => {
      if (answers[idx] === q.correctAnswerIndex) {
        localScore++;
      }
    });
    setScore(localScore);
    setSubmitted(true);
  };

  const handleRetake = () => {
    setAnswers({});
    setSubmitted(false);
    setScore(null);
  };

  if (loading) {
    return <div className={styles.quizContainer}>Loading quiz...</div>;
  }

  if (error) {
    return <div className={styles.quizContainer}>Error: {error}</div>;
  }

  return (
    <div className={styles.quizContainer}>
      <h2>MCQ Quiz</h2>

      {/* Optional: display the chat history context */}
      {chatHistory && (
        <div className={styles.chatHistoryPreview}>
          <p>Chat History for Context:</p>
          <pre>{JSON.stringify(chatHistory, null, 2)}</pre>
        </div>
      )}

      {questions.map((q, qIndex) => (
        <div key={qIndex} className={styles.questionBlock}>
          <p className={styles.question}>{q.question}</p>
          <div className={styles.options}>
            {q.options.map((opt, optIndex) => (
              <label key={optIndex}>
                <input
                  type="radio"
                  name={`question-${qIndex}`}
                  value={optIndex}
                  checked={answers[qIndex] === optIndex}
                  onChange={() => handleOptionChange(qIndex, optIndex)}
                  disabled={submitted}
                />
                {opt}
              </label>
            ))}
          </div>
        </div>
      ))}

      {!submitted && (
        <button className={styles.submitButton} onClick={handleSubmit}>
          Submit
        </button>
      )}

      {submitted && (
        <div className={styles.resultBlock}>
          <h3>
            Your Score: {score}/{questions.length}
          </h3>
          <button className={styles.retakeButton} onClick={handleRetake}>
            Retake Quiz
          </button>
        </div>
      )}
    </div>
  );
}
