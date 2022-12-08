const newMessage = document.querySelector(".fa-pencil-square-o");
const leftSide = document.querySelector(".left");
const messageArea = document.querySelector(".message-area");

const remoteVideo = document.querySelector('#remoteVideo');
window.localStream_ = null;
let remoteStream;
let animationCallText;

function addChat(chatID, profileImage, username) {
    let contentDiv = document.createElement("div");
    contentDiv.classList.add("content");
    contentDiv.onclick = function () {
        messagePage(this);
    }
    contentDiv.setAttribute("chat-id", chatID);
    contentDiv.innerHTML = `
        <div class="flex-r">
            <div class="photo" style='background-image: url(${profileImage})'></div>
            <div class="flex-c">
                <span class="name">${username}</span>
                <div class="message-container">
                    <div class="lastMessage"></div>
                    <span class="time-out"></span>
                </div>
            </div>
        </div>
    `

    leftSide.insertBefore(contentDiv, leftSide.firstElementChild.nextElementSibling);
}

newMessage.onclick = function () {
    let username = prompt("Lutfen kullanici adi girin: ");
    if (username != null && username !== "") {
        let formData = new FormData();
        let request = new XMLHttpRequest();
        formData.append("username", username);
        request.open("POST", "/new-message");
        request.send(formData);

        request.onload = function () {
            let response = JSON.parse(request.response);
            let imageBase64 = "data:image/" + response["image"]["extension"] + ";base64," + response["image"]["src"]
            addChat(response["chatID"], imageBase64, response["username"]);
            websocket.send(JSON.stringify({
                "me": {
                    "user_id": user_,
                    "other_username": response["username"],
                    "chat_id": response["chatID"],
                    "type": "new-chat"
                }
            }));
            websocket.send(JSON.stringify({
                "me": {
                    "user_id": user_,
                    "chat_id": response["chatID"],
                    "type": "create_room"
                }
            }));
        }

    }
}

document.querySelectorAll(".content").forEach((element) => {
    element.onclick = function () {
        messagePage(this);
    }
});

function messagePage(element) {
    location.href = "http://127.0.0.1:8080/chat/" + element.getAttribute("chat-id");
}

/****************************************************************************
 * Websocket
 ****************************************************************************/

let loc = window.location;
let websocket;
let isInitiator;
let wsStart = loc.protocol === "https:" ? "wss://" : "ws://";
let endPoint = wsStart + "localhost:8081/";
let chats = []


websocket = new WebSocket(endPoint);
websocket.onopen = function () {
    isInitiator = true;

    websocket.send(JSON.stringify({
        "me": {
            "user_id": user_,
            "type": "socket"
        }
    }));

    document.querySelectorAll(".content").forEach(element => {
        let chatID = element.getAttribute("chat-id");
        chats.push(chatID);
        websocket.send(JSON.stringify({
            "me": {
                "user_id": user_,
                "chat_id": chatID,
                "type": "create_room"
            }
        }));
    });
}

window.addEventListener('unload', function () {
    websocket.send(JSON.stringify({
        "me": {
            "user_id": user_,
            "type": "disconnect"
        }
    }));
});

let configuration = null;

