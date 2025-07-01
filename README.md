# Claude Code Hooks - Slack Integration

Claude Code用のSlack通知フックスクリプト集です。コードの実行状況をリアルタイムでSlackに通知します。

## 機能

- 📢 **Notification Hook**: ユーザー確認待ち通知
- 🔧 **PreToolUse Hook**: ツール実行前通知
- ✅ **PostToolUse Hook**: ツール実行後の結果通知

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/HosakaKeigo/claude-code-hooks.git
cd claude-code-hooks
```

### 2. フック用ディレクトリの作成

```bash
mkdir -p ~/.claude/hooks
cp -r hooks/* ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.py
```

### 3. Slack Webhook URLの設定

#### Slack Incoming Webhookの作成

1. [Slack API](https://api.slack.com/apps)にアクセス
2. "Create New App" → "From scratch"を選択
3. App名とWorkspaceを設定
4. "Incoming Webhooks"を有効化
5. "Add New Webhook to Workspace"で通知先チャンネルを選択
6. Webhook URLをコピー

#### 環境設定ファイルの作成

```bash
cp .env.example ~/.claude/hooks/.env
```

`~/.claude/hooks/.env`を編集:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_DEFAULT_CHANNEL=#claude-code
```

### 4. Claude Code設定への追加

`~/.claude/settings.json`に以下を追加:

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

※ `/Users/YOUR_USERNAME`の部分は実際のパスに置き換えてください

または、提供されている設定ファイルを使用:

```bash
# 既存の設定とマージ
jq -s '.[0] * .[1]' ~/.claude/settings.json config/hooks-config.json > ~/.claude/settings.json.tmp
mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```

### 5. 動作確認

Claude Codeで設定を確認:

```
claude /hooks
```

## テスト

個別のスクリプトをテスト:

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

## カスタマイズ

### 通知対象ツールの変更

`config/hooks-config.json`の`matcher`フィールドを編集:

```json
"matcher": "Bash|Write|Edit|MultiEdit|Read|WebFetch|WebSearch"
```

### 通知チャンネルの変更

`.env`ファイルで設定:

```
SLACK_DEFAULT_CHANNEL=@username  # DM
SLACK_DEFAULT_CHANNEL=#general   # チャンネル
```

### アイコンのカスタマイズ

各スクリプト内の`icon_emoji`を変更するか、`icon_url`を使用して画像を指定できます。

## ファイル構成

```
claude-code-hooks/
├── README.md
├── .gitignore
├── .env.example
├── hooks/
│   ├── slack_common.py      # 共通モジュール
│   ├── slack_notifier.py    # Notification Hook
│   ├── pre_tool_use.py      # PreToolUse Hook
│   └── post_tool_use.py     # PostToolUse Hook
├── config/
│   └── hooks-config.json    # Claude Code設定例
└── assets/
    └── .gitkeep
```

## 注意事項

- `.env`ファイルはGitにコミットしないでください
- Webhook URLは秘密情報として扱ってください
- Python 3.6以上が必要です

## ライセンス

MIT License

## 作者

HosakaKeigo