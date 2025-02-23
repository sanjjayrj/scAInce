import { useEffect, useState } from "react";
import styles from "./VideoReply.module.css";

export default function VideoReply({ url }) {
  const [videoSrc, setVideoSrc] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) {
      console.warn("[DEBUG] No URL provided for VideoReply.");
      return;
    }

    console.log(`[DEBUG] VideoReply component mounted. Fetching video from: ${url}`);

    let blobUrl = null;

    fetch(url)
      .then((response) => {
        console.log(`[DEBUG] Fetch request sent to: ${url}, Status: ${response.status}`);

        if (!response.ok) {
          throw new Error(`Failed to fetch video: ${response.statusText} (Status: ${response.status})`);
        }

        return response.blob();
      })
      .then((blob) => {
        blobUrl = URL.createObjectURL(blob);
        console.log(`[DEBUG] Video loaded successfully. Blob URL created: ${blobUrl}`);
        setVideoSrc(blobUrl);
      })
      .catch((err) => {
        console.error("[DEBUG] Error loading video:", err);
        setError(`Failed to load video: ${err.message}`);
      });

    // Cleanup function to revoke blob URL
    return () => {
      if (blobUrl) {
        console.log(`[DEBUG] Cleaning up blob URL: ${blobUrl}`);
        URL.revokeObjectURL(blobUrl);
      }
    };
  }, [url]);

  if (error) {
    console.warn(`[DEBUG] Video load error: ${error}`);
    return <p>{error}</p>;
  }

  return (
    <div className={styles.videoContainer}>
      {videoSrc ? (
        <video className={styles.videoFrame} controls>
          <source src={videoSrc} type="video/mp4" />
          <p>Your browser does not support the video tag.</p>
        </video>
      ) : (
        <p>[DEBUG] Loading video from {url}...</p>
      )}
    </div>
  );
}
