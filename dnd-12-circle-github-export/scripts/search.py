#!/usr/bin/env python3
import sqlite3,sys
from pathlib import Path
if len(sys.argv)<2: raise SystemExit('Usage: python scripts/search.py "query"')
q=' '.join(sys.argv[1:]); db=Path(__file__).resolve().parents[1]/'database'/'dnd_12_circle.sqlite'; con=sqlite3.connect(db)
for cid,title,snip in con.execute("SELECT c.chunk_id,c.title,snippet(chunks_fts,2,'[',']',' … ',18) FROM chunks_fts JOIN chunks c ON c.rowid=chunks_fts.rowid WHERE chunks_fts MATCH ? LIMIT 20",(q,)):
    print(f'\\n[{cid}] {title}\\n{snip}')