websocket.onmessage = function (message) {
    let data = JSON.parse(message.data);
    if (data.me.type === "created") {
        isInitiator = true;
    } else if (data.me.type === "joined") {
        isInitiator = false;
        createPeerConnection(data.me.chat_id, isInitiator, configuration);
    } else if (data.me.type === "ready") {
        createPeerConnection(data.me.chat_id, isInitiator, configuration);
    } else if (data.me.type === "new-chat") {
        let imageBase64 = "data:image/" + data.me.profileImage.extension + ";base64," + data.me.profileImage.src
        addChat(data.me.chat_id, imageBase64, data.me.username);
        websocket.send(JSON.stringify({
            "me": {
                "user_id": user_,
                "chat_id": data.me.chat_id,
                "type": "create_room"
            }
        }));
    } else if (data.me.type === "call-open") {
        callCreate("call-open", data.me.chat_id);
    } else if (data.me.type === "call-answered") {
        navigator.mediaDevices.getUserMedia({
            audio: true,
            video: false
        })
            .then(gotStream)
            .catch(function (e) {
                alert('getUserMedia() error: ' + e.name);
            });

        function gotStream(stream) {
            window.localStream_ = stream;
            websocket.send(JSON.stringify({
                    "me": {
                        "user_id": user_,
                        "type": "disconnect"
                    }
                }));
            chatDisconnect(chatID);
            clearInterval(animationCallText);
            document.querySelector(".call-message").innerText = "Cevap verdi";
        }
    } else if (data.me.type === "disconnect") {
        chatDisconnect(data.me.chat_id);
    } else if (data.rtc.type === 'offer') {
        peerConn.setRemoteDescription(new RTCSessionDescription(data.rtc), function () {
            },
            logError);
        peerConn.createAnswer().then((answer) => onLocalSessionCreated(data.me.chat_id, answer));
    } else if (data.rtc.type === 'answer') {
        peerConn.setRemoteDescription(new RTCSessionDescription(data.rtc), function () {
            },
            logError);
    } else if (data.rtc.type === 'candidate') {
        if (peerConn.remoteDescription === null) return;
        peerConn.addIceCandidate(new RTCIceCandidate({
            candidate: data.rtc.candidate,
            sdpMLineIndex: data.rtc.label,
            sdpMid: data.rtc.id
        }));
    }
}

const callText = [
    "Aranıyor.",
    "Aranıyor..",
    "Aranıyor...",
    "Aranıyor...",
    "Aranıyor..",
    "Aranıyor.",
    "Aranıyor",
]

const answerText = [
    "Gelen Arama.",
    "Gelen Arama..",
    "Gelen Arama...",
    "Gelen Arama...",
    "Gelen Arama..",
    "Gelen Arama.",
    "Gelen Arama",
]

let i = 0;
const innerCall = `
    <div class="flex-r">
        <div class="call-photo"></div>
        <div class="flex-c">
            <span class="call-name"></span>
            <div class="call-container">
                <div class="call-message">Aranıyor</div>
                <span class="time-out">
                </span>
            </div>
        </div>
        <div class="phone-no">
            <i class="fa fa-phone" aria-hidden="true"></i>
        </div>
        <div class="phone-yes">
            <i class="fa fa-phone" aria-hidden="true"></i>
        </div>
    </div>
`;

function callCreate(callType, chatID) {
    const callElement = document.createElement("div");
    callElement.classList.add("call");
    callElement.innerHTML = innerCall;
    const chatElement = document.querySelector('[chat-id="' + chatID + '"]');
    callElement.querySelector(".call-name").innerText = chatElement.querySelector(".name").innerText;
    callElement.querySelector(".call-photo").style.backgroundImage = chatElement.querySelector(".photo").style.backgroundImage;
    const phoneNo = callElement.querySelector(".phone-no");
    const phoneYes = callElement.querySelector(".phone-yes");
    const textElement = callElement.querySelector(".call-message");

    if (callType === "call-open") {
        textElement.innerText = "Gelen Arama";
        phoneNo.style.marginLeft = "200px";
        phoneYes.style.display = "block";
        phoneYes.onclick = function () {
            navigator.mediaDevices.getUserMedia({
                audio: true,
                video: false
            })
                .then(gotStream)
                .catch(function (e) {
                    alert('getUserMedia() error: ' + e.name);
                });

            function gotStream(stream) {
                window.localStream_ = stream;
                websocket.send(JSON.stringify(
                    {
                        "me": {
                            "user_id": user_,
                            "chat_id": chatID,
                            "type": "call-answered"
                        }
                    }
                ));
                phoneYes.style.display = "none";
                phoneNo.style.marginLeft = "250px";
                clearInterval(animationCallText);
                textElement.innerText = "Açıldı";
            }
        }
    }

    document.querySelector("body").appendChild(callElement);
    animationCallText = setInterval(() => {
        if (callType === "call-open") {
            textElement.innerText = answerText[i];
            i = ++i % answerText.length;
        } else {
            textElement.innerText = callText[i];
            i = ++i % callText.length;
        }
    }, 500);

    phoneNo.onclick = function () {
        clearInterval(animationCallText);
        document.querySelector("body").removeChild(callElement);
        i = 0;
        websocket.send(JSON.stringify(
            {
                "me": {
                    "user_id": user_,
                    "chat_id": chatID,
                    "type": "call-close"
                }
            }
        ));
    }
}

