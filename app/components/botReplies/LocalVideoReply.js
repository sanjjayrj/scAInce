// app/components/botReplies/LocalVideoReply.js

import React from 'react';
import styles from "./LocalVideoReply.module.css";

export default function LocalVideoReply({ filepath }) {
  return (
    <div className={styles.localVideoReply}>
      <video controls style={{ width: "100%" }}>
        <source src={filepath} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
