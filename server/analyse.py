"""
MDT Database Coverage Analyser
================================
Reads the generated Excel database and produces:
  - Overall fill stats (total cells, filled, empty, %)
  - Per-category breakdown (Demographics, Endoscopy, MRI, CT, etc.)
  - Per-column detail (how many of 50 patients have each field filled)
  - Optional category coverage chart saved as an image

Usage:
    python analyse_database.py
    python analyse_database.py --file path/to/your_database.xlsx
    python analyse_database.py --file path/to/your_database.xlsx --sheet "Sheet1"
    python analyse_database.py --output report.txt   (also saves to a text file)
    python analyse_database.py --chart coverage.png  (also saves a chart image)
"""

import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas is not installed. Run:  pip install pandas openpyxl")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Column → Category mapping
# Each entry is (keyword_in_column_name, category_label)
# Checked in order — first match wins.
# ---------------------------------------------------------------------------
CATEGORY_RULES = [
    ("Demographics",                        "Demographics"),
    ("Endoscop",                            "Endoscopy"),
    ("Histology",                           "Histology / Pathology"),
    ("Baseline MRI",                        "Baseline MRI"),
    ("Baseline CT",                         "Baseline CT"),
    ("1st MDT",                             "1st MDT"),
    ("Chemotherapy",                        "Chemotherapy"),
    ("Immunotherapy",                       "Immunotherapy"),
    ("Radioth",                             "Radiotherapy"),
    ("CEA",                                 "CEA / Blood Markers"),
    ("Surgery",                             "Surgery"),
    ("2nd MRI",                             "2nd MRI (Post-Treatment)"),
    ("MDT (after 6",                        "MDT After 6 Weeks"),
    ("12 week MRI",                         "12-Week MRI"),
    ("Flex sig",                            "Flexible Sigmoidoscopy"),
    ("MDT (after 12",                       "MDT After 12 Weeks"),
    ("Watch and wait",                      "Watch & Wait"),
    ("MRI and flexisigmoidoscopy",          "Watch & Wait Follow-up Scans"),
]

FILL_THRESHOLDS = {
    "Full":    (90, 101),   # ≥ 90%
    "Good":    (50,  90),   # 50–89%
    "Partial": (10,  50),   # 10–49%
    "Low":     ( 1,  10),   # 1–9%
    "Empty":   ( 0,   1),   # 0%
}

STATUS_ICONS = {
    "Full":    "✓",
    "Good":    "~",
    "Partial": "△",
    "Low":     "▽",
    "Empty":   "✗",
}


def categorise_column(col_name: str) -> str:
    for keyword, label in CATEGORY_RULES:
        if keyword.lower() in col_name.lower():
            return label
    return "Other"


def fill_status(pct: float) -> str:
    for label, (lo, hi) in FILL_THRESHOLDS.items():
        if lo <= pct < hi:
            return label
    return "Empty"


def bar(filled: int, total: int, width: int = 30) -> str:
    ratio = filled / total if total else 0
    filled_chars = round(ratio * width)
    return "[" + "█" * filled_chars + "░" * (width - filled_chars) + "]"


def analyse(file_path: str, sheet_name: str | None = None) -> dict:
    path = Path(file_path)
    if not path.exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    print(f"\nReading: {path.name} ...")
    kwargs = {"sheet_name": sheet_name} if sheet_name else {}
    try:
        df = pd.read_excel(file_path, **kwargs)
    except Exception as e:
        print(f"ERROR reading file: {e}")
        sys.exit(1)

    total_rows = len(df)
    total_cols = len(df.columns)
    total_cells = total_rows * total_cols
    filled_cells = int(df.notna().sum().sum())
    empty_cells = total_cells - filled_cells
    overall_pct = (filled_cells / total_cells * 100) if total_cells else 0

    # --- Per-column stats ---------------------------------------------------
    col_stats = []
    for col in df.columns:
        n_filled = int(df[col].notna().sum())
        pct = (n_filled / total_rows * 100) if total_rows else 0
        col_stats.append({
            "column":   col,
            "category": categorise_column(col),
            "filled":   n_filled,
            "total":    total_rows,
            "pct":      pct,
            "status":   fill_status(pct),
        })

    # --- Per-category rollup ------------------------------------------------
    from collections import defaultdict
    cat_data = defaultdict(lambda: {"cols": 0, "filled": 0, "total_cells": 0})
    for cs in col_stats:
        cat = cs["category"]
        cat_data[cat]["cols"]        += 1
        cat_data[cat]["filled"]      += cs["filled"]
        cat_data[cat]["total_cells"] += cs["total"]

    cat_stats = []
    for cat, d in cat_data.items():
        pct = (d["filled"] / d["total_cells"] * 100) if d["total_cells"] else 0
        cat_stats.append({
            "category":    cat,
            "columns":     d["cols"],
            "filled":      d["filled"],
            "total_cells": d["total_cells"],
            "pct":         pct,
            "status":      fill_status(pct),
        })
    cat_stats.sort(key=lambda x: -x["pct"])

    # --- Status counts -------------------------------------------------------
    status_counts = {}
    for label in FILL_THRESHOLDS:
        status_counts[label] = sum(1 for cs in col_stats if cs["status"] == label)

    return {
        "file":          path.name,
        "rows":          total_rows,
        "cols":          total_cols,
        "total_cells":   total_cells,
        "filled_cells":  filled_cells,
        "empty_cells":   empty_cells,
        "overall_pct":   overall_pct,
        "col_stats":     col_stats,
        "cat_stats":     cat_stats,
        "status_counts": status_counts,
    }


