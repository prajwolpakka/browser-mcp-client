/* global document, window */

let commandBox = null;
let isDragging = false;
let dragOffsetX = 0;
let dragOffsetY = 0;

/* ------------------------------------------------------------------ */
/* 1. Create the box and make it draggable                              */
/* ------------------------------------------------------------------ */
function createCommandBox() {
  if (commandBox) return;

  commandBox = document.createElement('div');
  commandBox.id = 'desktop-commander-box';
  commandBox.style.display = 'none';
  commandBox.style.position = 'fixed';
  commandBox.style.zIndex = '10000';

  commandBox.innerHTML = `
    <div class="commander-header">
      <span>Desktop Commander</span>
      <button id="close-commander" style="cursor:pointer">×</button>
    </div>
    <div class="commander-body">
      <input type="text" id="command-input" placeholder="read_file(path='/tmp/test.txt')" />
      <button id="execute-command">Execute</button>
    </div>
    <div id="command-output" class="commander-output"></div>
  `;

  document.body.appendChild(commandBox);
  /* close and execute listeners */
  document.getElementById('close-commander').onclick = toggleCommandBox;
  document.getElementById('execute-command').onclick = executeCommand;
  document.getElementById('command-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') executeCommand();
  });

  /* -------- drag implementation -------- */
  const header = commandBox.querySelector('.commander-header');
  header.addEventListener('mousedown', startDrag);
  window.addEventListener('mousemove', doDrag);
  window.addEventListener('mouseup', stopDrag);
}

/* ---- drag helpers ---- */
function startDrag(e) {
  isDragging = true;
  dragOffsetX = e.clientX - commandBox.offsetLeft;
  dragOffsetY = e.clientY - commandBox.offsetTop;
}
function doDrag(e) {
  if (!isDragging) return;
  commandBox.style.left = (e.clientX - dragOffsetX) + 'px';
  commandBox.style.top  = (e.clientY - dragOffsetY) + 'px';
}
function stopDrag() {
  isDragging = false;
}

/* ------------------------------------------------------------------ */
/* 2. Toggle visibility and smart positioning                           */
/* ------------------------------------------------------------------ */
function toggleCommandBox() {
  if (!commandBox) createCommandBox();

  if (commandBox.style.display === 'block') {
    commandBox.style.display = 'none';
    return;
  }
  const focused = document.activeElement;
  if (focused && (focused.tagName === 'INPUT' || focused.tagName === 'TEXTAREA')) {
    const rect = focused.getBoundingClientRect();
    commandBox.style.top  = (rect.top - commandBox.offsetHeight - 8) + 'px';
    commandBox.style.left = rect.left + 'px';
  } else {
    /* fallback: centre of viewport */
    commandBox.style.top  = '100px';
    commandBox.style.left = Math.max(0, (window.innerWidth - 400) / 2) + 'px';
  }
  commandBox.style.display = 'block';
  document.getElementById('command-input').focus();
}

/* ------------------------------------------------------------------ */
/* 3. Keyboard shortcut                                                 */
/* ------------------------------------------------------------------ */
document.addEventListener('keydown', e => {
  if (e.ctrlKey && e.shiftKey && e.key === 'D') {
    e.preventDefault();
    toggleCommandBox();
  }
});

/* ------------------------------------------------------------------ */
/* 4. Execute command & paste JSON into page                            */
/* ------------------------------------------------------------------ */
async function executeCommand() {
  const input   = document.getElementById('command-input');
  const output  = document.getElementById('command-output');
  const command = input.value.trim();
  if (!command) return;

  output.innerHTML = '<div class="loading">Executing…</div>';

  try {
    const res = await fetch('http://localhost:8000/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(JSON.parse(command))
    });    const data = await res.json();

    if (data.success) {
      /* --- find any textarea in the page and paste response --- */
      const textarea = document.querySelector('textarea');
      if (textarea) {
        textarea.focus();
        document.execCommand('insertText', false, data.data);
        output.innerHTML = '<div class="success">✓ Pasted successfully</div>';
      } else {
        output.innerHTML = '<div class="error">✗ No textarea found on this page</div>';
      }
      
      /* Clear the input for next command */
      input.value = '';
    } else {
      output.innerHTML = `<div class="error">✗ Error: ${data.error}</div>`;
    }
  } catch (err) {
    output.innerHTML = `<div class="error">✗ Connection error: ${err.message}</div>`;
  }
}

/* ------------------------------------------------------------------ */
/* 5. Initialise                                                        */
/* ------------------------------------------------------------------ */
createCommandBox();