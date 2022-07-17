import "../../src/bootstrap/css/bootstrap.css";
import "../css/styles.css";
import "../css/devices.css";

import { Devices } from "../../wailsjs/go/main/App";

mapDevices();

// Make a global list of reserved devices
let reservedDevices = [];

// Map devices to the DOM as cards
function mapDevices() {
  Devices("2022-01-01 00:00:00", "2022-01-01 01:00:00")
    .then((devices) => {
      // Log the devices
      console.log(devices);
      // Parse devices from json to an array
      let devicesArray = JSON.parse(devices);
      let deviceList = document.getElementById("device-list");
      deviceList.innerHTML = "";
      // Loop through the array and create a card for each device
      for (let i = 0; i < devicesArray.length; i++) {
        let device = devicesArray[i];
        let deviceCard = document.createElement("div");
        deviceCard.className = "device-list-item";
        deviceCard.id = `device-${device.name}`;
        deviceCard.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${device.name}</h5>
                    <p class="card-text">${device.description}</p>
                    <button class="btn btn-primary" onclick="reserveDevice('${device.name}')" id="button-${device.name}">Add</button>
                </div>
                `;
        deviceList.appendChild(deviceCard);
      }
    })
    .catch((err) => {
      console.error(err);
    });
}

// Define reserveDevice function (Adds device to the list of reserved devices)
window.reserveDevice = function(deviceName) {
    // Add device to the list of reserved devices
    reservedDevices.push(deviceName);
    // Grey out the device card and disable the button
    document.getElementById(`button-${deviceName}`).disabled = true;
    document.getElementById(`button-${deviceName}`).className = "btn btn-secondary disabled";
    // Console log the list of reserved devices
    console.log(reservedDevices);
    // Update number of devices reserved at submit button
    document.getElementById("submit-btn").textContent = "Next (" + reservedDevices.length + ")";
  }
  
  // MakeResvRequest function (Sends the list of reserved devices to the server)
  window.makeResvRequest = function() {
    // Get the list of reserved devices
    let resvDevices = reservedDevices;
    // Parse the list to json
    let resvDevicesJson = JSON.stringify(resvDevices);
    // Log the list of reserved devices
    console.log(resvDevicesJson);
  }