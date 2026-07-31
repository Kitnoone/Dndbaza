# Днд — сюжет / 12-й круг

Переносимая база знаний кампании для GitHub и NRI/RAG.

## Состав

- `source/12-круг.docx` — исходник.
- `docs/12-circle-full.md` — извлечённый текст.
- `knowledge/` — канон и справочники.
- `database/*.json` и `*.jsonl` — машинные данные.
- `database/dnd_12_circle.sqlite` — SQLite с полнотекстовым поиском.
- `database/chunks.jsonl` — 295 чанков.
- `archive/conversations/` — доступные конспекты веток.
- `scripts/search.py` — поиск.
- `scripts/import_chatgpt_export.py` — добавление официального экспорта.

## Поиск

```bash
python scripts/search.py "Седьмая струна"
```

## GitHub

```bash
git init
git add .
git commit -m "Initial campaign knowledge export"
git branch -M main
git remote add origin <URL_РЕПОЗИТОРИЯ>
git push -u origin main
```

См. `LIMITATIONS.md`.
