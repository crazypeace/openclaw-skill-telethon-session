# Telethon Session Skill Reference

## Unknown values to request from user

### Required before first real use
These values are stable for a given Telegram app/account setup and must be obtained from the user before first use:

- `api_id` — from https://my.telegram.org
- `api_hash` — from https://my.telegram.org
- `session` — local Telethon session path/name, created by `scripts/login.py`

### Required on each task
These are task inputs and may change every run:

- `username` — target Telegram username / recipient
- `text` — message content to send, only for send actions
- `limit` — how many recent messages to read, only for read actions

## Session handling

- Treat `.session` files like secrets.
- Do not commit `.session` files to git.
- Reuse the same session file until Telegram invalidates it.
- If the session is missing or invalid, run `scripts/login.py` again.

## Typical send flow

1. Ensure `telethon` is installed.
2. Ensure the user has provided `api_id` and `api_hash` (prefer `.env`).
3. Ensure a valid `.session` file exists.
4. Ask for per-run inputs: `to` and `message`.
5. Run `scripts/send.py`.

## Typical read flow

1. Ensure `telethon` is installed.
2. Ensure the user has provided `api_id` and `api_hash` (prefer `.env`).
3. Ensure a valid `.session` file exists.
4. Ask for per-run inputs: `with` and `limit`.
5. Run `scripts/read.py`.

## Examples

### Send

```bash
set -a && source .env && set +a
python3 scripts/send.py \
  --to @crazypeace \
  --message '测试信息'
```

### Read multiple recent messages

```bash
set -a && source .env && set +a
python3 scripts/read.py \
  --with @crazypeace \
  --limit 10
```
