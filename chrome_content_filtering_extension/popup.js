document.getElementById('blockWebsite').addEventListener('click', function() {
  var url = prompt('Enter the website URL to block:');
  
  if (url) {
    // Store the blocked URL in Chrome storage (replace with your storage logic)
    chrome.storage.local.set({ blockedUrls: [...(JSON.parse(localStorage.getItem("blockedUrls") || "[]"), url)] }, function() {
      if (chrome.runtime.lastError) {
        alert('Failed to save blocked website!');
        return;
      }
      alert('Website blocked successfully!');
    });
  }
});
