#!/usr/bin/env python3
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
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({"success": False, "error": "Empty command"})
        
        # Parse command (tool_name(args))
        import re
        match = re.match(r'(\w+)\((.*)\)', command.strip())
        if not match:
            return jsonify({"success": False, "error": "Invalid command format"})
        
        tool_name, args_str = match.groups()
        
        if tool_name not in TOOL_MAP:
            return jsonify({"success": False, "error": f"Unknown tool: {tool_name}"})
        
        # Parse arguments
        args = {}
        if args_str.strip():
            # Simple argument parsing (for demo - consider using ast.literal_eval for production)
            for arg in args_str.split(','):
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    args[key] = value
        
        # Execute tool
        tool_func = TOOL_MAP[tool_name]
        result = tool_func(**args)
        
        return jsonify({
            "success": True,
            "data": str(result)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)