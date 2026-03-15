# Baseline Solution

Author: Codex

## Purpose

This directory contains the baseline-solution work for the hackathon problem:
- prompts and handoff rules
- implementation attempts
- generated workbooks
- gap-analysis reports
- a running work diary

The target remains the same:
- read [`../data/hackathon-mdt-outcome-proformas.docx`](../data/hackathon-mdt-outcome-proformas.docx)
- generate a longitudinal Excel workbook aligned as closely as possible with [`../data/hackathon-database-prototype.xlsx`](../data/hackathon-database-prototype.xlsx)

## Current Status

Three implementation attempts now exist in this directory.

### Gemini Attempt

Gemini produced an initial working pipeline and workbook export.

Relevant files:
- [`src/extract_fields.py`](./src/extract_fields.py)
- [`src/pipeline.py`](./src/pipeline.py)
- [`reports/gemini-gap-report.md`](./reports/gemini-gap-report.md)

What it achieved:
- segmented the `.docx` into 50 cases
- aligned workbook columns to the prototype schema
- produced an initial generated workbook

Main gaps found:
- low extraction coverage
- many clinically important columns left blank
- weak validation logic
- output initially looked like a generic pandas export rather than the clinician-prepared workbook

See:
- [`reports/gemini-gap-report.md`](./reports/gemini-gap-report.md)

### Codex Attempt

I created a separate alternative implementation rather than patching Gemini's extractor in place.

Relevant files:
- [`src/codex_extract_fields.py`](./src/codex_extract_fields.py)
- [`src/pipeline_codex.py`](./src/pipeline_codex.py)
- [`src/write_excel.py`](./src/write_excel.py)
- [`reports/codex-gap-report.md`](./reports/codex-gap-report.md)

Improvements made:
- materially better extraction coverage than the Gemini attempt
- separate Codex extractor for clearer comparison
- workbook styling replicated from the prototype so the output looks familiar to clinicians
- agent-suffixed output naming convention

Measured improvements:
- Gemini non-empty cells: `127`
- Codex non-empty cells: `661`
- Gemini best normalized match to the populated prototype row: `8/12`
- Codex best normalized match to the populated prototype row: `10/12`

Main remaining gaps:
- `Endoscopy: date(f)` still not extracted
- `Histology: Biopsy date(g)` still not extracted
- 61 target columns remain empty
- follow-up, treatment-course, and later-pathway fields remain largely unimplemented
- some normalized fields are still heuristic rather than fully reliable

See:
- [`reports/codex-gap-report.md`](./reports/codex-gap-report.md)

### Claude Code Attempt

Relevant files:
- [`src/claude_extract_fields.py`](./src/claude_extract_fields.py)
- [`src/pipeline_claude.py`](./src/pipeline_claude.py)
- [`tests/test_claude_implementation.py`](./tests/test_claude_implementation.py)

Improvements over Codex:
- endoscopy date extracted from `TYPE DATE:` pattern (not only `TYPE on DATE:`)
- histology biopsy date inferred from dated colonoscopy when findings mention cancer/biopsy
- CT date broadened to match `CT abdomen`, `CT pelvis`, and other CT qualifiers
- MDT decision field extracts text after "Outcome:" label when present

Measured improvement over Codex:
- Codex non-empty cells: `661`
- Claude non-empty cells: `675`
- `Baseline CT: Date(h)`: 19 → 27 (+8 rows)
- `Endoscopy: date(f)`: 0 → 2 (+2 rows)
- `Histology: Biopsy date(g)`: 0 → 1 (+1 row)

Tests: 12 targeted tests pass, including regression guards from the Codex path.

Main remaining gaps:
- `Histology: Biopsy date(g)` populated for only 1 row — no recoverable evidence in the remaining 49
- 61+ target columns still empty (chemotherapy, radiotherapy, immunotherapy, CEA, surgery, second MRI, follow-up pathway fields)
- MDT decision normalization only applies to the 3 cases with an explicit "Outcome:" label

## Directory Layout

```text
baseline-solution/
├── README.md
├── work-diary.md
├── prompts/
│   ├── 00-prompt-starter.md
│   ├── 01-implementation_plan.md
│   ├── 02-claude-code-handoff.md
│   └── ... (agent-specific prompts)
├── reports/
│   ├── colorectal-cancer-primer.md
│   ├── codex-gap-report.md
│   ├── gemini-gap-report.md
│   ├── deep-research-claude.docx
│   ├── deep-research-gemini.docx
│   ├── deep-research-grok.md
│   └── ... (LLM research artifacts)
├── src/
│   ├── claude_extract_fields.py
│   ├── codex_extract_fields.py
│   ├── extract_fields.py
│   ├── inspect_artifacts.py
│   ├── load_docx.py
│   ├── pipeline.py
│   ├── pipeline_claude.py
│   ├── pipeline_codex.py
│   ├── validate_output.py
│   └── write_excel.py
├── tests/
│   ├── test_claude_implementation.py
│   ├── test_codex_implementation.py
│   └── test_standard_solution.py
└── output/
    ├── generated-database-claude.xlsx
    ├── generated-database-codex.xlsx
    └── generated-database-gemini.xlsx
```

## Prompts

Start with [`prompts/00-prompt-starter.md`](./prompts/00-prompt-starter.md).

Use [`prompts/01-implementation_plan.md`](./prompts/01-implementation_plan.md) only when the user explicitly asks for implementation work to continue.

Use [`prompts/02-claude-code-handoff.md`](./prompts/02-claude-code-handoff.md) when handing the current state to Claude Code for continuation.

## Work Diary

The running handoff log is:
- [`work-diary.md`](./work-diary.md)

## Author Attribution

This baseline-solution scaffold and the Codex implementation path were authored by Codex.
