#!/usr/bin/env python3
"""Search the generated campaign database."""

import argparse
import lzma
import sqlite3
from pathlib import Path


def ensure_database(path: Path) -> Path:
    if path.exists():
        return path
    archive = path.with_suffix(path.suffix + ".xz")
    if not archive.exists():
        raise FileNotFoundError(f"Database and archive are missing: {path}")
    path.write_bytes(lzma.decompress(archive.read_bytes()))
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="FTS5 search query")
    parser.add_argument("--db", default=str(Path(__file__).resolve().parents[1] / "data" / "dnd_12_circle.sqlite3"))
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    con = sqlite3.connect(ensure_database(Path(args.db)))
    rows = con.execute(
        "SELECT c.id, snippet(chunks_fts, 1, '[', ']', ' … ', 20) "
        "FROM chunks_fts JOIN chunks c USING(id) "
        "WHERE chunks_fts MATCH ? LIMIT ?",
        (args.query, args.limit),
    ).fetchall()
    for chunk_id, snippet in rows:
        print(f"{chunk_id}: {snippet}")


if __name__ == "__main__":
    main()
