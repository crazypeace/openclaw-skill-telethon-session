#!/usr/bin/env python3
"""Send a Telegram message as a *user* via Telethon using an existing .session.

Defaults to reading credentials from environment variables (load from .env):
  TELEGRAM_API_ID, TELEGRAM_API_HASH
Session name/path is read from --session or TELETHON_SESSION (default: telegram_session)

Example:
  set -a && source .env && set +a
  source venv/bin/activate
  python3 scripts/send.py --to @username --message "hi"
"""

import argparse
import asyncio
import getpass
import os
from pathlib import Path

from telethon import TelegramClient


def _env(name: str):
    v = os.getenv(name)
    return v if v not in (None, "") else None


def _need_int(value, env_name: str, label: str) -> int:
    if value is not None:
        return int(value)
    ev = _env(env_name)
    if ev is not None:
        return int(ev)
    while True:
        raw = input(label).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")


def _need_str(value, env_name: str, label: str, secret: bool = False) -> str:
    if value:
        return value
    ev = _env(env_name)
    if ev:
        return ev
    while True:
        raw = (getpass.getpass(label) if secret else input(label)).strip()
        if raw:
            return raw
        print("Value cannot be empty.")


async def main(args):
    api_id = _need_int(args.api_id, "TELEGRAM_API_ID", "App api_id: ")
    api_hash = _need_str(args.api_hash, "TELEGRAM_API_HASH", "App api_hash: ", secret=True)

    session = args.session or _env("TELETHON_SESSION") or "telegram_session"

    peer = args.to
    if peer.startswith("@"):
        peer = peer[1:]

    client = TelegramClient(session, api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        raise SystemExit(
            "Session is not authorized. Re-run login first (python3 scripts/login.py --session ...)."
        )

    entity = await client.get_entity(peer)
    await client.send_message(entity, args.message)

    sess_path = f"{Path(session).resolve()}.session"
    print("Sent.")
    print(f"To:      {args.to}")
    print(f"Session: {sess_path}")

    await client.disconnect()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Send Telegram message using Telethon session")
    p.add_argument("--api-id", type=int, default=None, help="Telegram API ID (from my.telegram.org)")
    p.add_argument("--api-hash", default=None, help="Telegram API hash")
    p.add_argument("--session", default=None, help="Session name/path without .session (default: TELETHON_SESSION or telegram_session)")
    p.add_argument("--to", required=True, help="Recipient: @username, username, phone, or numeric id")
    p.add_argument("--message", required=True, help="Message text")
    args = p.parse_args()

    asyncio.run(main(args))
