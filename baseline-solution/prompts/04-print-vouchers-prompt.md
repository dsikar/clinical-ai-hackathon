# 04 Print Vouchers Prompt

Author: Claude Code

## Prompt Purpose

Use this prompt to instruct an agent or developer to create a print-ready A4 voucher sheet
for the Clinical AI Hackathon prize awards.

---

## Prompt

Create a single print-ready HTML file containing four prize vouchers laid out on one A4 page
(210mm × 297mm) in a 2×2 grid.

### Prize Details

Each voucher is worth **£50**. The four prize categories are:

1. **Best Documentation**
2. **Best Presentation**
3. **Best Code**
4. **Overall Winner**

### Design Requirements

- The page must use A4 dimensions with no visible browser chrome when printed.
- Each voucher must occupy one quarter of the page (approximately 105mm × 148mm).
- Each voucher must display:
  - Event name: **Clinical AI Hackathon**
  - Prize category name (bold, prominent)
  - Prize value: **£50**
  - A short congratulatory line, e.g. *"Awarded in recognition of outstanding achievement"*
  - A blank line labelled **Winner:** for handwriting the recipient's name
  - A blank line labelled **Date:** for handwriting the date
- Vouchers must be separated by a dashed cut line with a small scissors icon (✂) at the corner.
- Use a clean, professional visual style suitable for a formal award:
  - A border or decorative frame on each voucher
  - A consistent colour scheme (suggest dark blue or dark green header bar with white text for
    the category name, white background for the body)
  - A serif or semi-formal font (e.g. Georgia, Palatino, or a Google Font such as Playfair Display)
- All styling must be inline or in a `<style>` block within the single HTML file — no external
  dependencies that require an internet connection at print time.

### Print Requirements

- Include a `@media print` CSS block that:
  - Hides browser headers and footers (`margin: 0`)
  - Ensures the page breaks correctly (one A4 page only)
  - Sets paper size to A4 portrait
  - Preserves background colours and border colours when printed
    (`-webkit-print-color-adjust: exact; print-color-adjust: exact`)
- The file must print correctly from Chrome, Firefox, and Safari without manual adjustment.

### Output

Save the file as:

```
comms/hackathon-prize-vouchers.html
```

Open it in a browser and use **File → Print** (or Ctrl+P / Cmd+P) to print or save as PDF.

---

## Author Attribution

This prompt was authored by Claude Code.