def print_report(r: dict) -> str:
    lines = []
    W = 72

    def line(text=""):
        lines.append(text)

    def ruler(char="─"):
        lines.append(char * W)

    def heading(text):
        ruler("═")
        lines.append(f"  {text}")
        ruler("═")

    # ── Header ──────────────────────────────────────────────────────────────
    heading(f"MDT DATABASE COVERAGE REPORT   {r['file']}")
    line()

    # ── Overall stats ────────────────────────────────────────────────────────
    line("OVERALL SUMMARY")
    ruler()
    line(f"  Patients (rows)      : {r['rows']}")
    line(f"  Data fields (columns): {r['cols']}")
    line(f"  Total possible cells : {r['total_cells']:,}")
    line(f"  Filled cells         : {r['filled_cells']:,}  ({r['overall_pct']:.1f}%)")
    line(f"  Empty cells          : {r['empty_cells']:,}  ({100 - r['overall_pct']:.1f}%)")
    line()
    line(f"  Overall fill rate    : {bar(r['filled_cells'], r['total_cells'])}  {r['overall_pct']:.1f}%")
    line()

    # ── Column status counts ─────────────────────────────────────────────────
    line("COLUMN STATUS BREAKDOWN")
    ruler()
    sc = r["status_counts"]
    for label, icon in STATUS_ICONS.items():
        count = sc.get(label, 0)
        pct = count / r["cols"] * 100
        line(f"  {icon} {label:<8}  {count:3d} columns  ({pct:.0f}%)")
    line()

    # ── Per-category breakdown ────────────────────────────────────────────────
    line("BY CATEGORY")
    ruler()
    line(f"  {'Category':<38} {'Cols':>4}  {'Filled':>8}  {'Rate':>6}  Status")
    ruler()
    for cs in r["cat_stats"]:
        icon = STATUS_ICONS[cs["status"]]
        frac = f"{cs['filled']}/{cs['total_cells']}"
        line(
            f"  {icon} {cs['category']:<37} {cs['columns']:>4}  "
            f"{frac:>8}  {cs['pct']:>5.1f}%"
        )
    line()

    # ── Per-column detail ─────────────────────────────────────────────────────
    line("COLUMN-BY-COLUMN DETAIL")
    ruler()
    current_cat = None
    for cs in r["col_stats"]:
        if cs["category"] != current_cat:
            current_cat = cs["category"]
            line()
            line(f"  ── {current_cat} ──")
        icon  = STATUS_ICONS[cs["status"]]
        short = cs["column"].replace("\n", " ")[:52]
        b     = bar(cs["filled"], cs["total"], width=20)
        line(f"    {icon} {short:<52}  {b}  {cs['filled']:2d}/{cs['total']}")
    line()

    ruler("═")
    line("  Legend:  ✓ Full (≥90%)   ~ Good (50-89%)   △ Partial (10-49%)")
    line("           ▽ Low (1-9%)    ✗ Empty (0%)")
    ruler("═")

    report_text = "\n".join(lines)
    print(report_text)
    return report_text


def render_category_chart(results: dict, output_path: str):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("WARNING: matplotlib is not installed. Run `pip install matplotlib` to generate charts.")
        return

    categories = [cs["category"] for cs in results["cat_stats"]]
    percentages = [cs["pct"] for cs in results["cat_stats"]]

    fig_height = max(4, 0.4 * len(categories))
    fig, ax = plt.subplots(figsize=(10, fig_height))
    bars = ax.barh(categories, percentages, color="#2563eb")
    ax.set_xlabel("Fill rate (%)")
    ax.set_title(f"MDT Coverage by Category — {results['file']}")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", alpha=0.2)

    for bar, pct in zip(bars, percentages):
        ax.text(pct + 1, bar.get_y() + bar.get_height() / 2, f"{pct:.1f}%", va="center")

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"\n  Chart saved to: {output_path}")


def save_report(text: str, output_path: str):
    Path(output_path).write_text(text, encoding="utf-8")
    print(f"\n  Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyse fill-rate of a generated MDT Excel database."
    )
    parser.add_argument(
        "--file", "-f",
        default="generated-database.xlsx",
        help="Path to the Excel file (default: generated-database.xlsx)"
    )
    parser.add_argument(
        "--sheet", "-s",
        default=None,
        help="Sheet name to read (default: first sheet)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Optional path to save the report as a .txt file"
    )
    parser.add_argument(
        "--chart", "-c",
        default=None,
        help="Optional path to save a category coverage chart (PNG)"
    )
    args = parser.parse_args()

    results = analyse(args.file, args.sheet)
    report  = print_report(results)

    if args.output:
        save_report(report, args.output)

    if args.chart:
        render_category_chart(results, args.chart)


if __name__ == "__main__":
    main()
