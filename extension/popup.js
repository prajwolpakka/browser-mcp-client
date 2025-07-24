document.addEventListener('DOMContentLoaded', async () => {
    const statusDiv = document.getElementById('server-status');
    const toggleBtn = document.getElementById('toggle-box');
    
    // Check server status
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        statusDiv.innerHTML = '<div class="status connected">Server Connected</div>';
      } else {
        throw new Error('Server error');
      }
    } catch (error) {
      statusDiv.innerHTML = '<div class="status disconnected">Server Disconnected</div>';
    }
    
    // Toggle command box
    toggleBtn.onclick = async () => {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      chrome.tabs.sendMessage(tab.id, { action: 'toggle' });
    };
  });