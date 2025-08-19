from .api_runner import get_api_path
from .utils import ensure_parent_dir, remove_if_exists
from .soffice_helper import convert_with_soffice
from .win_com import word_docx_to_pdf

def convert(input_path: str, output_path: str):
    api = get_api_path().lower()
    ensure_parent_dir(output_path)
    remove_if_exists(output_path)
    if "soffice" in api:
        convert_with_soffice(input_path, output_path, "pdf")
    elif "winword" in api:
        word_docx_to_pdf(input_path, output_path)
    else:
        raise RuntimeError(f"Unsupported API path in config: {api}")
