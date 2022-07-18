import "../../src/bootstrap/css/bootstrap.css";
import "../css/styles.css";
import "../css/devices.css";

import { Devices } from "../../wailsjs/go/main/App";

mapDevices();

// Make a global list of reserved devices
let selectedDevices = [];

// Map devices to the DOM as cards
function mapDevices() {
  // Get startTime and endTime from local storage
  let startTime = localStorage.getItem("startTime");
  let endTime = localStorage.getItem("endTime");
  Devices(startTime, endTime)
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
                    <button class="btn btn-primary" onclick="addDevice('${device.name}')" id="button-${device.name}">Add</button>
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
window.addDevice = function(deviceName) {
    // Add device to the list of reserved devices
    selectedDevices.push(deviceName);
    // Make the button red and change name to "Remove"
    let button = document.getElementById(`button-${deviceName}`);
    button.className = "btn btn-danger";
    button.innerHTML = "Remove";
    // Change onclick function to removeDevice
    button.onclick = function() {
        removeDevice(deviceName);
    }
    // Console log the list of reserved devices
    console.log(selectedDevices);
    // Update number of devices reserved at submit button
    document.getElementById("submit-btn").textContent = "Next (" + selectedDevices.length + ")";
  }
  
  // Remove device window function removes a name from the list of selected devices
  window.removeDevice = function(deviceName) {
    // Remove device from the list of reserved devices
    selectedDevices.splice(selectedDevices.indexOf(deviceName), 1);
    // Make the button green and change name to "Add"
    let button = document.getElementById(`button-${deviceName}`);
    button.className = "btn btn-primary";
    button.innerHTML = "Add";
    // Change onclick function to addDevice
    button.onclick = function() {
        addDevice(deviceName);
    }
    // Console log the list of reserved devices
    console.log(selectedDevices);
    // Update number of devices reserved at submit button
    document.getElementById("submit-btn").textContent = "Next (" + selectedDevices.length + ")";
  }


  // MakeResvRequest function (Sends the list of reserved devices to the server)
  window.makeResvRequest = function() {
    // Get the list of reserved devices
    let resvDevices = selectedDevices;
    // Parse the list to json
    let resvDevicesJson = JSON.stringify(resvDevices);
    // Log the list of reserved devices
    console.log(resvDevicesJson);
  }