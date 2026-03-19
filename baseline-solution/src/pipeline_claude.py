import argparse
import re
from pathlib import Path

import pandas as pd

from claude_extract_fields import extract_case_fields_claude
from load_docx import load_cases
from write_excel import write_styled_workbook


ROOT_DIR = Path(__file__).resolve().parents[2]
BASELINE_SOLUTION_DIR = ROOT_DIR / "baseline-solution"
OUTPUT_WORKBOOK = BASELINE_SOLUTION_DIR / "output" / "generated-database-claude.xlsx"
DOCX_INPUT = ROOT_DIR / "data" / "hackathon-mdt-outcome-proformas.docx"
PROTOTYPE_WORKBOOK = ROOT_DIR / "data" / "hackathon-database-prototype.xlsx"


def _extract_document_mdt_date(doc):
    for paragraph in doc.paragraphs:
        if "Multidisciplinary Meeting" in paragraph.text:
            match = re.search(r"(\d{2}/\d{2}/\d{4})\(i\)", paragraph.text)
            if match:
                return match.group(1)
    return ""


def run_pipeline(docx_input: Path = DOCX_INPUT, output_workbook: Path = OUTPUT_WORKBOOK, prototype_workbook: Path = PROTOTYPE_WORKBOOK) -> Path:
    docx_input = Path(docx_input)
    output_workbook = Path(output_workbook)
    prototype_workbook = Path(prototype_workbook)

    cases, doc = load_cases(str(docx_input))
    print(f"Loaded {len(cases)} cases from {docx_input}.")

    doc_date = _extract_document_mdt_date(doc)
    if doc_date:
        print(f"Found MDT Date: {doc_date}")

    extracted_data = [extract_case_fields_claude(case, doc_date=doc_date) for case in cases]
    dataframe = pd.DataFrame(extracted_data)

    template_columns = list(pd.read_excel(prototype_workbook, sheet_name=0).columns)
    dataframe = dataframe.reindex(columns=template_columns)

    if "Demographics: \nNHS number(d)" in dataframe.columns and "1st MDT: date(i)" in dataframe.columns:
        dataframe = dataframe.sort_values(
            by=["Demographics: \nNHS number(d)", "1st MDT: date(i)"],
            na_position="last",
        ).reset_index(drop=True)

    write_styled_workbook(dataframe, prototype_workbook, output_workbook)
    print(f"Generated workbook saved to {output_workbook}")
    return output_workbook


def main():
    parser = argparse.ArgumentParser(description="Run the Claude extraction pipeline")
    parser.add_argument("--docx", type=str, default=str(DOCX_INPUT), help="Path to the MDT DOCX input file")
    parser.add_argument("--output", type=str, default=str(OUTPUT_WORKBOOK), help="Path to write the generated workbook")
    parser.add_argument(
        "--prototype",
        type=str,
        default=str(PROTOTYPE_WORKBOOK),
        help="Path to the prototype workbook used for column alignment and styling",
    )
    args = parser.parse_args()

    run_pipeline(Path(args.docx), Path(args.output), Path(args.prototype))


if __name__ == "__main__":
    main()
