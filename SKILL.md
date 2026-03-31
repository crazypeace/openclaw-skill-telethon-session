---
name: telethon-session
description: Create and use a Telethon .session for Telegram user-account login (not bot-token). Use when the user needs Telethon-based user identity automation, including generating the session, sending messages, or reading chats. Not for bot-token-based bots.
---

# Telethon Session Generator

Generate a `.session` file to authenticate a Telegram **user account** via Telethon, and use that session to **send** and **read** messages.

## One-time initialization (required)

Before any send/read tasks, the user must do a one-time login to create a reusable `.session` file.

1) Install deps (recommended in a venv):
```bash
apt install python3.13-venv
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install telethon
```

2) Create `.env` interactively:
```bash
bash scripts/setup_env.sh
```

3) Login once to generate the session file:
```bash
set -a && source .env && set +a
python3 scripts/login.py
```

`login.py` now supports this precedence:
- command-line flags
- environment variables (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_PHONE`, `TELETHON_SESSION`)
- interactive prompts

So after loading `.env`, you usually do **not** need to pass `--api-id`, `--api-hash`, `--phone`, or `--session` manually.

If needed, you can still override env vars explicitly:
```bash
python3 scripts/login.py --session other_session
python3 scripts/login.py --api-id 12345 --api-hash "..." --phone "+8613..."
```

Steps 2 and 3 are required. Prefer asking the user to run them locally. Only run them on the user’s behalf if the user explicitly requests it and provides the required values.

**Stop condition:** if `.env` or `*.session` is missing, **do not** attempt send/read. Ask the user to complete the steps above.

## Day-to-day actions

All actions assume:
- you are in this skill directory
- venv is activated
- env vars loaded from `.env`

Load env vars:
```bash
set -a && source .env && set +a
```

### Send a message (scripts/send.py)
```bash
python3 scripts/send.py --to @username --message "hi"
```

### Send a message to a forum topic (scripts/send_to_topic.py)
```bash
python3 scripts/send_to_topic.py --chat -1001234567890 --topic 43 --message "hi"
```

`--topic` is the forum topic root message id (also used as the topic/thread id in many Telegram contexts).

### Read recent messages (scripts/read.py)
```bash
python3 scripts/read.py --with @username --limit 10
```

## Notes / safety

- Treat `.session` like a password. Do **not** commit it.
- This is for **user-account login** (Telethon session). Not for bot-token bots.
- If Telegram invalidates the session, rerun the login step to regenerate it.

## Minimal code example

```python
from telethon import TelegramClient

client = TelegramClient('telegram_session', api_id, api_hash)
await client.start()
```

## Repository references

- Extra details live in `references.md`.
- Scripts live in `scripts/`.
