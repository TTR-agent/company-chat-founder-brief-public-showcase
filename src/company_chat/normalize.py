"""Normalize Slack-like exports into public-safe message records."""

from __future__ import annotations

from typing import Any


def normalize_messages(raw_messages: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Keep only fields needed for analysis and strip private metadata."""
    normalized: list[dict[str, str]] = []
    for message in raw_messages:
        person = str(message.get("user") or message.get("person") or "Unknown").strip()
        text = str(message.get("text") or "").strip()
        timestamp = str(message.get("ts") or message.get("timestamp") or "").strip()
        channel = str(message.get("channel") or "company-chat").strip()
        if not text:
            continue
        normalized.append(
            {
                "person": person,
                "text": text,
                "timestamp": timestamp,
                "channel": channel,
            }
        )
    return normalized

