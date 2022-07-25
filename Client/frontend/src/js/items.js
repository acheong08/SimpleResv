import "../../src/bootstrap/css/bootstrap.css";
import "../css/styles.css";
import "../css/items.css";

import { Items, Reserve } from "../../wailsjs/go/main/App";

mapItems();

// Make a global list of reserved items
let selectedItems = [];

// Map items to the DOM as cards
function mapItems() {
  // Get startTime and endTime from local storage
  let startTime = localStorage.getItem("startTime");
  let endTime = localStorage.getItem("endTime");
  Items(startTime, endTime)
    .then((items) => {
      // Log the items
      console.log(items);
      // Parse items from json to an array
      let itemsArray = JSON.parse(items);
      let itemList = document.getElementById("item-list");
      itemList.innerHTML = "";
      // Loop through the array and create a card for each item
      for (let i = 0; i < itemsArray.length; i++) {
        let item = itemsArray[i];
        let itemCard = document.createElement("div");
        itemCard.className = "item-list-item";
        itemCard.id = `item-${item.name}`;
        itemCard.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${item.name}</h5>
                    <p class="card-text">${item.description}</p>
                    <button class="btn btn-primary" onclick="addDevice('${item.name}')" id="button-${item.name}">Add</button>
                </div>
                `;
        itemList.appendChild(itemCard);
      }
    })
    .catch((err) => {
      console.error(err);
    });
}

// Define reserveDevice function (Adds item to the list of reserved items)
window.addDevice = function(itemName) {
    // Add item to the list of reserved items
    selectedItems.push(itemName);
    // Make the button red and change name to "Remove"
    let button = document.getElementById(`button-${itemName}`);
    button.className = "btn btn-danger";
    button.innerHTML = "Remove";
    // Change onclick function to removeDevice
    button.onclick = function() {
        removeDevice(itemName);
    }
    // Console log the list of reserved items
    console.log(selectedItems);
    // Update number of items reserved at submit button
    document.getElementById("submit-btn").textContent = "Next (" + selectedItems.length + ")";
  }
  
  // Remove item window function removes a name from the list of selected items
  window.removeDevice = function(itemName) {
    // Remove item from the list of reserved items
    selectedItems.splice(selectedItems.indexOf(itemName), 1);
    // Make the button green and change name to "Add"
    let button = document.getElementById(`button-${itemName}`);
    button.className = "btn btn-primary";
    button.innerHTML = "Add";
    // Change onclick function to addDevice
    button.onclick = function() {
        addDevice(itemName);
    }
    // Console log the list of reserved items
    console.log(selectedItems);
    // Update number of items reserved at submit button
    document.getElementById("submit-btn").textContent = "Next (" + selectedItems.length + ")";
  }


  // MakeResvRequest function (Sends the list of reserved items to the server)
  window.nextWindow = function() {
    // Get the list of reserved items
    let resvItems = selectedItems;
    // Parse the list to json
    let resvItemsJson = JSON.stringify(resvItems);
    // Get start and end times from local storage
    let startTime = localStorage.getItem("startTime");
    let endTime = localStorage.getItem("endTime");
    // Make the request
    Reserve(resvItemsJson, startTime, endTime)
      .then((response) => {
        // If the response is false, alert error and go back to times page
        if (response === false) {
          console.log(response)
          alert("Error: Could not reserve items");
          window.location.href = "times.html";
        }
        // If the response is true, go to home page
        else {
          runtime.WindowSetSize(1000, 450)
          window.location.href = "home.html";
        }
      }
      // If there is an error, alert error and go back to times page
      ).catch((err) => {
        console.log(response)
        alert("Error: Could not reserve items");
        window.location.href = "times.html";
      }
      );
  }