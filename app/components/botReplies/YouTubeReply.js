import React from "react";

function getVideoId(url) {
  // This regex extracts the video ID from common YouTube URL formats.
  const match = url.match(/(?:\?v=|\/embed\/|youtu\.be\/)([^&\n?#]+)/);
  return match ? match[1] : null;
}

export default function YouTubeReply({ videoIds }) {
  // Ensure videoIds is an array; if it's a single string, wrap it in an array.
  const ids = Array.isArray(videoIds) ? videoIds : [videoIds];
  console.log("YouTubeReply original:", videoIds, "processed:", ids);

  return (
    <div>
      {ids.map((url, index) => {
        const videoId = getVideoId(url);
        if (!videoId) {
          return (
            <div key={index}>
              <p>Invalid YouTube URL: {url}</p>
            </div>
          );
        }
        return (
          <div key={index}>
            <iframe
              width="560"
              height="315"
              src={`https://www.youtube.com/embed/${videoId}`}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              title={`YouTube video ${index + 1}`}
            ></iframe>
          </div>
        );
      })}
    </div>
  );
}
