"""
Summarize a month's articles from metadata.csv.
Usage: python summarize_month.py --month 2025-01
Outputs a summary CSV to analysis/results/YYYY-MM-summary.csv
"""

import argparse
import csv
import os
from collections import Counter
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    parser.add_argument("--metadata", default="metadata.csv")
    args = parser.parse_args()

    root = Path(__file__).parent.parent.parent
    metadata_path = root / args.metadata
    output_dir = root / "analysis" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    with open(metadata_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"].startswith(args.month):
                rows.append(row)

    if not rows:
        print(f"No articles found for {args.month}")
        return

    # Outlet frequency
    outlets = Counter(r["outlet"] for r in rows)

    # Tag frequency
    tags = Counter()
    for r in rows:
        for tag in r.get("tags", "").split(";"):
            tag = tag.strip()
            if tag:
                tags[tag] += 1

    # Sentiment distribution
    sentiments = Counter(r.get("sentiment", "unknown") for r in rows)

    # Write summary
    output_path = output_dir / f"{args.month}-summary.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "count"])
        writer.writerow(["total_articles", args.month, len(rows)])
        writer.writerow([])
        writer.writerow(["--- outlets ---", "", ""])
        for outlet, count in outlets.most_common():
            writer.writerow(["outlet", outlet, count])
        writer.writerow([])
        writer.writerow(["--- tags ---", "", ""])
        for tag, count in tags.most_common(20):
            writer.writerow(["tag", tag, count])
        writer.writerow([])
        writer.writerow(["--- sentiment ---", "", ""])
        for sentiment, count in sentiments.most_common():
            writer.writerow(["sentiment", sentiment, count])

    print(f"Summary written to {output_path}")
    print(f"Total articles: {len(rows)}")
    print(f"Top outlets: {dict(outlets.most_common(5))}")
    print(f"Top tags: {dict(tags.most_common(10))}")

if __name__ == "__main__":
    main()
