#!/usr/bin/env python3
"""Verify SHA-256 checksums for dataset shards listed in a JSONL manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--root", type=pathlib.Path, required=True)
    args = parser.parse_args()

    failures = 0
    with args.manifest.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            path = args.root / row["path"]
            expected = row["sha256"]
            actual = sha256(path)
            if actual != expected:
                failures += 1
                print(f"FAIL {path}: expected {expected}, got {actual}")
            else:
                print(f"OK   {path}")

    if failures:
        raise SystemExit(f"{failures} checksum failure(s)")


if __name__ == "__main__":
    main()
