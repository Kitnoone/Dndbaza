#!/usr/bin/env python3
"""Unpack the checked-in SQLite snapshot."""

import lzma
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data" / "dnd_12_circle.sqlite3.xz"
DATABASE = ROOT / "data" / "dnd_12_circle.sqlite3"


def main():
    DATABASE.write_bytes(lzma.decompress(ARCHIVE.read_bytes()))
    print(DATABASE)


if __name__ == "__main__":
    main()
