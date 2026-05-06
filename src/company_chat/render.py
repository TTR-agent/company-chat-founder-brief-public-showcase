"""Render founder briefs and meeting prep from analysis."""

from __future__ import annotations

from typing import Any

from .founder_voice import FounderVoice


def render_daily_brief(analysis: dict[str, Any], voice: FounderVoice) -> str:
    lines = [
        "# Company Chat Founder Brief",
        "",
        "## Bottom line",
        _bottom_line(analysis),
        "",
        "## People read",
    ]
    for person, data in analysis["people"].items():
        lines.extend(_person_lines(person, data))
    lines.extend(["", "## Visibility gaps"])
    lines.extend(f"- {gap}" for gap in analysis["visibility_gaps"] or ["No visibility gaps in this sample."])
    lines.extend(["", "## Founder stance", f"- {voice.opening()}"])
    return "\n".join(lines).strip() + "\n"


def render_weekly_meeting_prep(analysis: dict[str, Any], voice: FounderVoice) -> str:
    lines = [
        "# Weekly Meeting Prep",
        "",
        "## Talking points",
    ]
    for person, data in analysis["people"].items():
        commercial = ", ".join(data["commercial_relevance"]) or "commercial impact unclear"
        blocker = ", ".join(data["blockers"]) or "no explicit blocker"
        lines.append(f"- Ask {person}: what is the next owned step, and how does it connect to commercial impact ({commercial})?")
        lines.append(f"  Evidence: {data['evidence'][0]}")
        lines.append(f"  Watch: {blocker}.")
    lines.extend(
        [
            "",
            "## Cross-team themes",
            f"- {voice.opening()}",
            "- Press for owner, metric, next action, and customer or revenue implication.",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def _bottom_line(analysis: dict[str, Any]) -> str:
    if analysis["message_count"] == 0:
        return "- No trustworthy team-chat signal in the review window."
    people = len(analysis["people"])
    gaps = len(analysis["visibility_gaps"])
    return f"- {people} people had visible updates; {gaps} expected people had no visible signal."


def _person_lines(person: str, data: dict[str, Any]) -> list[str]:
    workstreams = ", ".join(data["workstreams"]) or "unclear workstream"
    blockers = ", ".join(data["blockers"]) or "no explicit blocker"
    commercial = ", ".join(data["commercial_relevance"]) or "commercial impact unclear"
    return [
        f"- {person}",
        f"  Evidence: {data['evidence'][0]}",
        f"  Workstream: {workstreams}.",
        f"  Needs attention: {blockers}.",
        f"  Commercial read: {commercial}.",
    ]
