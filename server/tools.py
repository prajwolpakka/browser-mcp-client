import os
import shutil
import glob
import subprocess
import json
import time
import re
from typing import List, Optional

# Example in-memory config dictionary
_config = {
    "blockedCommands": [],
    "defaultShell": "/bin/bash",
    "allowedDirectories": [],
    "version": "1.0.0"
}

def get_config():
    """Get the entire server configuration."""
    return _config

def set_config_value(key: str, value):
    """Set a specific config value."""
    if key in _config:
        _config[key] = value
        return True
    else:
        raise KeyError(f"Config key '{key}' not found.")

def read_file(path: str, isUrl: bool = False, offset: int = 0, length: int = 1000):
    """Read file content or URL content (URL reading not implemented)."""
    if isUrl:
        raise NotImplementedError("URL reading not implemented.")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File '{path}' does not exist.")
    with open(path, "r") as f:
        lines = f.readlines()
    if offset < 0:
        offset = max(len(lines) + offset, 0)
    return "".join(lines[offset:offset+length])

def read_multiple_files(paths: List[str]):
    """Read multiple files content."""
    contents = {}
    for p in paths:
        try:
            contents[p] = read_file(p)
        except Exception as e:
            contents[p] = f"Error: {e}"
    return contents

def write_file(path: str, content: str, mode: str = "rewrite"):
    """Write or append text content to a file."""
    open_mode = "w" if mode == "rewrite" else "a"
    with open(path, open_mode) as f:
        f.write(content)
    return True

def create_directory(path: str):
    """Create directory including parents if needed."""
    os.makedirs(path, exist_ok=True)
    return True

def list_directory(path: str):
    """List files and directories with type info."""
    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path}' is not a directory.")
    entries = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        entries.append({
            "name": entry,
            "isFile": os.path.isfile(full_path),
            "isDirectory": os.path.isdir(full_path)
        })
    return entries

def move_file(source: str, destination: str):
    """Move or rename a file or directory."""
    shutil.move(source, destination)
    return True

def search_files(path: str, pattern: str, timeoutMs: Optional[int] = None):
    """Search files by name pattern."""
    # timeoutMs not implemented
    matches = []
    for root, _, files in os.walk(path):
        for f in files:
            if re.search(pattern, f, re.IGNORECASE):
                matches.append(os.path.join(root, f))
    return matches

def get_file_info(path: str):
    """Get metadata about file or directory."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"'{path}' does not exist.")
    info = os.stat(path)
    result = {
        "size": info.st_size,
        "created": time.ctime(info.st_ctime),
        "modified": time.ctime(info.st_mtime),
        "permissions": oct(info.st_mode)[-3:],
        "isDirectory": os.path.isdir(path),
        "isFile": os.path.isfile(path),
    }
    if os.path.isfile(path):
        with open(path, "r", errors="ignore") as f:
            lines = sum(1 for _ in f)
        result["lineCount"] = lines
    return result

def search_code(path: str, pattern: str, filePattern: Optional[str] = None, ignoreCase: bool = False,
                maxResults: Optional[int] = None, includeHidden: bool = False, contextLines: int = 0):
    """Search text/code inside files."""
    flags = re.IGNORECASE if ignoreCase else 0
    matched_results = []
    for root, dirs, files in os.walk(path):
        if not includeHidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
        for filename in files:
            if filePattern and not glob.fnmatch.fnmatch(filename, filePattern):
                continue
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "r", errors="ignore") as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if re.search(pattern, line, flags):
                        start = max(i - contextLines, 0)
                        end = min(i + contextLines + 1, len(lines))
                        snippet = "".join(lines[start:end])
                        matched_results.append({
                            "file": filepath,
                            "line": i + 1,
                            "snippet": snippet
                        })
                        if maxResults and len(matched_results) >= maxResults:
                            return matched_results
            except Exception:
                continue
    return matched_results

def edit_block(file_path: str, old_string: str, new_string: str, expected_replacements: int = 1):
    """Find/replace text in a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    with open(file_path, "r") as f:
        content = f.read()
    count = content.count(old_string)
    if count < expected_replacements:
        # Could add fuzzy matching here
        pass
    new_content = content.replace(old_string, new_string, expected_replacements)
    with open(file_path, "w") as f:
        f.write(new_content)
    return count

def start_process(command: str, timeout_ms: int, shell: Optional[str] = None):
    """Start a new process, return PID."""
    shell_cmd = shell if shell else True
    process = subprocess.Popen(command, shell=True, executable=shell)
    # ignoring timeout for simplicity
    return process.pid

def read_process_output(pid: int, timeout_ms: Optional[int] = None):
    """Not implemented: reading process output by PID is complex."""
    raise NotImplementedError("Reading process output by PID not implemented.")

def interact_with_process(pid: int, input: str, timeout_ms: Optional[int] = None, wait_for_prompt: bool = False):
    """Not implemented: interacting with process input/output."""
    raise NotImplementedError("Interacting with processes not implemented.")

def force_terminate(pid: int):
    """Terminate process by PID."""
    try:
        os.kill(pid, 9)
        return True
    except Exception as e:
        return False

def list_sessions():
    """List active Desktop Commander processes - placeholder empty list."""
    return []

def list_processes():
    """List all running system processes - simple ps output parsing."""
    try:
        out = subprocess.check_output(["ps", "-eo", "pid,comm,%cpu,%mem"], text=True)
        lines = out.strip().split("\n")[1:]
        procs = []
        for line in lines:
            parts = line.split(None, 3)
            if len(parts) == 4:
                pid, comm, cpu, mem = parts
                procs.append({"pid": int(pid), "command": comm, "cpu": cpu, "memory": mem})
        return procs
    except Exception as e:
        return []

def kill_process(pid: int):
    """Kill a system process by PID."""
    try:
        os.kill(pid, 9)
        return True
    except Exception:
        return False

def get_usage_stats():
    """Placeholder for usage statistics."""
    return {}

def give_feedback_to_desktop_commander():
    """Open feedback URL in default browser."""
    import webbrowser
    webbrowser.open("https://example.com/feedback")
    return True

