const u=function(){const o=document.createElement("link").relList;if(o&&o.supports&&o.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))i(e);new MutationObserver(e=>{for(const t of e)if(t.type==="childList")for(const r of t.addedNodes)r.tagName==="LINK"&&r.rel==="modulepreload"&&i(r)}).observe(document,{childList:!0,subtree:!0});function a(e){const t={};return e.integrity&&(t.integrity=e.integrity),e.referrerpolicy&&(t.referrerPolicy=e.referrerpolicy),e.crossorigin==="use-credentials"?t.credentials="include":e.crossorigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function i(e){if(e.ep)return;e.ep=!0;const t=a(e);fetch(e.href,t)}};u();var c="/assets/logo-universal.cb3119ea.png";function s(n){return window.go.main.App.Greet(n)}document.querySelector("#app").innerHTML=`
    <img id="logo" class="logo">
      <div class="result" id="result">Please enter your name below \u{1F447}</div>
      <div class="input-box" id="input">
        <input class="input" id="name" type="text" autocomplete="off" />
        <button class="btn" onclick="greet()">Greet</button>
      </div>
    </div>
`;document.getElementById("logo").src=c;let l=document.getElementById("name");l.focus();let d=document.getElementById("result");window.greet=function(){let n=l.value;if(n!=="")try{s(n).then(o=>{d.innerText=o}).catch(o=>{console.error(o)})}catch(o){console.error(o)}};
