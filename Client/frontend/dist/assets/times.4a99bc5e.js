import"./bootstrap.aa1d4188.js";/* empty css               */let h=document.getElementById("start-datetime"),y=document.getElementById("end-datetime");h.innerHTML=`
<div class="form-group">
  <label for="start-year">Year</label>
  <select class="form-control" id="start-year">
    <option>2022</option>
    <option>2023</option>
    <option>2024</option>
  </select>
</div>
<div class="form-group">
    <label for="start-month">Month</label>
    <select class="form-control" id="start-month">
        <!-- Add months to dropdown -->
    </select>
    </div>
<div class="form-group">
    <label for="start-day">Day</label>
    <select class="form-control" id="start-day">
        <!-- Add days to dropdown -->
    </select>
    </div>
<div class="form-group">
    <label for="start-hour">Hour</label>
    <select class="form-control" id="start-hour">
        <!-- Add hours to dropdown -->
    </select>
    </div>
<div class="form-group">
    <label for="start-minute">Minute</label>
    <select class="form-control" id="start-minute">
        <!-- Add minutes to dropdown -->
    </select>
    </div>`;y.innerHTML=`
<div class="form-group">
  <label for="end-year">Year</label>
  <select class="form-control" id="end-year">
    <option>2022</option>
    <option>2023</option>
    <option>2024</option>
  </select>
</div>
<div class="form-group">
    <label for="end-month">Month</label>
    <select class="form-control" id="end-month">
        <!-- Add months to dropdown -->
    </select>
    </div>
<div class="form-group">
    <label for="end-day">Day</label>
    <select class="form-control" id="end-day">
        <!-- Add days to dropdown -->
    </select>
    </div>
<div class="form-group">
    <label for="end-hour">Hour</label>
    <select class="form-control" id="end-hour">
        <!-- Add hours to dropdown -->
    </select>
    </div>
<div class="form-group">
    <label for="end-minute">Minute</label>
    <select class="form-control" id="end-minute">
        <!-- Add minutes to dropdown -->
    </select>
    </div>`;for(let t=1;t<=12;t++){let e=document.createElement("option");e.value=t,e.innerHTML=t,document.getElementById("start-month").appendChild(e),document.getElementById("end-month").appendChild(e.cloneNode(!0))}for(let t=1;t<=31;t++){let e=document.createElement("option");e.value=t,e.innerHTML=t,document.getElementById("start-day").appendChild(e),document.getElementById("end-day").appendChild(e.cloneNode(!0))}for(let t=0;t<=23;t++){let e=document.createElement("option");e.value=t,e.innerHTML=t,document.getElementById("start-hour").appendChild(e),document.getElementById("end-hour").appendChild(e.cloneNode(!0))}for(let t=0;t<=59;t++){let e=document.createElement("option");e.value=t,e.innerHTML=t,document.getElementById("start-minute").appendChild(e),document.getElementById("end-minute").appendChild(e.cloneNode(!0))}window.nextWindow=function(){let t=document.getElementById("start-year").value,e=document.getElementById("start-month").value,o=document.getElementById("start-day").value,n=document.getElementById("start-hour").value,s=document.getElementById("start-minute").value,c=document.getElementById("end-year").value,u=document.getElementById("end-month").value,p=document.getElementById("end-day").value,f=document.getElementById("end-hour").value,g=document.getElementById("end-minute").value,r=`${t}-${e}-${o} ${n}:${s}:00`,a=`${c}-${u}-${p} ${f}:${g}:00`,i=new Date,l=m(r),d=m(a);if(console.log(l),console.log(d),l<i){alert("Start time must be after current time");return}if(d<l){alert("End time must be after start time");return}if(d<i){alert("End time must be after current time");return}localStorage.setItem("startTime",r),localStorage.setItem("endTime",a),window.location.href="devices.html"};function m(t){if(console.log(t),!t)return null;let e=t.split("-"),o=e[2].split(" ")[1].split(":");e[2]=e[2].split(" ")[0];let n=new Date(e[0],e[1]-1,e[2],o[0],o[1],o[2]);return console.log(n),n}
