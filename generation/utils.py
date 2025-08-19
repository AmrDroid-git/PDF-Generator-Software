import os, time, shutil, tempfile
from pathlib import Path

def guess_ext(path: str) -> str:
    return Path(path).suffix.lower().lstrip(".")

def ensure_parent_dir(path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

def remove_if_exists(path: str):
    p = Path(path)
    if p.exists():
        try:
            if p.is_file():
                p.unlink()
            else:
                shutil.rmtree(p)
        except PermissionError:
            pass

def atomic_move_with_retries(src: str, dst: str, retries: int = 12, delay: float = 0.25):
    ensure_parent_dir(dst)
    last_err = None
    for _ in range(retries):
        try:
            try:
                os.replace(src, dst)
            except OSError:
                shutil.move(src, dst)
            return
        except (PermissionError, OSError) as e:
            last_err = e
            time.sleep(delay)
    raise last_err or RuntimeError("Failed to move file after retries")

EXT_MAP = {"PDF": "pdf", "DOCX": "docx", "PPT": "pptx"}
