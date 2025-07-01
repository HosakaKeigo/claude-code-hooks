#!/usr/bin/env python3
"""
Claude Code Slack Notification Hook

This script sends Claude Code notifications to Slack using Incoming Webhooks.
"""

import json
import sys
from slack_common import get_slack_config, send_slack_message, create_slack_payload


def main():
    """Main function to process Claude Code notification hook."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Extract notification data
    title = input_data.get("title", "Claude Code")
    message = input_data.get("message", "Notification from Claude Code")
    session_id = input_data.get("session_id", "")
    channel = input_data.get("channel")
    
    # Get Slack configuration
    try:
        config = get_slack_config()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Format notification message
    text = f"📢 {title}: {message}"
    if session_id:
        short_id = session_id[:8]
        text += f"\n_Session: {short_id}_"
    
    # Create payload
    payload = create_slack_payload(
        text=text,
        channel=channel or config["default_channel"],
        icon_emoji=":loudspeaker:"
    )
    
    # Send notification
    success = send_slack_message(config["webhook_url"], payload)
    
    if success:
        print("Slack notification sent successfully")
        sys.exit(0)
    else:
        print("Failed to send Slack notification", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()