# News Wiki Schema

Read this file at the start of every session before touching any wiki pages.

---

## Design Philosophy

This wiki is NOT one-page-per-article. News articles are evidence; the wiki pages are synthesis.

**Unit of wiki pages**: events, actors, themes — not individual articles.  
**Unit of raw storage**: individual articles in `raw/news/YYYY-MM/` + `metadata.csv`.

When Claude receives a batch of articles, it should ask: "What events and actors does this batch illuminate?" — then create or update wiki pages at that level.

---

## Directory Structure

```
<project>/
├── raw/
│   └── news/YYYY-MM/         # Raw articles — immutable after adding
├── metadata.csv               # Searchable index: one row per article
├── wiki/
│   ├── index.md               # Master catalogue
│   ├── log.md                 # Append-only operations log
│   ├── events/                # Distinct news events or story arcs
│   ├── actors/                # People, parties, organizations
│   ├── themes/                # Recurring narratives, frames, issues
│   └── overview/              # Cross-cutting analysis and timelines
├── analysis/
│   ├── scripts/               # Python analysis scripts
│   └── results/               # CSVs, summaries, frequency tables
├── outputs/                   # Final reports and exports
└── CLAUDE.md                  # This file
```

---

## Page Types

| Type | Directory | When to create |
|------|-----------|----------------|
| `event` | `wiki/events/` | A distinct story arc with a timeline (e.g., "2025 recall wave") |
| `actor` | `wiki/actors/` | A person, party, or organization that appears repeatedly |
| `theme` | `wiki/themes/` | A recurring frame or narrative across multiple events |
| `overview` | `wiki/overview/` | Cross-cutting analysis: timelines, comparisons, trend summaries |

Do NOT create a `source-summary` page for individual news articles.

---

## Frontmatter Rules

### Event page
```yaml
---
title: Event Name
type: event
date_range: YYYY-MM to YYYY-MM
sources:
  - metadata.csv (article IDs: 001, 002, 003)
related:
  - "[[actor-name]]"
  - "[[theme-name]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

### Actor page
```yaml
---
title: Actor Name
type: actor
sources:
  - metadata.csv (article IDs: ...)
related:
  - "[[event-name]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

### Theme page
```yaml
---
title: Theme Name
type: theme
sources:
  - metadata.csv (article IDs: ...)
related:
  - "[[event-name]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

---

## Event Page Template

```markdown
## Summary
One paragraph: what happened, when, why it matters.

## Timeline
- YYYY-MM-DD: event
- YYYY-MM-DD: development

## Key Actors
- [[actor-name]] — their role in this event

## Media Framing
How different outlets covered this event. Note dominant frames and outliers.

## Turning Points
Key moments that shifted the narrative or outcome.

## Related Events
- [[related-event]] — how it connects

## Article IDs
List of metadata.csv IDs that primarily cover this event.
```

---

## Actor Page Template

```markdown
## Role
Who they are and why they appear in this corpus.

## Coverage Volume
Approximate number of articles; trend (rising/falling/stable).

## Media Framing
How different outlets portray this actor. Note consistent frames and contested characterizations.

## Key Moments
Specific events where this actor was central.

## Linked Events
- [[event-name]] — actor's role
```

---

## Theme Page Template

```markdown
## Description
What this narrative frame claims or emphasizes.

## When It Appears
Which events, time periods, or outlets invoke this frame.

## Exemplar Articles
2–3 article IDs that best illustrate this theme.

## Counter-narratives
Competing frames that challenge or complicate this theme.

## Linked Actors / Events
- [[actor-or-event]] — connection
```

---

## The Three Operations

### Ingest (batch synthesis)
When user adds articles and says "ingest" or "synthesize":
1. Read this CLAUDE.md
2. Read `metadata.csv` to understand what's new
3. Sample relevant articles (don't try to read all 5,000 at once — filter by tag/date/event first)
4. For each major event or actor identified:
   - Check if a wiki page already exists → update it
   - If not → create a new page
5. Update `wiki/index.md`
6. Append to `wiki/log.md`: date, batch covered, pages created/updated, key patterns

### Query
When user asks a question:
1. Read `wiki/index.md` to find relevant event/actor/theme pages
2. If needed, filter `metadata.csv` for relevant article IDs
3. Load wiki pages + sample articles if detail needed
4. Synthesize answer with `[[wikilinks]]`
5. If answer reveals new synthesis: proactively save as `wiki/overview/` page
6. Append to `wiki/log.md`

### Lint
Scan for:
- **Coverage gaps**: events in `metadata.csv` with no wiki page
- **Stale pages**: wiki pages not updated after a major new batch
- **Orphan pages**: no incoming `[[wikilinks]]`
- **Missing actors**: actors mentioned in event pages but with no actor page
- **Unlinked themes**: themes described in event pages but no standalone theme page

Output severity report (HIGH/MEDIUM/LOW). Append to `wiki/log.md`.

---

## metadata.csv Columns

Required: `id`, `date`, `outlet`, `title`, `filename`  
Optional (fill progressively): `tags`, `url`, `sentiment`, `event_id`

```
id,date,outlet,title,filename,tags,url,sentiment,event_id
001,2025-01-15,自由時報,罷免連署突破門檻,raw/news/2025-01/001.md,recall;KMT,,negative,2025-recall-wave
```

---

## Working Principles

**Articles are evidence; wiki pages are knowledge.** Never create a wiki page just to mirror an article. Ask: "What does this article tell me about an event, actor, or theme?"

**metadata.csv is your search index.** Filter it with grep or Python before loading articles into context. Never try to read the entire corpus at once.

**analysis/ is for programs, wiki/ is for Claude.** Python computes frequencies, sentiment, entity counts. Claude interprets, synthesizes, and cross-links.

**Every wiki claim cites article IDs.** Trace claims to `metadata.csv` IDs so you can pull the original article later.

**log.md is append-only.** Never edit past entries.
