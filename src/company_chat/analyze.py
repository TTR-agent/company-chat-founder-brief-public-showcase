"""Analyze normalized team chat into founder-ready operating signals."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


WORKSTREAM_KEYWORDS = {
    "sales": {"sales", "demo", "customer", "pipeline", "call", "deal", "trial"},
    "marketing": {"marketing", "post", "launch", "published", "pricing", "conversion", "signup", "signups"},
    "operations": {"ops", "operation", "support", "queue", "migration", "process", "cleanup"},
    "product": {"product", "feature", "bug", "release", "website", "landing"},
}

BLOCKER_KEYWORDS = {
    "approval needed": {"approval", "approve", "review"},
    "blocked": {"blocked", "stuck", "waiting"},
    "ownership unclear": {"owner", "ownership", "unclear", "handoff"},
}

COMMERCIAL_KEYWORDS = {
    "conversion or pipeline impact": {"conversion", "signup", "signups", "demo", "pipeline", "trial", "revenue"},
    "customer delivery impact": {"customer", "migration", "support", "launch"},
    "marketing distribution impact": {"campaign"},
}


def analyze_messages(
    messages: list[dict[str, str]],
    *,
    expected_people: list[str] | None = None,
) -> dict[str, Any]:
    people: dict[str, dict[str, Any]] = defaultdict(_empty_person)
    for message in messages:
        person = message["person"]
        text = message["text"]
        lowered = text.lower()
        people[person]["messages"].append(text)
        people[person]["workstreams"].update(_matches(lowered, WORKSTREAM_KEYWORDS))
        people[person]["blockers"].update(_matches(lowered, BLOCKER_KEYWORDS))
        people[person]["commercial_relevance"].update(_matches(lowered, COMMERCIAL_KEYWORDS))
        people[person]["evidence"].append(text)

    expected = expected_people or sorted(people.keys())
    visibility_gaps = [
        f"{person} had no visible update in the review window."
        for person in expected
        if person not in people
    ]

    return {
        "people": {
            person: {
                "messages": data["messages"],
                "workstreams": sorted(data["workstreams"]),
                "blockers": sorted(data["blockers"]),
                "commercial_relevance": sorted(data["commercial_relevance"]),
                "evidence": data["evidence"],
            }
            for person, data in sorted(people.items())
        },
        "visibility_gaps": visibility_gaps,
        "message_count": len(messages),
    }


def _empty_person() -> dict[str, Any]:
    return {
        "messages": [],
        "workstreams": set(),
        "blockers": set(),
        "commercial_relevance": set(),
        "evidence": [],
    }


def _matches(text: str, groups: dict[str, set[str]]) -> set[str]:
    matches: set[str] = set()
    for label, keywords in groups.items():
        if any(keyword in text for keyword in keywords):
            matches.add(label)
    return matches
