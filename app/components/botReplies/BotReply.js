// app/components/botReplies/BotReply.js

import TextReply from "./TextReply";
import VideoReply from "./VideoReply";
import CodeReply from "./CodeReply";
import QuizReply from "./QuizReply";
import LocalVideoReply from "./LocalVideoReply";
import YouTubeReply from "./YouTubeReply";


export default function BotReply({ message }) {
  console.log("BotReply message:", message);

  let type;
  let res;
  if (!message.responseData) {
  } else {
    type = message.responseData.type;
    res = message.responseData;
  }


  console.log("BotReply type:", type);
  switch (type) {
    case "text":
      return <TextReply content={res.content} />;

    case "Manim":
      return (
        <div>
          <VideoReply url={res.content} />
          <TextReply content={res.explanation} />
        </div>
      );

    case "code":
      return (
        <div>
          <CodeReply code={res.content} />
          <TextReply content={res.explanation} />
        </div>
      );

    case "quiz":
      return <QuizReply chatHistory={message.content} />;

    case "localVideo":
      return <LocalVideoReply filepath={res.content} />;

    case "links":
      return (
        <div>
          <YouTubeReply videoIds={res.content} />
          <TextReply content={res.explanation} />
        </div>
      )

    default:
      return <div>Unknown bot reply type.</div>;
  }
}
