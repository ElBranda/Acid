import sys
import os
import re
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QFrame
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

import src.sistematizador as s
import src.documentador as d

QSS_STYLE = """
QMainWindow {
    background-color: #121214;
}
QLabel {
    color: #e1e1e6;
    font-family: "Segoe UI", Calibri, sans-serif;
    font-size: 13px;
}
QLabel#TitleLabel {
    color: #00ff87;
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 10px;
}
QLabel#StatusLabel {
    font-size: 14px;
    font-weight: bold;
}
QFrame#CardFrame {
    background-color: #202024;
    border: 1px solid #29292e;
    border-radius: 8px;
    padding: 12px;
}
QPushButton {
    background-color: #29292e;
    color: #e1e1e6;
    border: 1px solid #323238;
    border-radius: 6px;
    padding: 6px 16px;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #323238;
    border-color: #41414a;
}
QPushButton:pressed {
    background-color: #121214;
}
QPushButton#PrimaryButton {
    background-color: #00ff87;
    color: #0c0c0d;
    border: none;
    font-size: 14px;
    padding: 10px 24px;
}
QPushButton#PrimaryButton:hover {
    background-color: #17ff96;
}
QPushButton#PrimaryButton:pressed {
    background-color: #00cc6a;
}
"""

class TprojectApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.file_path: str | None = None
        self.out_path: str | None = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Acid")
        self.resize(450, 480)
        self.setMinimumSize(450, 480)
        self.setStyleSheet(QSS_STYLE)
        
        if os.path.exists("Acid.ico"):
            self.setWindowIcon(QIcon("Acid.ico"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        title_label = QLabel("Acid")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        upload_card = QFrame()
        upload_card.setObjectName("CardFrame")
        upload_layout = QVBoxLayout(upload_card)
        upload_row = QHBoxLayout()
        upload_row.addWidget(QLabel("Archivo de origen:"))
        btn_upload = QPushButton("Subir Excel")
        btn_upload.clicked.connect(self.upload_file)
        upload_row.addWidget(btn_upload)
        upload_layout.addLayout(upload_row)
        self.lbl_file = QLabel("Ningún archivo seleccionado")
        self.lbl_file.setStyleSheet("color: #7c7c8a;")
        self.lbl_file.setWordWrap(True)
        upload_layout.addWidget(self.lbl_file)
        main_layout.addWidget(upload_card)

        output_card = QFrame()
        output_card.setObjectName("CardFrame")
        output_layout = QVBoxLayout(output_card)
        output_row = QHBoxLayout()
        output_row.addWidget(QLabel("Carpeta de salida:"))
        btn_output = QPushButton("Elegir Ruta")
        btn_output.clicked.connect(self.choose_output_dir)
        output_row.addWidget(btn_output)
        output_layout.addLayout(output_row)
        self.lbl_output = QLabel("Directorio por defecto (.)")
        self.lbl_output.setStyleSheet("color: #7c7c8a;")
        self.lbl_output.setWordWrap(True)
        output_layout.addWidget(self.lbl_output)
        main_layout.addWidget(output_card)

        main_layout.addSpacing(10)
        btn_convert = QPushButton("Convertir Archivo")
        btn_convert.setObjectName("PrimaryButton")
        btn_convert.clicked.connect(self.convert_file)
        main_layout.addWidget(btn_convert)

        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("StatusLabel")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.lbl_status)

    def upload_file(self) -> None:
        temp, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Excel Files (*.xls *.xlsx)")
        if temp:
            self.file_path = temp
            file_name = os.path.basename(self.file_path)
            self.lbl_file.setText(file_name)
            self.lbl_file.setStyleSheet("color: #00ff87; font-weight: bold;")
            self.lbl_status.setText("")

    def choose_output_dir(self) -> None:
        temp = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if temp:
            self.out_path = temp
            self.lbl_output.setText(self.out_path)
            self.lbl_output.setStyleSheet("color: #e1e1e6;")
            self.lbl_status.setText("")

    def convert_file(self) -> None:
        if not self.file_path:
            self.lbl_status.setText("No se añadió ningún archivo")
            self.lbl_status.setStyleSheet("color: #f75a68;")
            return

        folder_destination = self.out_path if self.out_path else "."
        filename = os.path.basename(self.file_path)
        match = re.search(r"\d{2}-\d{4}", filename)
        
        if match:
            fecha_str = match.group(0)
        else:
            fecha_str = "00-0000"

        output_filename = f"LSD {fecha_str}.txt"
        full_output_path = os.path.join(folder_destination, output_filename)
        
        try:
            d.generate_LSD(self.file_path, full_output_path)
            self.lbl_status.setText("¡Archivo creado con éxito!")
            self.lbl_status.setStyleSheet("color: #00ff87;")
        except Exception as e:
            print(str(e))
            self.lbl_status.setText(f"Error: {str(e)}")
            self.lbl_status.setStyleSheet("color: #f75a68;")

def launch_gui() -> None:
    app = QApplication(sys.argv)
    window = TprojectApp()
    window.show()
    sys.exit(app.exec())