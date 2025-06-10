 (function() {
      const chatLog = document.getElementById("chat-log");
      const userInput = document.getElementById("user-input");
      const sendBtn = document.getElementById("send-btn");

      // Helper to append a message to the chat log
      function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.style.marginBottom = "10px";

        if (sender === "user") {
          msgDiv.innerHTML = `
            <div style="text-align: right;">
              <span style="
                display: inline-block; 
                background: #007bff; 
                color: #fff; 
                padding: 8px 12px; 
                border-radius: 12px;
                max-width: 80%;
                word-wrap: break-word;
              ">
                ${text}
              </span>
            </div>`;
        } else {
          msgDiv.innerHTML = `
            <div style="text-align: left;">
              <span style="
                display: inline-block; 
                background: #e1e1e1; 
                color: #333; 
                padding: 8px 12px; 
                border-radius: 12px;
                max-width: 80%;
                word-wrap: break-word;
              ">
                ${text}
              </span>
            </div>`;
        }

        chatLog.appendChild(msgDiv);
        // Scroll to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
      }

      // Send question to Flask /chatbot
      async function sendQuestion() {
        const question = userInput.value.trim();
        if (!question) return;

        // 1) Append user's question
        appendMessage("user", question);
        userInput.value = "";
        userInput.disabled = true;
        sendBtn.disabled = true;

        // 2) Call Flask endpoint
        try {
          const resp = await fetch("/chatbot", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
          });

          if (!resp.ok) {
            throw new Error(`Server returned ${resp.status}`);
          }

          const data = await resp.json();
          // Assume Flask returns { response: "..." }
          appendMessage("bot", data.response);
        } catch (err) {
          console.error("Error calling /chatbot:", err);
          appendMessage("bot", "Sorry, something went wrong. Please try again.");
        } finally {
          userInput.disabled = false;
          sendBtn.disabled = false;
          userInput.focus();
        }
      }

      // Event listeners
      sendBtn.addEventListener("click", sendQuestion);
      userInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
          e.preventDefault();
          sendQuestion();
        }
      });
    })();