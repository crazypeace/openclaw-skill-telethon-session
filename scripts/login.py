#!/usr/bin/env python3
"""Generate a Telethon .session file for user-login to Telegram.

Default behavior:
- Read credentials from command-line flags when provided.
- Otherwise fall back to environment variables:
  TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELETHON_SESSION
- If still missing, prompt interactively.

Usage examples:
    # With .env already loaded into current shell
    set -a && source .env && set +a
    python3 scripts/login.py

    # Specify only session name; other values can still come from env/prompt
    python3 scripts/login.py --session telegram_session

    # Non-interactive flags (works, but may leak secrets into shell history)
    python3 scripts/login.py --api-id 24714103 --api-hash "..." --phone "+8613..."

Interactive prompts:
  - api_id
  - api_hash
  - phone
  - Telegram login code (and 2FA password if enabled)

Output:
  - <session_name>.session (default: TELETHON_SESSION or telegram_session)
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


def _normalize_phone(phone: str) -> str:
    return phone.replace(" ", "")


async def main(args):
    api_id = _need_int(args.api_id, "TELEGRAM_API_ID", "App api_id: ")
    api_hash = _need_str(args.api_hash, "TELEGRAM_API_HASH", "App api_hash: ", secret=True)
    phone = _normalize_phone(_need_str(args.phone, "TELEGRAM_PHONE", "Phone number (e.g. +8613...): "))
    session = args.session or _env("TELETHON_SESSION") or "telegram_session"

    client = TelegramClient(session, api_id, api_hash)

    # This will prompt for login code + (optional) 2FA password.
    await client.start(phone=phone)

    me = await client.get_me()
    session_path = f"{Path(session).resolve()}.session"

    print("\nLogin successful")
    print(f"Name:     {me.first_name} {me.last_name or ''}")
    print(f"Username: @{me.username or 'N/A'}")
    if args.show_phone:
        print(f"Phone:    {me.phone}")
    print(f"Session:  {session_path}")

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Telethon session file")
    parser.add_argument("--api-id", type=int, default=None, help="Telegram API ID (from my.telegram.org)")
    parser.add_argument("--api-hash", default=None, help="Telegram API hash")
    parser.add_argument("--phone", default=None, help="Phone number with country code, e.g. +86...")
    parser.add_argument(
        "--session",
        default=None,
        help="Session file name/path without .session (default: TELETHON_SESSION or telegram_session)",
    )
    parser.add_argument(
        "--show-phone",
        action="store_true",
        help="Print the phone number on success (off by default).",
    )

    asyncio.run(main(parser.parse_args()))
