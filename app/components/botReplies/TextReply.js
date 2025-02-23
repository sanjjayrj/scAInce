// app/components/botReplies/TextReply.js
import styles from "./TextReply.module.css";

export default function TextReply({ content }) {
  return (
    <div className={styles.botText}>
      {content}
    </div>
  );
}
