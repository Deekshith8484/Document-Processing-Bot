import React, { useState } from "react";
import MessageInput from "./MessageInput";
import FileUpload from "./FileUpload";

const Chatbot = ({ lightMode }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (userMessage) => {
    setLoading(true);
    let response = await fetch("/process-document", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({ query: userMessage }),
    });
    response = await response.json();
    setMessages([...messages, { type: "user", text: userMessage }, { type: "bot", text: response.summary }]);
    setLoading(false);
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append("document", file);

    let response = await fetch("/process-document", {
      method: "POST",
      body: formData,
    });
    response = await response.json();
    setMessages([
      ...messages,
      { type: "bot", text: `Summary: ${response.summary}` },
      { type: "bot", text: `Effective Date: ${response.effective_date}` },
    ]);
  };

  return (
    <div className="chatbot">
      <FileUpload onFileUpload={handleFileUpload} />
      <MessageInput onSendMessage={handleSendMessage} />
      {loading && <div className="loading">Bot is processing...</div>}
      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message-box ${msg.type === "user" ? "user-text" : "bot-text"}`}>
            {msg.text}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chatbot;
