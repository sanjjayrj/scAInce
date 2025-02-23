import ChatBox from "./components/ChatBox";
import logo from './logo.png';
import Image from 'next/image';

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-200 to-blue-400 py-8 px-4">
      <Image
        src={logo}
        alt="Chatbot Logo"
        width={256}
        height={150}
        className="my-4"
      />
      <div className="w-full max-w-[1000px] h-[85vh] flex-shrink-0">
        <ChatBox />
      </div>
    </main>
  );
}