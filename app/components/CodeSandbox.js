"use client";

import { Sandpack } from "@codesandbox/sandpack-react";

export default function CodeSandbox({ code }) {
  return (
    <Sandpack
      template="vanilla"
      theme="light"
      files={{
        "/index.html": code.html || "<h1>Hello from AI</h1>",
        "/index.js": code.js || "console.log('AI-generated code running');",
        "/index.css": code.css || "h1 { color: blue; text-align: center; }"
      }}
      options={{
        showNavigator: false,
        showLineNumbers: true,
        editorHeight: 300,
        showConsole: false,
        showTabs: false,
        editorWidthPercentage: 0
      }}
    />
  );
}

