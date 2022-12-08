const userImage = document.querySelector("#user");
const file = document.querySelector("#file");
const postUploadButton = document.querySelector(".fa-plus-square");
const postUpload = document.querySelector("#drop-area");
let isPostUploadOpen = false;
let fileData;
let uploadType = "";

const changeProfilePhoto = () => {
  getBase64(fileData).then(function (data) {
    userImage.style.backgroundImage = 'url('+ data +')';
  });

}

file.onchange = function () { //suruklenme disinda tiklayip secerse null gitmemesi icin

    fileData = this.files[0];
}

document.querySelector('#uploadButton').addEventListener('click', event => {
    postUpload.style.display = "none";
    let formData = new FormData();
    let request = new XMLHttpRequest();

    request.onreadystatechange = function() {if (request.readyState == 4 && request.status == 204) location.reload();};

    let url = "";
    if (uploadType === "Profil Fotografi") {
        let type = fileData.type.split("/");
        if(type[1] === "jpg" || type[1] === "png" || type[1] === "jpeg") changeProfilePhoto();
        url = "/uploadprofilephoto";
    }
    else if(uploadType === "Post Fotografi") {
        url = "/postupload";
    }
    else if(uploadType === "Video") {
        url = "/videoupload";
    }
    formData.append("file", fileData);
    request.open("POST", url);
    request.send(formData);
});

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

postUploadButton.addEventListener("click", function (event) {
  isPostUploadOpen = !isPostUploadOpen;
  postUpload.style.display = isPostUploadOpen ? "block" : "none";
});

let postID;
document.querySelectorAll("#like, #unlike").forEach((element) => {
    element.addEventListener("click", (event) => {
        let element = event.target;
        while (element.className !== "post") element = element.parentElement;
        postID = element.getAttribute("data-id");
        fetch("/photo/" + postID + "/like-action", {
            headers : {
                'Content-Type' : 'application/json'
            },
            method : 'POST'
        }) //fetchin sonu
        .then(function (response){
            if(response.ok) {
                response.json()
                .then(function(response) {
                    let likeButton = document.querySelector(`[data-id="${postID}"] > #action > #like`);
                    let unlikeButton = document.querySelector(`[data-id="${postID}"] > #action > #unlike`);
                    let likes = document.querySelector(`[data-id="${postID}"] > #likes`);
                    if (response.like) {
                        unlikeButton.classList.remove("hidden");
                        likeButton.classList.add("hidden");
                    }else {
                        likeButton.classList.remove("hidden");
                        unlikeButton.classList.add("hidden");
                    }
                    if(response.likeCount !== 0) likes.innerHTML = response.likeCount + " begenme";
                    else likes.innerHTML = "";
                });
            }
            else {
                console.log("response not ok");
            }
        })
        .catch(function(error) {
          console.log(error.message);
        });
    });
});

let dropArea = document.querySelector("#drop-area");
let plusIcon = document.querySelector(".fa-upload");
let typeButtons = document.querySelectorAll(".button");
let photoText = document.querySelector(".photo-text");

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults (e) {
    e.preventDefault();
    e.stopPropagation();
}

;['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
})


//drag
dropArea.addEventListener("dragleave", unhighlight, false);


dropArea.addEventListener('drop', handleDrop, false);
function handleDrop(event) {
  let dt = event.dataTransfer;
  fileData = dt.files[0];
}



function highlight() {
    dropArea.classList.add('highlight');
    plusIcon.classList.remove("fa-upload");
    plusIcon.classList.add("fa-check");
}

function unhighlight() {
    dropArea.classList.remove('highlight')
    plusIcon.classList.add("fa-upload");
    plusIcon.classList.remove("fa-check");

}

typeButtons.forEach((element) => {
    if(element.id === "uploadButton") return;
    element.addEventListener('click', function(event) {
        typeButtons.forEach((element) => {
            if(event.target === element) return;
            if(element.classList.contains("highlight")) element.classList.remove("highlight");
        });
        uploadType = event.target.textContent;
        event.target.classList.add("highlight");
        photoText.textContent =  "Tur secildi : " + event.target.textContent;
    });
});

document.querySelectorAll(".fa-play").forEach((element) => {
    element.addEventListener("click", () => {
        let isVideoOpen = false;
        const video = document.createElement("video");
        video.id = "post-video";
        while (element.className !== "post") element = element.parentElement;
        postID = element.getAttribute("data-id");
        element.replaceChild(video, element.children[1]);
        video.src = "/video/" + postID;
        video.play().then(r => {
            video.addEventListener('click', () => {
                if (isVideoOpen) video.pause();
                else video.play().then(r => {});
                isVideoOpen = !isVideoOpen
            });
        });
        isVideoOpen = true;
    });
});
