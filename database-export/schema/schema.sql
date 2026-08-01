PRAGMA foreign_keys = ON;

CREATE TABLE sources (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  path TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  word_count INTEGER NOT NULL,
  paragraph_count INTEGER NOT NULL
);

CREATE TABLE chunks (
  id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL REFERENCES sources(id),
  chunk_index INTEGER NOT NULL,
  start_word INTEGER NOT NULL,
  end_word INTEGER NOT NULL,
  text TEXT NOT NULL
);

CREATE VIRTUAL TABLE chunks_fts USING fts5(
  id UNINDEXED,
  text,
  tokenize='unicode61'
);

CREATE TABLE entities (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  group_name TEXT,
  name TEXT NOT NULL,
  aliases_json TEXT NOT NULL,
  summary TEXT NOT NULL,
  status TEXT,
  extra_json TEXT NOT NULL
);

CREATE TABLE relationships (
  source_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  target_id TEXT NOT NULL,
  note TEXT,
  PRIMARY KEY (source_id, relation, target_id)
);

CREATE TABLE timeline (
  sort_order INTEGER PRIMARY KEY,
  period TEXT NOT NULL,
  event TEXT NOT NULL
);

CREATE TABLE canon_facts (
  id TEXT PRIMARY KEY,
  subject TEXT NOT NULL,
  fact TEXT NOT NULL,
  status TEXT NOT NULL
);

CREATE TABLE conversation_summaries (
  id TEXT PRIMARY KEY,
  topic TEXT NOT NULL,
  summary TEXT NOT NULL,
  provenance TEXT NOT NULL
);
