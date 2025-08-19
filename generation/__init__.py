from . import docx_to_pdf, ppt_to_pdf, pdf_to_docx
from .utils import EXT_MAP, guess_ext

_CONVERTERS = {
    ("docx", "pdf"): docx_to_pdf.convert,
    ("ppt", "pdf"): ppt_to_pdf.convert,
    ("pptx", "pdf"): ppt_to_pdf.convert,
    ("pdf", "docx"): pdf_to_docx.convert,
}

def get_converter(src_ext: str, dst_ext: str):
    key = (src_ext.lower(), dst_ext.lower())
    if key not in _CONVERTERS:
        raise RuntimeError(f"Unsupported conversion {src_ext} → {dst_ext}")
    return _CONVERTERS[key]

def available_targets_for(src_ext: str):
    s = src_ext.lower()
    return [dst for (src, dst) in _CONVERTERS.keys() if src == s]
