import"./bootstrap.aa1d4188.js";/* empty css               */import{L as i}from"./App.572138ff.js";document.querySelector("#login").innerHTML=`
<div class="container">
    <input type="text" id="username" placeholder="Username" required autofocus><br>
    <input type="password" id="password" placeholder="Password" required><br>
    <button class="btn btn-lg btn-secondary btn-block" type="submit" onclick="login()">Sign in</button>
</div>
`;window.login=function(){let t=document.getElementById("username"),n=document.getElementById("password"),r=t.value,o=n.value;if(!(r===""||o===""))try{i(r,o).then(e=>{e?(console.log("Logged in successfully"),window.location.href="times.html"):(console.error(e),alert("Login failed"),showLogin())}).catch(e=>{console.error(e)})}catch(e){console.error(e)}};
