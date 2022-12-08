const inputMap = new Map();
const closeButton = document.getElementById("close-button");
const settingsForm = document.getElementById("settings-form");
const settingsError = document.getElementById("settings-error");
const profilePhotoContainer = document.querySelector(".profile-photo");
const cancelButton = document.querySelector(".profile-photo-cancel");
const deletePhotoButton = document.querySelector(".profile-photo-delete");
const profilePhotoUpload = document.querySelector(".profile-photo-upload");
const userImage = document.querySelector("#user");
const file = document.querySelector("#file");
const profileChange = `
<div class="settings-property">
    <div class="user-container">
           <div class="user-photo" style="background-image: url('data:image/${image_.extension};base64,${image_.src}');"></div>
           <div class="user-container-inner">
               <span style="font-weight: 500; font-size: 16px" class="property-text">${user_.username}</span>
               <span id="change-profile-image">Profil fotoğrafını değiştir</span>
           </div>
        </div>
        <br>
        <div class="property-container">
            <div class="property-container-name">Adın</div>
            <div class="property-container-inner">
                <input type="text" class="property-input" id="name-input" name="name" value='${user_.name}'>
                <br>
                <span class="property-text">Adın ve soyadın, takma adın veya işletmenin adı gibi tanındığın bir adı kullanarak insanların hesabını keşfetmesine yardımcı ol.</span>
                <br>
                <span class="property-text">Adını 14 gün içinde sadece iki kez değiştirebilirsin.</span>
            </div>
        </div>
        <div class="property-container">
            <div class="property-container-name">Kullanıcı Adı</div>
            <div class="property-container-inner">
                <input type="text" class="property-input" id="username-input" name="username" value=${user_.username}>
                <br>
                <span class="property-text">Çoğu durumda, kullanıcı adını 14 gün içinde yeniden değiştirip ${user_.username} yapabileceksin.</span>
            </div>
        </div>
        <div class="property-container">
            <div class="property-container-name">Email</div>
            <div class="property-container-inner">
                <input type="text" class="property-input" id="email-input" name="email" value=${user_.email}>
            </div>
        </div>
        <div class="property-container">
            <div class="property-container-name"></div>
            <div class="property-container-inner">
                <div id="push-update-button" type="submit" class="button">Gönder</div>
           </div>
        </div>
    </div>
</div>
`;

const passwordChange = `
    <div>MOKOKO</div>
`;

file.onchange = function () {
    let fileData = this.files[0];
    let formData = new FormData();
    let request = new XMLHttpRequest();
    formData.append("file", fileData);

    request.open("POST", "/uploadprofilephoto");
    request.send(formData);

    request.onload = function () {
        getBase64(fileData).then(function (data) {
            userImage.style.backgroundImage = 'url('+ data +')';
            userSettingsImage.style.backgroundImage = 'url('+ data +')';
            cancelButton.click();
        });
    }
}

deletePhotoButton.onclick = function () {
    let request = new XMLHttpRequest();
    request.open("POST", "/removeprofilephoto");
    request.send();
    request.onload = function () {
        userImage.style.backgroundImage = 'url('+ "data:image/png;base64," + request.response +')';
        userSettingsImage.style.backgroundImage = 'url('+ "data:image/png;base64," + request.response +')';
        cancelButton.click();
    }
}


function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

let activeElement = document.getElementById("password-change");
let firstElement = document.getElementById("profile-change");
firstElement.classList.add("active");

document.querySelectorAll(".settings-property-name").forEach(element => {
    element.onclick = function (e) {
        if (activeElement.id === e.currentTarget.id) return;
        else {
            activeElement.classList.remove("active");
            activeElement = e.currentTarget;
            activeElement.classList.add("active");
        }
        switch (e.currentTarget.id) {
            case "profile-change":
                settingsForm.innerHTML = profileChange;
                break;
            case "password-change":
                settingsForm.innerHTML = passwordChange;
                break;
        }
    };
});

firstElement.click();
const pushUpdateButton = document.getElementById("push-update-button");
const nameLabel_ = document.getElementById("name-input");
const usernameLabel_ = document.getElementById("username-input");
const emailLabel_ = document.getElementById("email-input");
const userSettingsImage = document.querySelector(".user-photo");


let canShiny = false;
document.querySelectorAll(".property-input").forEach(element => {
    inputMap.set(element.id, [element.value, false]);
    element.oninput = function (e) {
        const el = inputMap.get(e.target.id);
        if(el[0] === e.target.value) {
            canShiny = false;
            inputMap.set(e.target.id, [el[0], false]);
            inputMap.forEach((v) => {
                if(v[1]) canShiny = true;
            });
        }
        else {
            canShiny = true;
            inputMap.set(e.target.id, [el[0], true]);
        }
        if(canShiny) pushUpdateButton.classList.add("highlight")
        else pushUpdateButton.classList.remove("highlight");
    }
});

pushUpdateButton.addEventListener('click', event => {
    let formData = new FormData();
    let request = new XMLHttpRequest();
    formData.append("username", usernameLabel_.value);
    formData.append("name", nameLabel_.value);
    formData.append("email", emailLabel_.value)

    request.open("POST", "/update-profile");
    request.send(formData);

    request.onload = function () {
        let response = JSON.parse(request.response);
        if (response["errorMessage"]) {
            settingsError.style.display = "block";
            settingsError.innerText = response["errorMessage"];
            location.reload();
        }else {
            settingsError.style.display = "none";
            settingsError.innerText = "";
        }
    }
});

document.getElementById("change-profile-image").onclick = () => profilePhotoContainer.style.display = "block";
cancelButton.onclick = () => document.querySelector(".profile-photo").style.display = "none";