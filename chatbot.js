const API_URL = "http://127.0.0.1:8000/chat";

// Session handling
let sessionId = localStorage.getItem("session_id");

if (!sessionId) {
    sessionId = "user_" + Math.random().toString(36).substring(2);
    localStorage.setItem("session_id", sessionId);
}

// Add message to chat
function addMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");

    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.innerText = message;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message
async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");

    input.value = "";
    input.style.height = "auto";  // reset textarea height

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                session_id: sessionId,
                query: message
            })
        });

        const data = await response.json();
        addMessage(data.response, "bot");

    } catch (error) {
        addMessage("Error connecting to server.", "bot");
        console.error(error);
    }
}

// Handle Enter / Shift+Enter
const input = document.getElementById("user-input");

input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-expand textarea
input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
});

// Initial bot message
window.onload = () => {
    addMessage("Hey, I'm here for you. How are you feeling today?", "bot");
};