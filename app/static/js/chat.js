document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const recipientId = "{{ recipient.id }}";

    function fetchMessages() {
        fetch(`/get_messages/${recipientId}`)
            .then(response => response.json())
            .then(messages => {
                chatBox.innerHTML = '';
                messages.forEach(msg => {
                    const messageElement = document.createElement('div');
                    messageElement.className = msg.sender ? 'sent' : 'received';
                    messageElement.innerHTML = `<p>${msg.content}</p><span>${msg.timestamp}</span>`;
                    chatBox.appendChild(messageElement);
                });
            });
    }

    setInterval(fetchMessages, 2000);
});

document.addEventListener("DOMContentLoaded", function() {
    // Example: Auto-scroll to the bottom of the chat
    const chatBox = document.querySelector('#chat-box');
    if(chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Example: Send message functionality
    const messageForm = document.querySelector('form');
    if(messageForm) {
        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const messageInput = document.querySelector('#message');
            const message = messageInput.value;

            if(message.trim() !== "") {
                // Append message to chat box
                const messageElement = document.createElement('p');
                messageElement.innerHTML = `<strong>You:</strong> ${message}`;
                chatBox.appendChild(messageElement);

                // Clear input field
                messageInput.value = "";

                // Auto-scroll to bottom
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        });
    }
});

