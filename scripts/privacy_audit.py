#!/usr/bin/env python3
"""Public-safety scan for the Venture Community Ops repo."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SECRET_PATTERNS = [
    ("OpenAI/API sk key", r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}"),
    ("Anthropic key", r"sk-ant-[A-Za-z0-9_\-]{12,}"),
    ("GitHub token", r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}|github_pat_[A-Za-z0-9_]{20,}"),
    ("Google API key", r"AIza[0-9A-Za-z\-_]{35}"),
    ("AWS access key", r"AKIA[0-9A-Z]{16}"),
    ("Slack token", r"xox[baprs]-[0-9A-Za-z-]{20,}"),
    ("JWT", r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ("Private key block", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ("Bearer token", r"Bearer\s+[A-Za-z0-9._\-]{25,}"),
    ("Basic auth URL", r"https?://[^/\s:@]+:[^/\s@]+@"),
]

PRIVATE_PATTERNS = [
    ("Private/local absolute path", r"/Users/|~/(?:dev|Documents)|(?:^|[\s\"'])\.claude(?:/|\b)|(?:^|[\s\"'])\.codex(?:/|\b)"),
    ("Old private branding", r"Emerging\s*LA|EmergingLA|emerging-la|ela-dashboard|eladash|ela-workspace|emergingla\.com|\bELA\b"),
    ("Private people names", r"\b(?:Brandon|Cesar|Ces)\b"),
    ("Private GitHub/user refs", r"github\.com/cesalas13/(?:ela|orchestrated)|\borchestratedbyczr\b|\bczer\b"),
    ("Concrete Google Sheet IDs/URLs", r"https://docs\.google\.com/spreadsheets/d/[A-Za-z0-9_-]+|spreadsheets/d/[A-Za-z0-9_-]+"),
    ("Known private sheet IDs", r"15ZiT7r-aDOyUVmU96nLd9m0ktZll3_ri6Z6DO3EsZ2w|1ZcBZzj2rzplo3hjxoM1J8L6Oxl1QdwZDIz5BnJ-cugE"),
    ("Private automation endpoints", r"https?://[^\s\"'<>]*(?:webhook|telegram\.me|t\.me/)[^\s\"'<>]*"),
    ("Private event labels", r"Milken|Beverly Hills|NASA|JPL|Space Tour"),
    ("Private venue labels/domains", r"Bacari|Marea|Catch LA|Matsuhisa|Nobu|Cecconi|Manhatta|Locanda Verde|Nine Orchard|Altamarea|manhattarestaurant|cecconisdumbo"),
]

PII_PATTERNS = [
    ("Non-placeholder email", r"(?<![\w.+-])[A-Za-z0-9._%+-]+@(?!(?:2x\.png|example\.invalid|example\.com|[A-Za-z0-9.-]+\.example)\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])"),
    ("Non-placeholder phone", r"(?<!\d)(?:\+1[\s.-]?)?(?!\(?000\)?[\s.-]?000[\s.-]?0000)(?:\(\d{3}\)|\d{3}[\s.-])\s*\d{3}[\s.-]?\d{4}(?!\d)"),
]

SKIP_PARTS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
SKIP_FILES = {"scripts/privacy_audit.py"}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    files = []
    for raw in result.stdout.decode("utf-8").split("\0"):
        if raw:
            files.append(ROOT / raw)
    return files


def readable_text(path: Path) -> str | None:
    if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
        return None
    data = path.read_bytes()
    if b"\0" in data:
        return None
    return data.decode("utf-8", "replace")


def scan() -> list[tuple[str, str, str, int, str]]:
    hits: list[tuple[str, str, str, int, str]] = []
    groups = [
        ("secret", SECRET_PATTERNS, 0),
        ("private", PRIVATE_PATTERNS, re.IGNORECASE),
        ("pii", PII_PATTERNS, re.IGNORECASE),
    ]
    for path in tracked_files():
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES:
            continue
        text = readable_text(path)
        if text is None:
            continue
        for group_name, patterns, flags in groups:
            for pattern_name, pattern in patterns:
                for match in re.finditer(pattern, text, flags):
                    line = text.count("\n", 0, match.start()) + 1
                    snippet = text[max(0, match.start() - 40): match.end() + 40].replace("\n", " ")
                    hits.append((group_name, pattern_name, rel, line, snippet))
    return hits


def main() -> int:
    hits = scan()
    print(f"privacy audit: scanned {len(tracked_files())} tracked files")
    if not hits:
        print("privacy audit: PASS")
        return 0

    print(f"privacy audit: FAIL ({len(hits)} hits)")
    for group_name, pattern_name, rel, line, snippet in hits:
        print(f"{group_name}\t{pattern_name}\t{rel}:{line}\t{snippet}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
