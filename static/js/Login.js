document.onreadystatechange = function () {
    document.readyState == "complete" ? console.log("Login sayfasi yuklendi.") : null;
}

const regex = new RegExp( "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)");

document.addEventListener('DOMContentLoaded', function (event) {
    const loginButton = document.querySelector("#btn-login");
    const usernameOrEmail = document.querySelector("#username_or_email");
    const password = document.querySelector("#password");
    const errorMessage = document.querySelector("#error-message");


    function loginRequest() {
        let isEmail = false;
        if (usernameOrEmail.value.match(regex) !== null) isEmail = true;
        fetch('/login', {
            headers : {
                'Content-Type' : 'application/json'
            },
            method : 'POST',
            body : JSON.stringify( {
                username : usernameOrEmail.value,
                password: password.value,
                isEmail : isEmail
            })
        }) //fetchin sonu
        .then(function (response){
            if(response.ok) {
                response.json()
                .then(function(response) {
                    if(response.url != null) window.location.replace(response.url);
                    if (response.errorMessage != null) {
                        errorMessage.innerHTML = response.errorMessage;
                        errorMessage.style.display = "block";
                    }else errorMessage.style.display = "none";
                });
            }
            else {
                console.log("response not ok");
                errorMessage.innerHTML = "Bir hata meydana geldi tekrar deneyin";
                errorMessage.style.display = "block";
            }
        })
        .catch(function(error) {
            errorMessage.innerHTML = "Bir hata meydana geldi tekrar deneniyor";
            errorMessage.style.display = "block";
            setTimeout(() => {loginRequest();}, 2000);
        });
    }

    loginButton.addEventListener('click', (event) => {
        event.preventDefault();
        loginRequest();
    });

    document.addEventListener('keypress', (event) => {
        if (event.code === "Enter") loginButton.click();
    }, false);
});