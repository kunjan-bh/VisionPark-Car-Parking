// Function to load the chatbot HTML dynamically
async function loadChatbot() {
    const response = await fetch("chatbot");
    const chatbotHTML = await response.text();
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);
  
    // Add message sending functionality
    document.getElementById("send-btn").addEventListener("click", sendMessage);
    document.getElementById("user-input").addEventListener("keydown", function(event) {
      if (event.key === "Enter") sendMessage();
    });
  }
  
  // Function to send user input and get the bot response
  async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();
    if (message === "") return;
  
    // Add the user message to the chatbox
    addMessageToChatBox(message, "user");
    userInput.value = "";
  
    // Send the user message to the server and fetch bot response
    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
  
      const data = await response.json();
      addMessageToChatBox(data.response, "bot");
    } catch (error) {
      console.error("Error:", error);
      addMessageToChatBox("Something went wrong, try again later.", "bot");
    }
  }
  
  // Function to add message to the chat box
  function addMessageToChatBox(message, sender) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto scroll to the latest message
  }

  function toggleChatbot() {
    const chatContainer = document.getElementById("chat-container");
    const toggleBtn = document.getElementById("chatbot-toggle-btn");
  
    if (chatContainer.style.display === "none" || !chatContainer.style.display) {
      chatContainer.style.display = "flex";
      toggleBtn.style.display = "none"; // Hide the toggle button when the chat is open
    } else {
      chatContainer.style.display = "none";
      toggleBtn.style.display = "block"; // Show the toggle button when the chat is closed
    }
  }
  
  // Load chatbot when the page is fully loaded
  document.addEventListener("DOMContentLoaded", loadChatbot);
  