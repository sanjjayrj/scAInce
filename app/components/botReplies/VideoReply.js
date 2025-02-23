import { useEffect, useState } from "react";
import styles from "./VideoReply.module.css";

export default function VideoReply({ url }) {
  const [videoSrc, setVideoSrc] = useState("");

  function getTailPath(filePath) {
    const parts = filePath.split("/"); // Split using "/" for UNIX paths
    const index = parts.indexOf("python"); // Find the index of "python"

    if (index !== -1) {
      return parts.slice(index).join("/"); // Return everything after "python"
    }
    console.warn("getTailPath: 'python' not found in filePath:", filePath);
    return filePath; // Return unchanged if "python" is not found
  }

  useEffect(() => {
    let blobUrl = null; // To store blob URL for cleanup

    if (url.startsWith("/")) {
      const modUrl = getTailPath(url);

      fetch(modUrl)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Failed to fetch video: ${response.statusText}`);
          }
          return response.blob();
        })
        .then((blob) => {
          blobUrl = URL.createObjectURL(blob);
          setVideoSrc(blobUrl);
        })
        .catch((error) => console.error("Error loading video:", error));
    } else {
      setVideoSrc(url);
    }

    return () => {
      if (blobUrl) {
        URL.revokeObjectURL(blobUrl); // Cleanup blob URL to prevent memory leaks
      }
    };
  }, [url]);

  return (
    <div className={styles.videoContainer}>
      {videoSrc ? (
        <video className={styles.videoFrame} controls>
          <source src={videoSrc} type="video/mp4" />
          <source src={videoSrc} type="video/webm" />
          <p>Your browser does not support the video tag.</p>
        </video>
      ) : (
        <p>Loading video...</p>
      )}
    </div>
  );
}
