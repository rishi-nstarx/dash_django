// document.addEventListener("DOMContentLoaded", function () {
//     const ws = new WebSocket("ws://127.0.0.1:8000/ws/live-data/");

//     ws.onopen = function () {
//         console.log("WebSocket connection established");
//     };

//     ws.onmessage = function (event) {
//     console.log("Received data:", event.data);

//     // Parse the incoming data
//     const data = JSON.parse(event.data);

//     // Get the data-board div
//     const dataBoard = document.getElementById("data-board");

//     // Clear existing content
//     dataBoard.innerHTML = "";

//     // Create a title for the data board
//     const title = document.createElement("h2");
//     title.textContent = "Live Zone Data";
//     dataBoard.appendChild(title);

//     // Create a table element
//     const table = document.createElement("table");
//     table.style.borderCollapse = "collapse";
//     table.style.width = "100%";

//     // Add table header
//     const headerRow = document.createElement("tr");
//     const headers = ["Zone", "Users"];
//     headers.forEach(headerText => {
//         const th = document.createElement("th");
//         th.textContent = headerText;
//         th.style.border = "1px solid black";
//         th.style.padding = "8px";
//         th.style.textAlign = "left";
//         headerRow.appendChild(th);
//     });
//     table.appendChild(headerRow);

//     // Add data rows
//     for (const [zone, users] of Object.entries(data)) {
//         const row = document.createElement("tr");

//         const zoneCell = document.createElement("td");
//         zoneCell.textContent = zone;
//         zoneCell.style.border = "1px solid black";
//         zoneCell.style.padding = "8px";

//         const userCell = document.createElement("td");
//         userCell.textContent = users;
//         userCell.style.border = "1px solid black";
//         userCell.style.padding = "8px";

//         row.appendChild(zoneCell);
//         row.appendChild(userCell);
//         table.appendChild(row);
//     }

//     // Append the table to the data-board
//     dataBoard.appendChild(table);
// };




//     ws.onerror = function (error) {
//         console.error("WebSocket error:", error);
//     };

//     ws.onclose = function () {
//         console.log("WebSocket connection closed");
//     };
// });
