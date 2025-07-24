document.addEventListener('DOMContentLoaded', async () => {
  const statusDiv = document.getElementById('server-status');
  try {
    const r = await fetch('http://localhost:8000/health');
    statusDiv.innerHTML = r.ok
      ? '<div class="status connected">Server Connected</div>'
      : '<div class="status disconnected">Server Error</div>';
  } catch {
    statusDiv.innerHTML = '<div class="status disconnected">Server Disconnected</div>';
  }
});