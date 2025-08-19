from PyQt6 import QtCore, QtGui, QtWidgets
from pathlib import Path
from generation import get_converter, EXT_MAP, available_targets_for
from generation.utils import guess_ext
from .settingsWindow import SettingsDialog

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 520)
        Form.setMinimumSize(QtCore.QSize(720, 420))

        # ===== root layout =====
        self.root = QtWidgets.QVBoxLayout(Form)
        self.root.setContentsMargins(24, 24, 24, 24)
        self.root.setSpacing(16)

        # ===== header with settings button (top-left) =====
        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(0)

        self.btnSettings = QtWidgets.QToolButton(parent=Form)
        self.btnSettings.setToolTip("Settings")
        self.btnSettings.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnSettings.setText("⚙")
        self.btnSettings.setStyleSheet(
            "QToolButton{font-size:18px; background:#f5f5f5; border:0px; "
            "border-radius:6px; padding:6px;} "
            "QToolButton:hover{background:#eee;} "
            "QToolButton:pressed{background:#e0e0e0;}"
        )
        self.btnSettings.setFixedSize(36, 36)
        hdr.addWidget(self.btnSettings, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        hdr.addStretch(1)
        self.root.addLayout(hdr)

        # ===== title =====
        self.lblTitle = QtWidgets.QLabel(parent=Form)
        tfont = QtGui.QFont()
        tfont.setFamily("Poppins")
        tfont.setBold(True)
        self.lblTitle.setFont(tfont)
        self.lblTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblTitle.setStyleSheet(
            "font-family:'Poppins',sans-serif;"
            "font-size:26px;"
            "font-weight:bold;"
            "color:#222;"
            "text-transform:uppercase;"
            "letter-spacing:2px;"
            "padding:10px;"
            "border-radius:8px;"
            "background-color:#f0f0f0;"
            "border:0px;"          # << only drop area has borders now
        )
        self.root.addWidget(self.lblTitle)

        # ===== drop area (ONLY place with borders) =====
        self.dropArea = DropFrame(parent=Form)
        self.dropArea.setObjectName("dropArea")
        self.dropArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.dropArea.setStyleSheet(
            "background:#fafafa;"
            "border:2px dashed #bbb;"   # << keep border here
            "border-radius:8px;"
        )
        self.dropArea.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.dropLayout = QtWidgets.QVBoxLayout(self.dropArea)
        self.dropLayout.setContentsMargins(24, 18, 24, 18)
        self.dropLayout.setSpacing(12)

        self.label = QtWidgets.QLabel(parent=self.dropArea)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border:0px;")
        self.dropLayout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.btnBrowse = QtWidgets.QPushButton(parent=self.dropArea)
        self.btnBrowse.setObjectName("btnBrowse")
        self.btnBrowse.setFixedHeight(44)
        self.btnBrowse.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnBrowse.setStyleSheet(
            "QPushButton{background-color:#4CAF50;color:white;border:0px;"
            "padding:10px 20px;border-radius:6px;font-size:20px;font-weight:bold;}"
            "QPushButton:hover{background-color:#45a049;}"
            "QPushButton:pressed{background-color:#3e8e41;}"
        )
        self.dropLayout.addWidget(self.btnBrowse, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.root.addWidget(self.dropArea)

        # ===== row: file chosen =====
        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(10)

        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setStyleSheet("border:0px;")
        row1.addWidget(self.label_2)

        self.lineFilePath = QtWidgets.QLineEdit(parent=Form)
        self.lineFilePath.setReadOnly(True)
        self.lineFilePath.setStyleSheet(
            "QLineEdit{background:#fafafa;border:0px;border-radius:4px;"
            "padding:6px;font-size:13px;}"
            "QLineEdit:focus{border:0px;outline:none;}"
        )
        self.lineFilePath.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        row1.addWidget(self.lineFilePath)
        self.root.addLayout(row1)

        # ===== row: type + generate =====
        row2 = QtWidgets.QHBoxLayout()
        row2.setSpacing(10)

        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setStyleSheet("border:0px;")
        row2.addWidget(self.label_3)

        self.comboType = QtWidgets.QComboBox(parent=Form)
        self.comboType.setStyleSheet(
            "QComboBox{background:#fafafa;border:0px;border-radius:4px;"
            "padding:6px;font-size:13px;}"
            "QComboBox:focus{border:0px;outline:none;}"
            "QComboBox::drop-down{border:0px;width:20px;}"
        )
        self.comboType.addItems(["PDF", "DOCX"])
        self.comboType.setFixedWidth(120)
        row2.addWidget(self.comboType)

        row2.addStretch(1)

        self.btnGenerate = QtWidgets.QPushButton(parent=Form)
        self.btnGenerate.setObjectName("btnGenerate")
        self.btnGenerate.setFixedSize(180, 52)
        self.btnGenerate.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnGenerate.setStyleSheet(
            "QPushButton{background-color:#2196F3;color:white;border:0px;"
            "padding:10px 20px;border-radius:6px;font-size:14px;font-weight:bold;}"
            "QPushButton:hover{background-color:#1976D2;}"
            "QPushButton:pressed{background-color:#1565C0;}"
        )
        row2.addWidget(self.btnGenerate)
        self.root.addLayout(row2)

                # ===== footer: copyright =====
        self.footer = QtWidgets.QLabel(parent=Form)
        self.footer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.footer.setOpenExternalLinks(True)
        self.footer.setStyleSheet("color: #888; font-size: 15px; border:0px;")
        self.footer.setText(
            '<html><head/><body>'
            '<p align="center">Created by '
            '<a href="https://github.com/AmrDroid-git" style="color:#2196F3; text-decoration:none;">AmrDroid</a>'
            '</p></body></html>'
        )
        self.root.addWidget(self.footer)

        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # hookups
        self.btnBrowse.clicked.connect(self._pick_file)
        self.btnGenerate.clicked.connect(self._on_generate_clicked)
        self.dropArea.fileDropped.connect(self._on_drop_file)
        self.btnSettings.clicked.connect(self._open_settings)

    def retranslateUi(self, Form):
        _t = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_t("Form", "PDF Convertor"))
        self.lblTitle.setText(_t("Form",
            "<html><head/><body><p align=\"center\"><span style=\" color:#ff5500;\">pdf / docx / ppt generation</span></p></body></html>"
        ))
        self.label.setText(_t("Form",
            "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Drop file here</span></p></body></html>"
        ))
        self.btnBrowse.setText(_t("Form", "Browse files"))
        self.label_2.setText(_t("Form",
            "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; color:#000000;\">File chosen :</span></p></body></html>"
        ))
        self.label_3.setText(_t("Form",
            "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Type to generate :</span></p></body></html>"
        ))
        self.btnGenerate.setText(_t("Form", "Generate"))

    # ===== helpers =====
    def _pick_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Choose a file", "", "All Files (*.*)"
        )
        if path:
            self.lineFilePath.setText(path)

    def _on_drop_file(self, path: str):
        self.lineFilePath.setText(path)

    def _open_settings(self):
        SettingsDialog(self.dropArea).exec()

    def _on_generate_clicked(self):
        in_path = self.lineFilePath.text().strip()
        if not in_path:
            QtWidgets.QMessageBox.warning(None, "No file", "Please choose a file first.")
            return

        src_ext = guess_ext(in_path)
        wanted_ui = self.comboType.currentText().upper()
        dst_ext = EXT_MAP.get(wanted_ui, wanted_ui.lower())
        if dst_ext == src_ext:
            QtWidgets.QMessageBox.information(None, "Same Type", "Source and target are the same.")
            return

        targets = available_targets_for(src_ext)
        if dst_ext not in targets:
            QtWidgets.QMessageBox.warning(
                None, "Unsupported",
                f"This build supports: {src_ext} -> {', '.join(targets) or '—'}"
            )
            return

        default_name = str(Path(in_path).with_suffix("." + dst_ext).name)
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Save As", default_name, "*/*"
        )
        if not out_path:
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        try:
            converter = get_converter(src_ext, dst_ext)
            converter(in_path, out_path)
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.information(None, "Done", f"Saved to:\n{out_path}")
        except Exception as e:
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.critical(None, "Error", f"{type(e).__name__}: {e}")


# --- simple drop frame ---
class DropFrame(QtWidgets.QFrame):
    fileDropped = QtCore.pyqtSignal(str)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QtGui.QDropEvent):
        urls = e.mimeData().urls()
        if urls:
            local = urls[0].toLocalFile()
            if local:
                self.fileDropped.emit(local)
