// Create floating command box
let commandBox = null;
let isVisible = false;

// Create the command interface
function createCommandBox() {
  if (commandBox) return;
  
  commandBox = document.createElement('div');
  commandBox.id = 'desktop-commander-box';
  commandBox.innerHTML = `
    <div class="commander-header">
      <span>Desktop Commander</span>
      <button id="close-commander">×</button>
    </div>
    <div class="commander-body">
      <input type="text" id="command-input" placeholder="Type tool call (e.g., read_file(path='/tmp/test.txt'))" />
      <button id="execute-command">Execute</button>
    </div>
    <div id="command-output" class="commander-output"></div>
  `;
  
  document.body.appendChild(commandBox);
  
  // Event listeners
  document.getElementById('close-commander').onclick = toggleCommandBox;
  document.getElementById('execute-command').onclick = executeCommand;
  document.getElementById('command-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') executeCommand();
  });
}

// Toggle command box visibility
function toggleCommandBox() {
  if (!commandBox) createCommandBox();
  isVisible = !isVisible;
  commandBox.style.display = isVisible ? 'block' : 'none';
}

// Execute command via Python server
async function executeCommand() {
  const input = document.getElementById('command-input');
  const output = document.getElementById('command-output');
  const command = input.value.trim();
  
  if (!command) return;
  
  output.innerHTML = '<div class="loading">Executing...</div>';
  
  try {
    const response = await fetch('http://localhost:8000/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command })
    });
    
    const result = await response.json();
    
    if (result.success) {
      output.innerHTML = `<pre class="success">${result.data}</pre>`;
      
      // Auto-fill focused input field if available
      const focusedElement = document.activeElement;
      if (focusedElement && 
          (focusedElement.tagName === 'INPUT' || 
           focusedElement.tagName === 'TEXTAREA')) {
        focusedElement.value = result.data;
        // Trigger input event for React/Vue apps
        focusedElement.dispatchEvent(new Event('input', { bubbles: true }));
      }
    } else {
      output.innerHTML = `<pre class="error">${result.error}</pre>`;
    }
  } catch (error) {
    output.innerHTML = `<pre class="error">Connection error: ${error.message}</pre>`;
  }
}

// Listen for keyboard shortcut (Ctrl+Shift+D)
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.shiftKey && e.key === 'D') {
    e.preventDefault();
    toggleCommandBox();
  }
});

// Initialize
createCommandBox();