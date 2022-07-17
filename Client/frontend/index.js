import "./src/bootstrap/css/bootstrap.css";
import "./index.css"

// Get ID app and create home page html
const idApp = document.getElementById("app");
idApp.innerHTML = `
<div class="container">
<!-- Login button center -->
<center>
    <button type="button" id="login-button" onclick="gotoLogin()">Login</button>
</center>
</div>
`;

window.gotoLogin = function() {
    runtime.WindowSetSize(600, 400);
    window.location.href = "./src/login.html";
}