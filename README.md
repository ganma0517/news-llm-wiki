# News Analysis LLM Wiki

A scalable LLM-powered news analysis system for large corpora (hundreds to thousands of articles). Instead of summarizing every article individually, Claude synthesizes **events, actors, and themes** — the wiki becomes a structured knowledge base about what happened, not a filing cabinet of raw clippings.

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adapted for news-scale data.

---

## Why Not One-Page-Per-Article?

| Approach | 50 articles | 5,000 articles |
|---|---|---|
| One wiki page per article | ✅ practical | ❌ 5,000 pages, unusable index |
| **This system (event/theme pages)** | ✅ works | ✅ still works |

The key insight: **news articles are evidence, not units of knowledge**. Ten articles reporting the same protest are one event with ten evidence trails — not ten wiki pages.

---

## Architecture

```
your-news-project/
├── PURPOSE.md              # ← Fill this first: project scope + what deserves a wiki page
├── raw/
│   └── news/                   # Raw articles, organized by month
│       ├── 2025-01/
│       │   ├── article-001.md  # Plain text or markdown
│       │   └── article-002.md
│       └── 2025-02/
├── metadata.csv                # One row per article — the searchable index
├── wiki/                       # Claude-maintained synthesis pages
│   ├── index.md                # Master catalogue of events/actors/themes
│   ├── log.md                  # Append-only record of all operations
│   ├── events/                 # One page per distinct news event or story arc
│   ├── actors/                 # Politicians, organizations, movements
│   ├── themes/                 # Recurring frames, narratives, policy issues
│   └── overview/               # Cross-cutting analysis and timelines
├── analysis/                   # Programmatic outputs (Python scripts + results)
│   ├── scripts/                # Reusable analysis scripts
│   └── results/                # CSVs, charts, frequency counts
├── outputs/                    # Final exports — reports, essays, presentations
└── CLAUDE.md                   # Wiki schema — Claude reads this first
```

---

## The Three-Layer Workflow

```
Layer 1 (raw/)         Layer 2 (analysis/)        Layer 3 (wiki/)
─────────────          ───────────────────         ───────────────
Raw articles     →     Batch analysis      →       Synthesis pages
metadata.csv           (Python scripts)            Events / Actors / Themes
                        frequency, sentiment,       Cross-links, timelines
                        entity extraction           Claude-maintained
```

- **Layer 1**: You collect. Claude and Python never modify `raw/`.
- **Layer 2**: Python handles bulk quantitative work (frequency, sentiment, entity counts). Outputs go to `analysis/results/`.
- **Layer 3**: Claude reads analysis outputs + samples of raw articles → writes synthesis wiki pages.

---

## Quick Start

### 0. Fill in PURPOSE.md

Before ingesting anything, open `PURPOSE.md` and describe your project scope: what period, which outlets, what analysis questions, and crucially — what threshold an event or actor must meet to get their own wiki page. Claude reads this first every session.

### 1. Clone and set up

```bash
git clone https://github.com/ganma0517/news-llm-wiki.git my-news-project
cd my-news-project
```

### 2. Add articles

Save articles as plain text or Markdown in `raw/news/YYYY-MM/`. Then add a row to `metadata.csv` for each:

```csv
id,date,outlet,title,filename,tags,url
001,2025-01-15,自由時報,罷免連署突破門檻,raw/news/2025-01/article-001.md,recall;KMT;Taiwan,https://...
```

### 3. Run batch analysis (optional but recommended)

```bash
python analysis/scripts/summarize_month.py --month 2025-01
```

This generates frequency counts and keyword summaries in `analysis/results/`.

### 4. Ask Claude to synthesize

```
Read analysis/results/2025-01-summary.csv and the articles in raw/news/2025-01/.
Create or update wiki pages for the major events and actors in this batch.
```

### 5. Query the wiki

```
What narratives dominated recall coverage in January 2025?
Which actors received the most negative framing?
```

---

## metadata.csv Format

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Unique article ID (e.g., `001`, `LTN-20250115`) |
| `date` | YYYY-MM-DD | Publication date |
| `outlet` | string | Media outlet name |
| `title` | string | Article headline |
| `filename` | string | Path relative to project root |
| `tags` | string | Semicolon-separated keywords |
| `url` | string | Original URL (for reference) |
| `sentiment` | string | `positive` / `negative` / `neutral` (optional, fill after analysis) |
| `event_id` | string | Links to a `wiki/events/` page (optional, fill after synthesis) |

---

## Wiki Page Types

### Events (`wiki/events/`)
One page per distinct story arc or news event.

```markdown
---
title: 2025 Taiwan Great Recall Wave
type: event
date_range: 2025-01 to 2025-06
related: ["[[kmt-legislators]]", "[[poera-reform]]"]
confidence: high
---

## Summary
## Timeline
## Key Actors
## Media Framing
## Turning Points
## Sources (article IDs)
```

### Actors (`wiki/actors/`)
Politicians, parties, organizations, movements.

```markdown
---
title: KMT Legislative Caucus
type: actor
related: ["[[2025-recall-wave]]"]
---

## Role
## Coverage Volume
## Framing (how media portrays them)
## Key Moments
## Linked Events
```

### Themes (`wiki/themes/`)
Recurring narratives, frames, or policy issues that cut across events.

```markdown
---
title: Civil Society vs. Party Machine Frame
type: theme
---

## Description
## When It Appears
## Outlets Using This Frame
## Counter-narratives
```

---

## Querying at Scale

When the corpus is large, Claude uses `metadata.csv` as its search layer:

```
Find all articles tagged "recall" between 2025-01 and 2025-03.
```

Claude filters `metadata.csv` first, then reads only the relevant articles — so you're never loading thousands of files into context at once.

For semantic search across 1,000+ articles, consider adding a local vector database (Chroma, sqlite-vec). The `analysis/` folder is the right place for this.

---

## Scaling Guide

| Corpus size | Approach |
|---|---|
| < 500 articles | Direct ingest batches; Claude reads articles directly |
| 500–2,000 articles | Use `metadata.csv` filtering + sampling; Python for frequency counts |
| 2,000–10,000 articles | Add local vector search; Claude queries embeddings, reads top-k |
| 10,000+ articles | Full RAG pipeline; wiki becomes synthesis-only layer |

---

## Obsidian Integration

Open the project root as an Obsidian vault. `[[wikilinks]]` in `wiki/` pages will resolve automatically. The graph view shows how events, actors, and themes connect.

---

## Credits

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).  
Template by [beck](https://github.com/ganma0517).
