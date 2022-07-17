import"./bootstrap.aa1d4188.js";/* empty css               */import{D as l}from"./App.dbb98865.js";a();let r=[];function a(){let e=localStorage.getItem("startTime"),n=localStorage.getItem("endTime");l(e,n).then(i=>{console.log(i);let s=JSON.parse(i),c=document.getElementById("device-list");c.innerHTML="";for(let d=0;d<s.length;d++){let t=s[d],o=document.createElement("div");o.className="device-list-item",o.id=`device-${t.name}`,o.innerHTML=`
                <div class="card-body">
                    <h5 class="card-title">${t.name}</h5>
                    <p class="card-text">${t.description}</p>
                    <button class="btn btn-primary" onclick="reserveDevice('${t.name}')" id="button-${t.name}">Add</button>
                </div>
                `,c.appendChild(o)}}).catch(i=>{console.error(i)})}window.reserveDevice=function(e){r.push(e),document.getElementById(`button-${e}`).disabled=!0,document.getElementById(`button-${e}`).className="btn btn-secondary disabled",console.log(r),document.getElementById("submit-btn").textContent="Next ("+r.length+")"};window.makeResvRequest=function(){let e=r,n=JSON.stringify(e);console.log(n)};
