#!/usr/bin/env python3
"""
Common Slack notification functionality for Claude Code hooks.
"""

import json
import urllib.request
from pathlib import Path


def load_env():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent / ".env"
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def get_slack_config():
    """Get Slack configuration from environment."""
    env_vars = load_env()
    webhook_url = env_vars.get("SLACK_WEBHOOK_URL", "")
    default_channel = env_vars.get("SLACK_DEFAULT_CHANNEL", "#claude-code")
    
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL not found in .env file")
    
    return {
        "webhook_url": webhook_url,
        "default_channel": default_channel
    }


def send_slack_message(webhook_url, payload):
    """Send a message to Slack using webhook."""
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
            
    except Exception as e:
        print(f"Error sending Slack message: {e}")
        return False


def format_tool_message(tool_name, tool_input, tool_response=None, is_pre=False):
    """Format a tool use message for Slack."""
    if is_pre:
        # PreToolUse: ツール実行前
        message = f"🔧 Tool: `{tool_name}`"
        
        # ツールごとの特別な処理
        if tool_name == "Bash":
            command = tool_input.get("command", "")
            description = tool_input.get("description", "")
            message += f"\n```{command}```"
            if description:
                message += f"\n_{description}_"
                
        elif tool_name in ["Write", "Edit", "MultiEdit"]:
            file_path = tool_input.get("file_path", "")
            message += f"\nFile: `{file_path}`"
            
        elif tool_name == "Read":
            file_path = tool_input.get("file_path", "")
            message += f"\nReading: `{file_path}`"
            
        else:
            # その他のツール: 主要なパラメータを表示
            params = []
            for key, value in tool_input.items():
                if isinstance(value, str) and len(value) < 100:
                    params.append(f"{key}: {value}")
            if params:
                message += "\n" + "\n".join(params[:3])  # 最大3つまで
                
    else:
        # PostToolUse: ツール実行後
        message = f"✅ Completed: `{tool_name}`"
        
        if tool_response:
            # エラーチェック
            if isinstance(tool_response, dict):
                if tool_response.get("error"):
                    message = f"❌ Failed: `{tool_name}`\n{tool_response['error']}"
                elif tool_response.get("success") == False:
                    message = f"⚠️ Warning: `{tool_name}`"
                    
    return message


def create_slack_payload(text, channel=None, username="Claude Code", icon_emoji=":robot_face:"):
    """Create a Slack payload with common settings."""
    payload = {
        "text": text,
        "username": username,
    }
    
    if channel:
        payload["channel"] = channel
        
    if icon_emoji:
        payload["icon_emoji"] = icon_emoji
        
    return payload