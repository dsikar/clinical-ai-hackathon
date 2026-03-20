import base64
import logging
import shutil
import sys
import tempfile
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "baseline-solution" / "src"
TEMP_DIR = ROOT_DIR / "tmp"
TEMP_DIR.mkdir(exist_ok=True)
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from pipeline_claude import run_pipeline as run_claude_pipeline  # type: ignore  # noqa: E402
from .analyse import analyse as analyse_workbook, print_report as render_text_report  # type: ignore  # noqa: E402


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mdt_api")


app = FastAPI(title="Clinical AI MDT Extractor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _cleanup_file(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except Exception:
        pass


@app.post("/extract")
async def extract_workbook(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".docx"):
        logger.warning("Rejected upload: invalid filename %s", file.filename)
        raise HTTPException(status_code=400, detail="Please upload a DOCX file.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx", dir=TEMP_DIR) as tmp_docx:
            shutil.copyfileobj(file.file, tmp_docx)
            source_path = Path(tmp_docx.name)
        logger.info("Saved upload to %s", source_path)
    except Exception as exc:
        logger.exception("Failed to persist uploaded file: %s", exc)
        raise HTTPException(status_code=500, detail=f"Failed to save upload: {exc}") from exc
    finally:
        await file.close()

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx", dir=TEMP_DIR) as tmp_xlsx:
            excel_path = Path(tmp_xlsx.name)
        logger.info("Running pipeline for %s -> %s", source_path, excel_path)
        run_claude_pipeline(docx_input=source_path, output_workbook=excel_path)
        logger.info("Generated workbook at %s", excel_path)

        results = analyse_workbook(str(excel_path))
        report_text = render_text_report(results)
        excel_bytes = excel_path.read_bytes()
        excel_b64 = base64.b64encode(excel_bytes).decode("utf-8")

        background_tasks.add_task(_cleanup_file, source_path)
        background_tasks.add_task(_cleanup_file, excel_path)

        return JSONResponse(
            {
                "report": report_text,
                "results": results,
                "workbook_base64": excel_b64,
            }
        )
    except Exception as exc:
        logger.exception("Extraction failed: %s", exc)
        if 'source_path' in locals():
            _cleanup_file(source_path)
        if 'excel_path' in locals():
            _cleanup_file(excel_path)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {exc}") from exc
