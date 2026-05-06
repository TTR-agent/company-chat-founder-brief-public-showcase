"""Founder voice profile for meeting-ready output."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FounderVoice:
    """Small public-safe equivalent of a founder voice or soul file."""

    principles: tuple[str, ...]

    @classmethod
    def from_file(cls, path: str) -> "FounderVoice":
        text = Path(path).read_text()
        principles = tuple(
            line.removeprefix("-").strip()
            for line in text.splitlines()
            if line.strip().startswith("-")
        )
        return cls(principles=principles)

    def opening(self) -> str:
        return "Be direct, commercial, and kind without softening accountability."
