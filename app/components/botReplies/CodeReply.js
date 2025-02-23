// app/components/botReplies/CodeReply.js
import CodeSandbox from "../CodeSandbox";
import styles from "./CodeReply.module.css";

export default function CodeReply({ code }) {
  return (
    <div className={styles.codeReply}>
      <CodeSandbox code={code} />
    </div>
  );
}
