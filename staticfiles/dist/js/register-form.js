<!--login button disabled-->
document.getElementById("register-button").disabled = true;
document.getElementById("first_name").addEventListener("input", checkForm);
document.getElementById("username").addEventListener("input", checkForm);
document.getElementById("email").addEventListener("input", checkForm);
document.getElementById("password1").addEventListener("input", checkForm);
document.getElementById("password2").addEventListener("input", checkForm);

function checkForm() {
    var first_name = document.getElementById("first_name").value;
    var username =  document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password1 = document.getElementById("password1").value;
    var password2 = document.getElementById("password2").value;
    if (first_name.length > 0
        && username.length > 0
        && email.length > 0
        && password1.length > 0
        && password2.length > 0) {
        document.getElementById("register-button").disabled = false;
    } else {
        document.getElementById("register-button").disabled = true;
    }
}