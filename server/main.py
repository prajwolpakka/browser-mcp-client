#!/usr/bin/env python3
import traceback
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import subprocess
import sys
import io
import contextlib

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

# Import your available tools
sys.path.append('.')
from tools import (
    get_config, set_config_value, read_file, write_file,
    create_directory, list_directory, move_file, search_files,
    get_file_info, search_code, edit_block, start_process,
    read_process_output, interact_with_process, force_terminate,
    list_sessions, list_processes, kill_process, get_usage_stats
)

# Map tool names to functions
TOOL_MAP = {
    'get_config': get_config,
    'set_config_value': set_config_value,
    'read_file': read_file,
    'write_file': write_file,
    'create_directory': create_directory,
    'list_directory': list_directory,
    'move_file': move_file,
    'search_files': search_files,
    'get_file_info': get_file_info,
    'search_code': search_code,
    'edit_block': edit_block,
    'start_process': start_process,
    'read_process_output': read_process_output,
    'interact_with_process': interact_with_process,
    'force_terminate': force_terminate,
    'list_sessions': list_sessions,
    'list_processes': list_processes,
    'kill_process': kill_process,
    'get_usage_stats': get_usage_stats
}

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})


@app.route('/execute', methods=['POST'])
def execute_command():
    req_time = datetime.now().strftime('%H:%M:%S')
    raw_body = request.get_data(as_text=True)
    print(f"[{req_time}] ➜  REQUEST: {raw_body}")

    try:
        payload = request.get_json(force=True)
        tool_name = payload["name"]
        args = payload.get("arguments", {})
        print(f"[{req_time}] 🔧  TOOL: {tool_name} | ARGS: {args}")

        if tool_name not in TOOL_MAP:
            msg = f"Unknown tool: {tool_name}"
            print(f"[{req_time}] ❌  {msg}")
            return jsonify({"success": False, "error": msg})

        result = TOOL_MAP[tool_name](**args)
        print(f"[{req_time}] ✅  RESULT: {result}")
        return jsonify({"success": True, "data": str(result)})

    except Exception as e:
        tb = traceback.format_exc()
        print(f"[{req_time}] 🚨  ERROR:\n{tb}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)