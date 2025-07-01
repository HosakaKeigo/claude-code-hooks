# Claude Code Hooks - Slack Integration

A collection of Slack notification hook scripts for Claude Code. Notifies code execution status to Slack in real-time.

## Features

- 📢 **Notification Hook**: User confirmation pending notifications
- 🔧 **PreToolUse Hook**: Pre-tool execution notifications
- ✅ **PostToolUse Hook**: Post-tool execution result notifications

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/HosakaKeigo/claude-code-hooks.git
cd claude-code-hooks
```

### 2. Create Hook Directory

```bash
mkdir -p ~/.claude/hooks
cp -r hooks/* ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.py
```

### 3. Configure Slack Webhook URL

#### Create Slack Incoming Webhook

1. Access [Slack API](https://api.slack.com/apps)
2. Select "Create New App" → "From scratch"
3. Set App name and Workspace
4. Enable "Incoming Webhooks"
5. Select notification channel with "Add New Webhook to Workspace"
6. Copy the Webhook URL

#### Create Environment Configuration File

```bash
cp .env.example ~/.claude/hooks/.env
```

Edit `~/.claude/hooks/.env`:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_DEFAULT_CHANNEL=#claude-code
```

### 4. Add to Claude Code Configuration

Add the following to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /Users/YOUR_USERNAME/.claude/hooks/slack_notifier.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit|MultiEdit|Read",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /Users/YOUR_USERNAME/.claude/hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash|Write|Edit|MultiEdit|Read",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /Users/YOUR_USERNAME/.claude/hooks/post_tool_use.py"
          }
        ]
      }
    ]
  }
}
```

※ Replace `/Users/YOUR_USERNAME` with your actual path

Alternatively, use the provided configuration file:

```bash
# Merge with existing configuration
jq -s '.[0] * .[1]' ~/.claude/settings.json config/hooks-config.json > ~/.claude/settings.json.tmp
mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```

### 5. Verify Operation

Check configuration with Claude Code:

```
claude /hooks
```

## Testing

Test individual scripts:

```bash
# Notification Hook
echo '{"title": "Test", "message": "Hello from Claude Code"}' | python3 ~/.claude/hooks/slack_notifier.py

# PreToolUse Hook
echo '{
  "session_id": "test123",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/test/file.txt",
    "content": "test content"
  }
}' | python3 ~/.claude/hooks/pre_tool_use.py

# PostToolUse Hook
echo '{
  "session_id": "test123",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/test/file.txt",
    "content": "test content"
  },
  "tool_response": {
    "success": true
  }
}' | python3 ~/.claude/hooks/post_tool_use.py
```

## Customization

### Change Target Tools for Notifications

Edit the `matcher` field in `config/hooks-config.json`:

```json
"matcher": "Bash|Write|Edit|MultiEdit|Read|WebFetch|WebSearch"
```

### Change Notification Channel

Configure in the `.env` file:

```
SLACK_DEFAULT_CHANNEL=@username  # DM
SLACK_DEFAULT_CHANNEL=#general   # Channel
```

### Customize Icons

Change `icon_emoji` in each script or specify an image using `icon_url`.

## File Structure

```
claude-code-hooks/
├── README.md
├── .gitignore
├── .env.example
├── hooks/
│   ├── slack_common.py      # Common module
│   ├── slack_notifier.py    # Notification Hook
│   ├── pre_tool_use.py      # PreToolUse Hook
│   └── post_tool_use.py     # PostToolUse Hook
├── config/
│   └── hooks-config.json    # Claude Code configuration example
└── assets/
    └── .gitkeep
```

## Important Notes

- Do not commit `.env` file to Git
- Treat Webhook URL as confidential information
- Python 3.6+ is required

## License

MIT License

## Author

HosakaKeigo