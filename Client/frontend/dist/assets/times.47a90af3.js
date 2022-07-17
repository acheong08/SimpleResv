import"./bootstrap.aa1d4188.js";/* empty css               */let u=document.getElementById("start-datetime"),p=document.getElementById("end-datetime");u.innerHTML=`
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
    </div>`;p.innerHTML=`
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
    </div>`;for(let e=1;e<=12;e++){let t=document.createElement("option");t.value=e,t.innerHTML=e,document.getElementById("start-month").appendChild(t),document.getElementById("end-month").appendChild(t.cloneNode(!0))}for(let e=1;e<=31;e++){let t=document.createElement("option");t.value=e,t.innerHTML=e,document.getElementById("start-day").appendChild(t),document.getElementById("end-day").appendChild(t.cloneNode(!0))}for(let e=0;e<=23;e++){let t=document.createElement("option");t.value=e,t.innerHTML=e,document.getElementById("start-hour").appendChild(t),document.getElementById("end-hour").appendChild(t.cloneNode(!0))}for(let e=0;e<=59;e++){let t=document.createElement("option");t.value=e,t.innerHTML=e,document.getElementById("start-minute").appendChild(t),document.getElementById("end-minute").appendChild(t.cloneNode(!0))}window.nextWindow=function(){let e=document.getElementById("start-year").value,t=document.getElementById("start-month").value,o=document.getElementById("start-day").value,d=document.getElementById("start-hour").value,n=document.getElementById("start-minute").value,l=document.getElementById("end-year").value,r=document.getElementById("end-month").value,a=document.getElementById("end-day").value,m=document.getElementById("end-hour").value,i=document.getElementById("end-minute").value,s=`${e}-${t}-${o} ${d}:${n}:00`,c=`${l}-${r}-${a} ${m}:${i}:00`;localStorage.setItem("startTime",s),localStorage.setItem("endTime",c),window.location.href="devices.html"};
