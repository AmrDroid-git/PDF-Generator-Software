from pathlib import Path
import tempfile
from .api_runner import get_api_path
from .utils import ensure_parent_dir, remove_if_exists, atomic_move_with_retries
from .win_com import word_pdf_to_docx

def _convert_with_pdf2docx(input_path: str, output_path: str):
    try:
        from pdf2docx import Converter
    except Exception as e:
        raise RuntimeError("pdf2docx is required. Install with: pip install pdf2docx") from e

    ensure_parent_dir(output_path)
    remove_if_exists(output_path)

    with tempfile.TemporaryDirectory(prefix="pdf2docx_") as td:
        tmp_out = str((Path(td) / (Path(output_path).stem + ".docx")).resolve())
        cv = Converter(str(Path(input_path).resolve()))
        try:
            # pdf2docx already quiet; no prints unless debug=True
            cv.convert(tmp_out, start=0, end=None)
        finally:
            cv.close()
        atomic_move_with_retries(tmp_out, output_path)

def convert(input_path: str, output_path: str):
    api = get_api_path().lower()
    if "winword" in api:
        word_pdf_to_docx(input_path, output_path)
    else:
        _convert_with_pdf2docx(input_path, output_path)
