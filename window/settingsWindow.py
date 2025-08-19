from __future__ import annotations
from PyQt6 import QtCore, QtGui, QtWidgets
from pathlib import Path
import json, os

# ---------- config helpers ----------
def user_config_dir() -> Path:
    return Path("C:/PDF_Creator")

def user_config_path() -> Path:
    return user_config_dir() / "config.json"

def ensure_config_dir() -> Path:
    cfg_dir = user_config_dir()
    cfg_dir.mkdir(parents=True, exist_ok=True)
    return cfg_dir

def atomic_write_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def load_api_path() -> str | None:
    cfg = user_config_path()
    try:
        if cfg.exists():
            return json.loads(cfg.read_text(encoding="utf-8")).get("api_path") or None
    except Exception:
        pass
    return None

def save_api_path(api_path: str) -> Path:
    cfg_dir = ensure_config_dir()
    cfg = cfg_dir / "config.json"
    atomic_write_json(cfg, {"api_path": api_path})
    return cfg


# ---------- drag & drop field ----------
class ExeDropField(QtWidgets.QFrame):
    fileDropped = QtCore.pyqtSignal(str)
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("ExeDropField")
        self.setAcceptDrops(True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(120)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)  # ONLY padding we keep
        lay.setSpacing(6)

        self._icon = QtWidgets.QLabel(self)
        self._icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._icon.setText("📂")
        self._icon.setStyleSheet("font-size:28px; padding:6px; border:0px;")
        lay.addWidget(self._icon)

        self._label = QtWidgets.QLabel(
            "Drop <b>winword.exe</b> or <b>soffice.exe</b> here<br>(or click to browse)",
            self
        )
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._label.setObjectName("dropHint")
        lay.addWidget(self._label)

    def set_hint(self, text: str):
        self._label.setText(text)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QtGui.QDropEvent):
        for url in e.mimeData().urls():
            p = url.toLocalFile()
            if p:
                self.fileDropped.emit(p)
                return

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.clicked.emit()
        super().mousePressEvent(e)


