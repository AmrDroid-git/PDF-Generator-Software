from pathlib import Path
import tempfile

def _ensure_pywin32():
    try:
        import win32com.client  # noqa
        import pythoncom        # noqa
    except Exception as e:
        raise RuntimeError("pywin32 is required for Microsoft Office automation. Install with: pip install pywin32") from e

def word_docx_to_pdf(input_path: str, output_path: str):
    _ensure_pywin32()
    import win32com.client, pythoncom
    pythoncom.CoInitialize()
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # wdAlertsNone
        doc = word.Documents.Open(str(Path(input_path).resolve()), ReadOnly=True)
        # 17 = wdFormatPDF
        doc.SaveAs2(str(Path(output_path).resolve()), FileFormat=17)
        doc.Close(False)
    finally:
        if word:
            try: word.Quit()
            except Exception: pass

def word_pdf_to_docx(input_path: str, output_path: str):
    _ensure_pywin32()
    import win32com.client, pythoncom
    pythoncom.CoInitialize()
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        doc = word.Documents.Open(str(Path(input_path).resolve()), ConfirmConversions=False, ReadOnly=True)
        # 16 = wdFormatDocumentDefault (DOCX)
        doc.SaveAs2(str(Path(output_path).resolve()), FileFormat=16)
        doc.Close(False)
    finally:
        if word:
            try: word.Quit()
            except Exception: pass

def ppt_to_pdf(input_path: str, output_path: str):
    _ensure_pywin32()
    import win32com.client, pythoncom
    pythoncom.CoInitialize()
    ppt = None
    try:
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        ppt.Visible = True
        pres = ppt.Presentations.Open(str(Path(input_path).resolve()), WithWindow=False)
        # 32 = ppSaveAsPDF
        pres.SaveAs(str(Path(output_path).resolve()), 32)
        pres.Close()
    finally:
        if ppt:
            try: ppt.Quit()
            except Exception: pass
