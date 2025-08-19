import json, subprocess
from pathlib import Path
import subprocess

CONFIG_PATH = Path("C:/PDF_Creator/config.json")

def get_api_path() -> str:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    api = cfg.get("api_path")
    if not api:
        raise RuntimeError("api_path missing in config.json")
    return api

def run_office_api(args: list[str]):
    api = get_api_path()
    # Silence stdout + stderr completely
    return subprocess.run(
        [api] + args,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW  # hide console window on Windows
    )
