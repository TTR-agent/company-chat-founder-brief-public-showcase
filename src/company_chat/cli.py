"""CLI for the public-safe company chat founder brief demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyze import analyze_messages
from .founder_voice import FounderVoice
from .normalize import normalize_messages
from .render import render_daily_brief, render_weekly_meeting_prep


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a public-safe founder brief from fake Slack-like messages.")
    parser.add_argument("--messages", default="examples/slack-messages.json", help="Path to fake Slack-like messages JSON.")
    parser.add_argument("--voice", default="docs/founder-voice.md", help="Path to public-safe founder voice profile.")
    parser.add_argument("--mode", choices=["daily", "weekly"], default="daily", help="Output type.")
    args = parser.parse_args()

    raw_messages = json.loads(Path(args.messages).read_text())
    messages = normalize_messages(raw_messages)
    expected_people = sorted({str(item.get("user") or item.get("person")) for item in raw_messages if item.get("user") or item.get("person")})
    analysis = analyze_messages(messages, expected_people=expected_people)
    voice = FounderVoice.from_file(args.voice)

    if args.mode == "weekly":
        print(render_weekly_meeting_prep(analysis, voice))
    else:
        print(render_daily_brief(analysis, voice))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

