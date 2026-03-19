# 06 Print Scoring Rubric Prompt

Author: Claude Code

## Prompt Purpose

Use this prompt to instruct an agent or developer to create a print-ready scoring rubric
sheet for the Clinical AI Hackathon judges.

## Existing Source Material

The scoring criteria already defined in `docs/judging-criteria.md` must be used as the
authoritative source. The key content is reproduced below for reference.

### Scoring Scale (1–4)

| Score | Meaning |
|-------|---------|
| **1** | Not all core requirements implemented — major gaps; does not fully solve the task |
| **2** | All core requirements implemented — works end-to-end, accurate/useful Excel output, solid level |
| **3** | Surpassed expectations — noticeably better: clever features, polish, real-world ready |
| **4** | Blew my mind — exceptional: innovative, clinically transformative, wow factor |

**Guidance for a score of 4:** Use sparingly for projects that genuinely surprise or impress
— e.g., unusually accurate/safe extraction on tricky real-world cases, smart clinician-friendly
additions (confidence flags, summaries), elegant handling of edge cases, or clear potential to
save serious time/errors in NHS/MoD workflows. It should feel like *"this could actually change
how we work"*.

### Scoring Categories

The three prize categories that need a score are:

1. **Documentation** — clarity, completeness, reproducibility, quality of written artefacts
2. **Presentation** — delivery, clarity of explanation, ability to answer questions
3. **Code** — correctness, structure, readability, robustness, clinical safety of extraction

An **Overall Winner** is determined from the combined scores across all three categories.

### Judges

- Dr. Anita Wale — Consultant Radiologist, St George's University Hospitals NHS Foundation Trust
- Dr. Alex Nicholls — Ministry of Defence
- Hitesh Patel — Superintendent Radiographer and Radiology IT Systems Manager, St George's

### Teams

Up to 6 teams will be scored.

---

## Prompt

Create a single print-ready HTML file containing the scoring rubric for the Clinical AI
Hackathon judges.

### Layout

The document should fit on **one or two A4 pages** (210mm × 297mm) in portrait orientation
and contain the following sections in order:

#### 1. Header

- Event name: **Clinical AI Hackathon**
- Title: **Judge Scoring Sheet**
- A field for the judge to write their name: `Judge: ___________________________`
- A field for the date: `Date: ___________________________`

#### 2. Scoring Scale Reference Box

A clearly boxed reference section showing the 1–4 scale with the label for each score, as
specified above. Include the guidance note for score 4 in smaller italic text beneath the
table. This box must appear at the top of the scoring sheet so judges can refer to it while
scoring without turning the page.

#### 3. Scoring Table

A table with the following columns:

| Team # / Name | Documentation (1–4) | Presentation (1–4) | Code (1–4) | Total (3–12) | Notes |
|---------------|--------------------|--------------------|------------|--------------|-------|

- Six rows (one per team), with alternating light background shading for readability.
- The **Total** column should have enough space for the judge to write the sum.
- The **Notes** column should be wide enough for a short handwritten comment (at least 4 cm).
- All score cells should be large enough to write a single digit clearly (minimum 1.5 cm wide).

#### 4. Prize Category Summary

A small section below the table with four boxes, one per prize, for the judge to record their
recommended winner after scoring is complete:

- Best Documentation → `Winner: ___________________________`
- Best Presentation → `Winner: ___________________________`
- Best Code → `Winner: ___________________________`
- Overall Winner → `Winner: ___________________________`

#### 5. Footer

A small footer with the text:
*"Clinical AI Hackathon — Confidential judge scoring sheet"*

### Design Requirements

- Clean, professional, print-friendly style — black text on white background.
- Use a sans-serif font (e.g. Arial, Helvetica, or a Google Font such as Inter or Source Sans Pro).
- The scoring scale reference box should have a visible border and a light grey background to
  distinguish it from the table.
- All styling must be in a `<style>` block within the single HTML file — no external
  dependencies that require an internet connection at print time.
- Include a `@media print` CSS block that:
  - Sets paper size to A4 portrait (`@page { size: A4 portrait; margin: 15mm; }`)
  - Hides any browser UI elements
  - Preserves table borders and shading (`-webkit-print-color-adjust: exact; print-color-adjust: exact`)
- The file must print correctly from Chrome, Firefox, and Safari without manual adjustment.

### Output

Save the file as:

```
comms/hackathon-scoring-rubric.html
```

Open it in a browser and use **File → Print** (or Ctrl+P / Cmd+P) to print or save as PDF.
Print one copy per judge (three copies total).

---

## Author Attribution

This prompt was authored by Claude Code.
