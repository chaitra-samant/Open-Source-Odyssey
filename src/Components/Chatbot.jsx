import React, { useState } from "react";
import { MessageSquare, Minimize2, Send } from "lucide-react";


const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isMinimized, setIsMinimized] = useState(true);
  const [isLoading, setIsLoading] = useState(false);


  const handleSend = async () => {
    if (!userInput.trim()) return;
   
    // Add user message to chat
    setChatHistory((prev) => [...prev, { sender: "user", message: userInput }]);
   
    setIsLoading(true);
    try {
      // Send request to backend
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });
     
      const data = await response.json();
     
      // Add bot response to chat
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", message: data.reply },
      ]);
    } catch (error) {
      console.error('Error:', error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", message: "Sorry, I'm having trouble connecting to the server." },
      ]);
    }
   
    setIsLoading(false);
    setUserInput("");
  };


  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };


  return (
    <div
      className={`
        fixed bottom-6 right-6 z-[1000] transition-all duration-300
        ${isMinimized ? 'w-14 h-14' : 'w-96'}
      `}
    >
      {isMinimized ? (
        <div
          onClick={toggleMinimize}
          className="
            w-full h-full bg-purple-600 rounded-full flex items-center
            justify-center cursor-pointer shadow-gradient hover:bg-purple-700
            transition-colors
          "
        >
          <MessageSquare size={24} color="#fff" />
        </div>
      ) : (
        <div
          className="
            glass-effect shadow-gradient flex flex-col h-[500px]
            font-tech text-purple-blue p-3
          "
        >
          {/* Header */}
          <div className="flex justify-between items-center px-3 py-2 border-b border-purple-200">
            <h3 className="text-lg font-bold text-white">Project X Assistant</h3>
            <div
              onClick={toggleMinimize}
              className="cursor-pointer hover:bg-purple-200 rounded-full p-1"
            >
              <Minimize2 size={16} color="#6a5acd" />
            </div>
          </div>
         
          {/* Chat History */}
          <div
            className="
              flex-grow overflow-y-auto px-2 py-3 space-y-2
              scrollbar-hide
            "
          >
            {chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`
                  max-w-[80%] p-2 rounded-xl text-sm
                  ${chat.sender === 'user'
                    ? 'bg-purple-600 text-white self-end ml-auto'
                    : 'bg-white text-purple-800 border border-purple-200 self-start'}
                `}
              >
                {chat.message}
              </div>
            ))}
            {isLoading && (
              <div className="text-white text-sm self-start bg-purple-400 p-2 rounded-xl">
                Thinking...
              </div>
            )}
          </div>
         
          {/* Input Area */}
          <div className="flex p-2 space-x-2">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSend()}
              placeholder="Type your message..."
              className="
                flex-grow p-2 rounded-full bg-white/10
                border border-purple-200 text-white text-sm
                focus:outline-none focus:ring-2 focus:ring-purple-500
              "
            />
            <button
              onClick={handleSend}
              disabled={isLoading}
              className="
                bg-purple-600 text-white p-2 rounded-full
                hover:bg-purple-700 transition-colors
                flex items-center justify-center
                disabled:opacity-50 disabled:cursor-not-allowed
              "
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};


export default Chatbot;
