// Import bootstrap, styles, and times.css
import "../../src/bootstrap/css/bootstrap.css";
import "../css/styles.css";
import "../css/times.css";

// Get element for start and end times selectors
let startTimeSelector = document.getElementById("start-datetime");
let endTimeSelector = document.getElementById("end-datetime");

// Make dropdown selector with year, month, day, hour, and minute
startTimeSelector.innerHTML = `
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
    </div>`;

endTimeSelector.innerHTML = `
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
    </div>`;

// Add months to dropdown
for (let i = 1; i <= 12; i++) {
  let month = document.createElement("option");
  month.value = i;
  month.innerHTML = i;
  document.getElementById("start-month").appendChild(month);
  document.getElementById("end-month").appendChild(month.cloneNode(true));
}
// Add days to dropdown
for (let i = 1; i <= 31; i++) {
  let day = document.createElement("option");
  day.value = i;
  day.innerHTML = i;
  document.getElementById("start-day").appendChild(day);
  document.getElementById("end-day").appendChild(day.cloneNode(true));
}
// Add hours to dropdown
for (let i = 0; i <= 23; i++) {
  let hour = document.createElement("option");
  hour.value = i;
  hour.innerHTML = i;
  document.getElementById("start-hour").appendChild(hour);
  document.getElementById("end-hour").appendChild(hour.cloneNode(true));
}
// Add minutes to dropdown
for (let i = 0; i <= 59; i++) {
  let minute = document.createElement("option");
  minute.value = i;
  minute.innerHTML = i;
  document.getElementById("start-minute").appendChild(minute);
  document.getElementById("end-minute").appendChild(minute.cloneNode(true));
}

window.nextWindow = function () {
  // Get values from start and end times selectors
  let startYear = document.getElementById("start-year").value;
  let startMonth = document.getElementById("start-month").value;
  let startDay = document.getElementById("start-day").value;
  let startHour = document.getElementById("start-hour").value;
  let startMinute = document.getElementById("start-minute").value;
  let endYear = document.getElementById("end-year").value;
  let endMonth = document.getElementById("end-month").value;
  let endDay = document.getElementById("end-day").value;
  let endHour = document.getElementById("end-hour").value;
  let endMinute = document.getElementById("end-minute").value;
  // Convert start and end times to format string "YYYY-MM-DD HH:MM:SS" (Seconds are 00 by default)
  let startTime = `${startYear}-${startMonth}-${startDay} ${startHour}:${startMinute}:00`;
  let endTime = `${endYear}-${endMonth}-${endDay} ${endHour}:${endMinute}:00`;
  // Get current time
  let currentTime = new Date();
  // string to date
  let startDateD = strToDate(startTime);
  let endDateD = strToDate(endTime);
  // Log dates
  console.log(startDateD);
  console.log(endDateD);
  // Verify that start time is after current time
  if (startDateD < currentTime) {
    alert("Start time must be after current time");
    return;
  }
  // Verify that end time is after start time
  if (endDateD < startDateD) {
    alert("End time must be after start time");
    return;
  }
  // Verify that end time is after current time
  if (endDateD < currentTime) {
    alert("End time must be after current time");
    return;
  }
  // Store startTime and endTime in localStorage
  localStorage.setItem("startTime", startTime);
  localStorage.setItem("endTime", endTime);
  // Redirect to next page (devices.html)
  window.location.href = "devices.html";
};

// String to date function
function strToDate(dtStr) {
  console.log(dtStr);
  if (!dtStr) return null;
  let dateParts = dtStr.split("-");
  let timeParts = dateParts[2].split(" ")[1].split(":");
  dateParts[2] = dateParts[2].split(" ")[0];
  // month is 0-based, that's why we need dataParts[1] - 1
  let dateObj = new Date(
    dateParts[0],
    dateParts[1] - 1,
    dateParts[2],
    timeParts[0],
    timeParts[1],
    timeParts[2]
  );
  console.log(dateObj);
  return dateObj;
}