/****************************************************************************
 * WebRTC peer connection and data channel
 ****************************************************************************/

let mapPeers = {}

function logError(err) {
    if (!err) return;
    if (typeof err === 'string') {
        console.warn(err);
    } else {
        console.warn(err.toString(), err);
    }
}


function sendMessage(chatID, message) {
    websocket.send(JSON.stringify({
        "rtc": message, "me": {
            "user_id": user_,
            "chat_id": chatID,
            "type": ""
        }
    }));
}

let peerConn;
let dataChannel;

function createPeerConnection(chatID, isInitiator, config) {
    peerConn = new RTCPeerConnection(config);
    peerConn.onaddstream = (event) => {
        console.log("on add stream girdim");
        remoteStream = event.stream;
        remoteVideo.srcObject = remoteStream;
    }
    if (window.localStream_ !== null) {
        console.log("local stream keke")
        peerConn.addStream(window.localStream_);
    }

    peerConn.onicecandidate = function (event) {
        if (event.candidate) {
            sendMessage(chatID, {
                type: 'candidate',
                label: event.candidate.sdpMLineIndex,
                id: event.candidate.sdpMid,
                candidate: event.candidate.candidate
            });
        }
    };

    if (isInitiator) {
        //peerConn.addStream(localStream);
        dataChannel = peerConn.createDataChannel('channel');
        onDataChannelCreated(chatID, peerConn, dataChannel);

        peerConn.createOffer().then(function (offer) {
            return peerConn.setLocalDescription(offer);
        })
            .then(() => sendMessage(chatID, peerConn.localDescription))
            .catch(logError);

    } else {
        peerConn.ondatachannel = function (event) {
            dataChannel = event.channel;
            onDataChannelCreated(chatID, peerConn, dataChannel);
        };
    }

}

function onLocalSessionCreated(chatID, desc) {
    peerConn.setLocalDescription(desc).then(function () {
        sendMessage(chatID, peerConn.localDescription);
    }).catch(logError);
}

function onDataChannelCreated(chatID, peerCon, channel) {
    channel.onopen = function () {
        console.log("Channel opened.");
        mapPeers[chatID] = [peerCon, channel]
    };

    channel.onclose = () => {
        console.log('Channel closed.');
        //chatDisconnect(chatID);
    }

    channel.onmessage = function (event) {
        const chatLeftElement = document.querySelector('[chat-id="' + chatID + '"]');
        chatLeftElement.querySelector(".lastMessage").innerText = event.data;
        chatLeftElement.querySelector(".time-out").innerText = "· Şimdi";
        if (messageArea !== null) {
            const messageDiv = document.createElement("div");
            const messageContainer = document.createElement("div");
            const messageContent = document.createElement("span");
            const photoDiv = document.createElement("div");
            const innerMessagePhoto = document.createElement("div");
            innerMessagePhoto.classList.add("inner-message-photo");
            photoDiv.classList.add("photoDiv");
            messageContent.classList.add("message-content");
            messageContainer.classList.add("message-container");
            messageDiv.classList.add("message");
            innerMessagePhoto.style.backgroundImage = chatLeftElement.querySelector('.photo').style.backgroundImage;
            messageContent.innerText = event.data;
            photoDiv.appendChild(innerMessagePhoto);
            messageContainer.appendChild(photoDiv);
            messageContainer.appendChild(messageContent);
            messageDiv.appendChild(messageContainer);
            messageArea.appendChild(messageDiv);
            right.scrollTo(0, right.scrollHeight);
        }
    };
}

function chatDisconnect(chatID) {
    mapPeers[chatID][0].close();
    delete mapPeers[chatID];
    websocket.send(JSON.stringify({
        "me": {
            "user_id": user_,
            "chat_id": chatID,
            "type": "create_room"
        }
    }));
}