# ---------- settings dialog ----------
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("SettingsDialog")
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(560)

        # Styles: border 0 everywhere, dashed border only on ExeDropField
        self.setStyleSheet("""
#SettingsDialog{ background:#f7f9fc; padding:6px; }
#Card{ background:#ffffff; border:0px; border-radius:0px; padding:6px; }
#title{ font-size:16px; font-weight:700; color:#1f2937; padding:6px; border:0px; }
#hintPath{ color:#64748b; font-size:11px; padding:6px; border:0px; }
QLineEdit{ background:#fafafa; border:0px; border-radius:0px; padding:6px; font-size:13px; }
QLineEdit:focus{ border:0px; }
QPushButton{ border:0px; border-radius:6px; padding:6px; font-weight:600; font-size:13px; }
QPushButton#btnBrowse{ background:#eef2ff; color:#4338ca; }
QPushButton#btnBrowse:hover{ background:#e0e7ff; }
QPushButton#btnSave{ background:#2563eb; color:white; }
QPushButton#btnSave:hover{ background:#1d4ed8; }
#ExeDropField{ background:#fafafa; border:2px dashed #cbd5e1; border-radius:10px; }
#ExeDropField:hover{ background:#f3f4f6; }
QLabel#dropHint{ color:#475569; font-size:13px; padding:6px; border:0px; }
""")

        # Root layout – no margins/spacing
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        card = QtWidgets.QFrame(self)
        card.setObjectName("Card")
        root.addWidget(card)

        c = QtWidgets.QVBoxLayout(card)
        c.setContentsMargins(0, 0, 0, 0)
        c.setSpacing(8)

        title = QtWidgets.QLabel("Choose an API to convert the files", card)
        title.setObjectName("title")
        c.addWidget(title)

        self.drop = ExeDropField(card)
        c.addWidget(self.drop)

        # Path row
        rowPath = QtWidgets.QHBoxLayout()
        rowPath.setContentsMargins(0, 0, 0, 0)
        rowPath.setSpacing(4)
        self.linePath = QtWidgets.QLineEdit(card)
        self.linePath.setReadOnly(True)
        self.linePath.setPlaceholderText("Drop winword.exe or soffice.exe (or click the box to browse)")
        rowPath.addWidget(self.linePath)

        self.btnCopy = QtWidgets.QToolButton(card)
        self.btnCopy.setToolTip("Copy path")
        self.btnCopy.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnCopy.setText("⧉")
        self.btnCopy.setAutoRaise(True)
        rowPath.addWidget(self.btnCopy)
        c.addLayout(rowPath)

        # Buttons row
        actions = QtWidgets.QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(6)
        actions.addStretch(1)

        self.btnBrowse = QtWidgets.QPushButton("Browse…", card)
        self.btnBrowse.setObjectName("btnBrowse")
        actions.addWidget(self.btnBrowse)

        self.btnSave = QtWidgets.QPushButton("Save", card)
        self.btnSave.setObjectName("btnSave")
        actions.addWidget(self.btnSave)

        c.addLayout(actions)

        hint = QtWidgets.QLabel(f"Will save to: {user_config_path()}", card)
        hint.setObjectName("hintPath")
        c.addWidget(hint)

        # Prefill old config
        old = load_api_path()
        if old:
            self.drop.set_hint(os.path.basename(old))
            self.linePath.setText(old)

        # Hooks
        self.drop.fileDropped.connect(self._on_drop)
        self.drop.clicked.connect(self._browse)
        self.btnBrowse.clicked.connect(self._browse)
        self.btnSave.clicked.connect(self._save)
        self.btnCopy.clicked.connect(self._copy_path)

    # --- actions ---
    def _copy_path(self):
        text = self.linePath.text().strip()
        if text:
            QtWidgets.QApplication.clipboard().setText(text)
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), "Copied", self.btnCopy, QtCore.QRect(), 1200
            )

    def _on_drop(self, path: str):
        norm = self._normalize_candidate(path)
        if self._validate_candidate(norm):
            self.linePath.setText(norm)

    def _browse(self):
        start_dir = os.environ.get("ProgramFiles", "C:\\")
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose converter executable",
            start_dir, "Executables (*.exe);;All Files (*.*)"
        )
        if path:
            norm = self._normalize_candidate(path)
            if self._validate_candidate(norm):
                self.linePath.setText(norm)

    def _normalize_candidate(self, path: str) -> str:
        p = path.strip().strip('"').strip("'")
        p = os.path.expandvars(p)
        return str(Path(p))

    def _validate_candidate(self, path: str) -> bool:
        p = Path(path)
        if not (p.exists() and p.is_file()):
            QtWidgets.QMessageBox.warning(self, "Invalid file", "The selected path is not a file.")
            return False
        if p.suffix.lower() != ".exe":
            QtWidgets.QMessageBox.warning(self, "Invalid file", "Please choose an executable (.exe).")
            return False
        base = p.name.lower()
        if base not in ("winword.exe", "soffice.exe"):
            QtWidgets.QMessageBox.information(
                self, "Note",
                "This doesn't look like winword.exe or soffice.exe.\n"
                "You can still save it if you know what you’re doing."
            )
        return True

    def _save(self):
        val = self.linePath.text().strip()
        if not val:
            QtWidgets.QMessageBox.warning(self, "Nothing to save", "Please choose a file first.")
            return
        try:
            cfg_path = save_api_path(val)
            QtWidgets.QMessageBox.information(self, "Saved", f"Saved to:\n{cfg_path}")
            self.accept()
        except PermissionError:
            QtWidgets.QMessageBox.critical(
                self, "Permission denied",
                "Windows blocked writing to C:\\PDF_Creator.\n"
                "Run the app as Administrator or choose another folder."
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"{type(e).__name__}: {e}")
