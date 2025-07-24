// Handle extension lifecycle
chrome.runtime.onInstalled.addListener(() => {
    console.log('Desktop Commander installed');
  });
  
  // Listen for messages from popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'toggle') {
      chrome.tabs.sendMessage(sender.tab.id, { action: 'toggle' });
    }
  });