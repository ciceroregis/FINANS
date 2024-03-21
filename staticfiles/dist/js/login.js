//login button disabled
document.getElementById("login-button").disabled = true;
document.getElementById("username").addEventListener("input", checkForm);
document.getElementById("password").addEventListener("input", checkForm);

function checkForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if (username.length > 0 && password.length > 0) {
        document.getElementById("login-button").disabled = false;
    } else {
        document.getElementById("login-button").disabled = true;
    }
}