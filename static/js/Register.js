document.onreadystatechange = function () {
    document.readyState == "complete" ? console.log("Register sayfasi yuklendi.") : null;
}

document.addEventListener('DOMContentLoaded', function (event) {
    const loginButton = document.querySelector("#btn-login");
    const email = document.querySelector("#mail");
    const name = document.querySelector("#name");
    const username = document.querySelector("#username");
    const password = document.querySelector("#password");
    const errorMessage = document.querySelector("#error-message");

    function registerRequest() {
        fetch('/register', {
            headers : {
                'Content-Type' : 'application/json'
            },
            method : 'POST',
            body : JSON.stringify( {
                'email' : email.value,
                'username' : username.value,
                'name': name.value,
                password: password.value
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
            setTimeout(() => {registerRequest();}, 2000);
        });
    }

    loginButton.addEventListener('click', (event) => {
        event.preventDefault();
        registerRequest();
    });
});