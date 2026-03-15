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

Two implementation attempts now exist in this directory.

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

## Directory Layout

```text
baseline-solution/
├── README.md
├── work-diary.md
├── prompts/
│   ├── 00-prompt-starter.md
│   └── 01-implementation_plan.md
│   └── 02-claude-code-handoff.md
├── reports/
│   ├── gemini-gap-report.md
│   └── codex-gap-report.md
├── src/
│   ├── codex_extract_fields.py
│   ├── extract_fields.py
│   ├── inspect_artifacts.py
│   ├── load_docx.py
│   ├── pipeline.py
│   ├── pipeline_codex.py
│   ├── validate_output.py
│   └── write_excel.py
├── tests/
│   ├── test_codex_implementation.py
│   └── test_standard_solution.py
└── output/
    ├── generated-database-gemini.xlsx
    └── generated-database-codex.xlsx
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
