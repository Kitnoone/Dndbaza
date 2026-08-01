#!/usr/bin/env python3
"""Rebuild SQLite from the checked-in JSON/JSONL and source text."""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCHEMA = (ROOT / "schema" / "schema.sql").read_text(encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    db = DATA / "dnd_12_circle.sqlite3"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.executescript(SCHEMA)

    manifest = read_json(DATA / "manifest.json")
    source = manifest["source"]
    con.execute("INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?)", (
        source["id"], source["title"], source["path"], source["sha256"],
        source["word_count"], source["paragraph_count"],
    ))
    chunks = read_jsonl(DATA / "chunks.jsonl")
    con.executemany("INSERT INTO chunks VALUES (:id, :source_id, :chunk_index, :start_word, :end_word, :text)", chunks)
    con.executemany("INSERT INTO chunks_fts(id, text) VALUES (:id, :text)", chunks)

    for entity in read_json(DATA / "entities.json"):
        extra = {k: v for k, v in entity.items() if k not in {"id", "type", "group", "name", "aliases", "summary", "status"}}
        con.execute("INSERT INTO entities VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
            entity["id"], entity["type"], entity.get("group"), entity["name"],
            json.dumps(entity.get("aliases", []), ensure_ascii=False), entity["summary"],
            entity.get("status"), json.dumps(extra, ensure_ascii=False),
        ))
    con.executemany("INSERT INTO relationships VALUES (:source, :relation, :target, :note)", read_json(DATA / "relationships.json"))
    con.executemany("INSERT INTO timeline VALUES (:order, :period, :event)", read_json(DATA / "timeline.json"))
    con.executemany("INSERT INTO canon_facts VALUES (:id, :subject, :fact, :status)", read_json(DATA / "canon_facts.json"))
    con.executemany("INSERT INTO conversation_summaries VALUES (:id, :topic, :summary, :provenance)", read_jsonl(DATA / "conversation_summaries.jsonl"))
    con.commit()
    print(db)


if __name__ == "__main__":
    main()
