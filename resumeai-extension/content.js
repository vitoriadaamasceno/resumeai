chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "GET_PAGE_TEXT") {
    sendResponse({
      url: window.location.href,
    });
  }
});