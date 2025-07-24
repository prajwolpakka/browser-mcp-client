# Desktop Commander – Browser MCP Client

A lightweight Chrome extension + Python server that lets you execute arbitrary tool-calls (file operations, process control, etc.) from any web page and instantly paste the result back into the page's active input field.

---

## How it works

1. **Start the server**
   ```bash
   cd server
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py
   ```
   The server listens on http://localhost:8000.

2. **Load the extension**
   - Open `chrome://extensions`
   - Enable "Developer mode" 
   - Click "Load unpacked"
   - Select the `extension/` folder
   - Make sure the extension shows "Server Connected" in its popup

3. **Use it**
   - Focus any `<input>` or `<textarea>` on any webpage
   - Press `Ctrl + Shift + D` – a floating prompt appears above the focused field
   - Paste or type a tool-call, e.g.:
     ```
     read_file(path='C:\\Users\\me\\notes.txt')
     ```
   - Hit Enter or click Execute
   - The plain-text result (or error) is inserted at the caret position
   - The prompt stays open for the next call

## Available tools

See `tools.txt` for the full list and JSON schema of every supported function (`read_file`, `write_file`, `search_code`, `start_process`, `kill_process`, etc.).

## Shortcut

| Keys | Action |
|------|--------|
| `Ctrl + Shift + D` | Toggle the command prompt box |

## Security note

The server runs with your user privileges and can read, write, move, or execute anything your account can. Use it only on trusted machines and networks.

## Troubleshooting

- **"Server Disconnected" in popup**: Ensure `python main.py` is running and port 8000 isn't blocked
- **Nothing happens on shortcut**: Reload the extension and refresh the target page  
- **CORS errors**: The server already enables CORS for all origins (Flask-CORS)