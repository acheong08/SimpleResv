import "../bootstrap/css/bootstrap.css";
import "../css/styles.css";
import "../css/login.css";

import { Login } from "../../wailsjs/go/main/App";

// Make login form
document.querySelector("#login").innerHTML = `
<div class="container">
    <input type="text" id="username" placeholder="Username" required autofocus><br>
    <input type="password" id="password" placeholder="Password" required><br>
    <button class="btn btn-lg btn-secondary btn-block" type="submit" onclick="login()">Sign in</button>
</div>
`;

window.login = function () {
  // Get username and password
  let usernameElement = document.getElementById("username");
  let passwordElement = document.getElementById("password");
  let username = usernameElement.value;
  let password = passwordElement.value;
  // Check if the input is empty
  if (username === "" || password === "") return;
  // Call App.Login(username, password)
  try {
    Login(username, password)
      .then((result) => {
        // If login is successful, show home page
        if (result) {
          // Show the home page (Log success)
          console.log("Logged in successfully");
          window.location.href = "times.html";
        }
        // If login is unsuccessful, alert the user and show the login page again
        else {
          console.error(result);
          alert("Login failed");
          showLogin();
        }
      })
      .catch((err) => {
        console.error(err);
      });
  } catch (err) {
    console.error(err);
  }
};
