#!/usr/bin/env python3
import json,sys,zipfile
from pathlib import Path
if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/import_chatgpt_export.py export.zip')
root=Path(__file__).resolve().parents[1]; out=root/'archive'/'raw-chatgpt-export'; out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(Path(sys.argv[1])) as z: z.extractall(out)
files=list(out.rglob('conversations.json'))
if not files: raise SystemExit('conversations.json not found')
data=json.loads(files[0].read_text(encoding='utf-8'))
with (root/'database'/'chatgpt-export-conversations.jsonl').open('w',encoding='utf-8') as f:
    for x in data: f.write(json.dumps(x,ensure_ascii=False)+'\n')
print('Imported',len(data),'conversations')
