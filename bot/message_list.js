import React from "react";

const MessageList = ({ messages, lightMode }) => {
  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`message-line ${message.type}-text`}
        >
          <div
            className={`message-box ${message.type}-text ${
              !lightMode ? "dark" : ""
            }`}
          >
            <div className={message.type === "user" ? "me" : "bot"}>
              {message.text}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;
