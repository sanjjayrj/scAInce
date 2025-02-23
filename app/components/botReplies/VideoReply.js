// app/components/botReplies/VideoReply.js
import styles from "./VideoReply.module.css";

export default function VideoReply({ url }) {
  return (
    <div className={styles.videoContainer}>
      <iframe
        className={styles.videoFrame}
        src={url}
        title="Video from AI"
        frameBorder="0"
        allowFullScreen
      />
    </div>
  );
}
