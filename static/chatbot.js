function appendMessage(sender, text) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);

  msgDiv.innerHTML = marked.parse(text);

  document.getElementById("chatBox").appendChild(msgDiv);
  document.getElementById("chatBox").scrollTop = document.getElementById("chatBox").scrollHeight;
}

async function sendMessage() {
  const inputField = document.getElementById("userInput");
  const userText = inputField.value.trim();
  if (!userText) return;

  appendMessage("user", userText);
  inputField.value = "";

  appendMessage("bot", "Typing...");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText })
    });

    const data = await res.json();
    const chatBox = document.getElementById("chatBox");
    chatBox.lastChild.innerHTML = marked.parse(data.reply);

  } catch (err) {
    const chatBox = document.getElementById("chatBox");
    chatBox.lastChild.innerText = "Error contacting AI.";
  }
}

document.getElementById("userInput").addEventListener("keydown", function(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});


