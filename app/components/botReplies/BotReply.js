// app/components/botReplies/BotReply.js

import TextReply from "./TextReply";
import VideoReply from "./VideoReply";
import CodeReply from "./CodeReply";
import QuizReply from "./QuizReply";
import LocalVideoReply from "./LocalVideoReply";

export default function BotReply({ message }) {
  console.log("BotReply message:", message);
  const type = message.responseData.type;
  const content = message.responseData.content;

  console.log("BotReply type:", type);
  switch (type) {
    case "text":
      return <TextReply content={content} />;

    case "Manim":
      return <VideoReply url={content} />;

    case "code":
      return (
        <div>
          <CodeReply code={content} />
          <TextReply content={explanation} />
        </div>
      );

    case "quiz":
      return <QuizReply chatHistory={content} />;

    case "localVideo":
      return <LocalVideoReply filepath={content} />;

    default:
      return <div>Unknown bot reply type.</div>;
  }
}
