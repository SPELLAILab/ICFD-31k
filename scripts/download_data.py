#!/usr/bin/env python3
"""Download dataset shards listed in a JSONL manifest."""

from __future__ import annotations

import argparse
import json
import pathlib
import urllib.request


def read_manifest(path: pathlib.Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def download(url: str, destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        print(f"skip existing {destination}")
        return
    print(f"download {url} -> {destination}")
    urllib.request.urlretrieve(url, destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()

    for row in read_manifest(args.manifest):
        download(row["url"], args.output / row["path"])


if __name__ == "__main__":
    main()

