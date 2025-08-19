from pathlib import Path
import tempfile
from .api_runner import get_api_path, run_office_api
from .utils import ensure_parent_dir, remove_if_exists, atomic_move_with_retries

def convert_with_soffice(input_path: str, output_path: str, to_filter: str):
    """
    Use LibreOffice to convert file, write to a temp dir, then atomically move.
    to_filter examples: 'pdf', 'docx'
    """
    api = get_api_path().lower()
    if "soffice" not in api:
        raise RuntimeError("Configured API is not LibreOffice (soffice).")

    src = Path(input_path)
    dst = Path(output_path)
    target_suffix = "." + dst.suffix.lstrip(".").lower()

    ensure_parent_dir(output_path)
    remove_if_exists(output_path)

    with tempfile.TemporaryDirectory(prefix="lo_convert_") as tmpdir:
        run_office_api([
            "--headless", "--norestore", "--nolockcheck", "--nodefault",
            "--convert-to", to_filter,
            "--outdir", tmpdir,
            str(src)
        ])
        produced = Path(tmpdir) / (src.stem + target_suffix)
        if not produced.exists():
            # Fallback: any file with same stem and right suffix
            for c in Path(tmpdir).glob(src.stem + ".*"):
                if c.suffix.lower() == target_suffix:
                    produced = c
                    break
        if not produced.exists():
            raise FileNotFoundError(f"LibreOffice did not produce expected file: {produced}")
        atomic_move_with_retries(str(produced), str(dst))
