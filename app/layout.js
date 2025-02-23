import "./globals.css";

export const metadata = {
  title: "Chatbot",
  description: "A chatbot with CSS Modules & sandboxed code execution."
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
