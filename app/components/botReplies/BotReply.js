// app/components/botReplies/BotReply.js

import TextReply from "./TextReply";
import VideoReply from "./VideoReply";
import CodeReply from "./CodeReply";
import QuizReply from "./QuizReply";
import LocalVideoReply from "./LocalVideoReply";

export default function BotReply({ message }) {
  console.log("BotReply message:", message);

  switch (message.type) {
    case "text":
      return <TextReply content={message.content} />;

    case "video":
      return <VideoReply url={message.content} />;

    case "code":
      return (
        <div>
          <CodeReply code={message.content} />
          <TextReply content={message.explanation} />
        </div>
      );

    case "quiz":
      return <QuizReply chatHistory={message.content} />;

    case "localVideo":
      return <LocalVideoReply filepath={message.content} />;

    default:
      return <div>Unknown bot reply type.</div>;
  }
}
