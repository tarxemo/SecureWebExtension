chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.action == "checkURL") {
      // Extract the URL from the request
      const urlToCheck = request.url;

      // Perform a request to your Django backend for URL checking
      const apiUrl = 'http://127.0.0.1:8000/api/check-url/';
      const requestData = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: urlToCheck }),
        mode: 'cors',
      };

      fetch(apiUrl, requestData)
        .then(response => response.json())
        .then(data => {
          // Handle the response from the Django app
          if (data.result === "allowed") {
            sendResponse({ result: "allowed" });
          } else if (data.result == "blocked"){
            sendResponse({ result: "blocked" });
          }
        })
        .catch(error => {
          console.error('Error checking URL:', error);
          sendResponse({ result: "error" });
        });

      // Indicate that we want to asynchronously send a response
      return true;
    }
  }
);
