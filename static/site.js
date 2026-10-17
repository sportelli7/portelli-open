"use strict";

const connectionStatus = document.getElementById("connection-status");
function updateConnection() {
  connectionStatus.hidden = navigator.onLine;
}
window.addEventListener("online", updateConnection);
window.addEventListener("offline", updateConnection);
updateConnection();

window.addEventListener("beforeunload", () => {
  document.getElementById("navigation-status").hidden = false;
});
window.addEventListener("pageshow", () => {
  document.getElementById("navigation-status").hidden = true;
});
