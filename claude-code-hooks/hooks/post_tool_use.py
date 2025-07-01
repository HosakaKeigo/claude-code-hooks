#!/usr/bin/env python3
"""
PostToolUse Hook for Claude Code - Sends Slack notifications after tool execution.
"""

import json
import sys
from slack_common import get_slack_config, send_slack_message, format_tool_message, create_slack_payload


def main():
    """Process PostToolUse hook and send Slack notification."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Extract tool information
    tool_name = input_data.get("tool_name", "Unknown")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})
    session_id = input_data.get("session_id", "")
    
    # Get Slack configuration
    try:
        config = get_slack_config()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Format message
    message = format_tool_message(tool_name, tool_input, tool_response, is_pre=False)
    
    # Add session info
    if session_id:
        short_id = session_id[:8]
        message += f"\n_Session: {short_id}_"
    
    # Create and send Slack payload
    payload = create_slack_payload(
        text=message,
        channel=config["default_channel"],
        icon_emoji=":white_check_mark:"
    )
    
    success = send_slack_message(config["webhook_url"], payload)
    
    if success:
        print(f"Slack notification sent for {tool_name}")
        sys.exit(0)
    else:
        print("Failed to send Slack notification", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()