// Extract the current URL
const currentURL = window.location.href;

// Send a request to the background script for URL checking
chrome.runtime.sendMessage({ action: "checkURL", url: currentURL }, function(response) {
  if (response.result === "blocked") {
    // Redirect or block the website as needed
    window.location.href = chrome.runtime.getURL("blocked.html");
  }
});
