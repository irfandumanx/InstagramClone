const sendMessageButton = document.querySelector(".send-message");
const messageInput = document.querySelector(".message-input");
const voiceCallIcon = document.querySelector(".voice-call");
const chatID = location.pathname.split('/')[2];

messageInput.setAttribute("style", "height:" + messageInput.scrollHeight)
function textAreaAdjust(element) {
  element.style.height = (element.scrollHeight) + "px";
}
sendMessageButton.onclick = function () {
    if (messageInput.value === "") return;
    const chatElement =  document.querySelector('[chat-id="' + chatID +'"]');

    if(chatID in mapPeers) mapPeers[chatID][1].send(messageInput.value)
    let formData = new FormData();
    let request = new XMLHttpRequest();
    formData.append("message", messageInput.value);
    request.open("POST", location.href);
    request.send(formData);

    const messageDiv = document.createElement("div");
    const messageContainer = document.createElement("div");
    const messageContent = document.createElement("span");
    messageContent.classList.add("message-content");
    messageContainer.classList.add("message-container");
    messageContainer.classList.add("my");
    messageDiv.classList.add("message");
    messageContent.innerText = messageInput.value;
    messageContainer.appendChild(messageContent);
    messageDiv.appendChild(messageContainer);
    messageArea.appendChild(messageDiv);
    chatElement.querySelector('.lastMessage').innerText = messageInput.value;
    chatElement.querySelector('.time-out').innerText = "· Şimdi";
    messageInput.value = "";
}

voiceCallIcon.onclick = function (event) {
    if (document.querySelector(".call") !== null) return;
    websocket.send(JSON.stringify(
    {
            "me": {
                "user_id": user_,
                "chat_id": chatID,
                "type": "call-open"
            }
        }
    ));
    callCreate("my-call", chatID);
}