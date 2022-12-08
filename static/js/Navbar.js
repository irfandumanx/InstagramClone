const user = document.querySelector("#user");
const dropdown = document.querySelector("#dropdown-wrapper");
const chatIcon = document.querySelector(".fa-comments");
let isOpen = false;

chatIcon.onclick = function () {
    location.href = "http://127.0.0.1:8080/chat";
}

document.addEventListener("click", function (event) {
    if(event.target.id === "user") {
        isOpen = !isOpen;
        dropdown.style.display = isOpen ? "flex" : "none";
    } else {
        if (isOpen) {
            dropdown.style.display = "none";
            isOpen = !isOpen;
        }
    }
});