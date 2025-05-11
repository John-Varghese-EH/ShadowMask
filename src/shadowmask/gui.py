import sys
import os
import time
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox, QProgressBar, QAction, QMenuBar
)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from .core import alpha_layer_attack, fgsm_attack

REPO_URL = "https://github.com/John-Varghese-EH/ShadowMask"

class Worker(QThread):
    progress = pyqtSignal(str, int)  # status, percent
    finished = pyqtSignal(str)       # output file

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        start_time = time.time()
        self.progress.emit("Running Alpha Layer Attack...", 20)
        alpha_path = alpha_layer_attack(self.image_path)
        self.progress.emit("Alpha Layer Attack done. Running FGSM...", 60)
        fgsm_path = fgsm_attack(alpha_path)
        # Rename output as required
        dir_, base = os.path.split(self.image_path)
        name, ext = os.path.splitext(base)
        out_path = os.path.join(dir_, f"{name}_ShadowMask-cloaked{ext}")
        os.replace(fgsm_path, out_path)
        elapsed = time.time() - start_time
        self.progress.emit(f"Done in {elapsed:.1f}s", 100)
        self.finished.emit(out_path)

class ShadowMaskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShadowMask")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../logo.png")))
        self.setGeometry(200, 200, 600, 450)
        self.image_path = None
        self.processed_path = None

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        # Logo and name
        logo_path = os.path.join(os.path.dirname(__file__), "../logo.png")
        logo_label = QLabel()
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        name_label = QLabel("ShadowMask")
        name_label.setFont(QFont("Arial", 24, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        logo_name_box = QHBoxLayout()
        logo_name_box.addWidget(logo_label)
        logo_name_box.addWidget(name_label)
        logo_name_box.addStretch()
        vbox.addLayout(logo_name_box)

        # Image preview
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setFixedHeight(200)
        vbox.addWidget(self.img_label)

        # Buttons
        btn_box = QHBoxLayout()
        self.select_btn = QPushButton("Select Image")
        self.select_btn.clicked.connect(self.select_image)
        btn_box.addWidget(self.select_btn)
        self.process_btn = QPushButton("Run ShadowMask Cloak")
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self.run_processing)
        btn_box.addWidget(self.process_btn)
        vbox.addLayout(btn_box)

        # Status and time
        self.status_label = QLabel("Select an image to begin.")
        self.status_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.status_label)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        vbox.addWidget(self.progress)

        # Date
        date_label = QLabel(f"Current date: {datetime.now().strftime('%A, %B %d, %Y, %I:%M %p')}")
        date_label.setAlignment(Qt.AlignRight)
        vbox.addWidget(date_label)

        central.setLayout(vbox)

        # Menu bar
        menubar = self.menuBar()
        about_menu = menubar.addMenu("About")
        about_action = QAction("About ShadowMask", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.img_label.setPixmap(pixmap.scaled(400, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.status_label.setText(f"Loaded: {os.path.basename(file_path)}")
            self.process_btn.setEnabled(True)
            self.progress.setValue(0)

    def run_processing(self):
        if not self.image_path:
            QMessageBox.warning(self, "No Image", "Please select an image first.")
            return
        self.status_label.setText("Processing...")
        self.progress.setValue(10)
        self.process_btn.setEnabled(False)
        self.worker = Worker(self.image_path)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.processing_done)
        self.worker.start()

    def update_status(self, status, percent):
        self.status_label.setText(status)
        self.progress.setValue(percent)

    def processing_done(self, out_path):
        self.processed_path = out_path
        self.status_label.setText(f"Saved: {os.path.basename(out_path)}")
        pixmap = QPixmap(out_path)
        self.img_label.setPixmap(pixmap.scaled(400, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.progress.setValue(100)
        self.process_btn.setEnabled(True)
        QMessageBox.information(self, "Done", f"Image processed and saved as:\n{out_path}")

    def show_about(self):
        QMessageBox.information(
            self, "About ShadowMask",
            (
                "<b>ShadowMask</b><br>"
                "Your Face, Your Rules – Beyond AI’s Reach<br><br>"
                "Protect your images from unauthorized AI-based facial recognition and scraping.<br>"
                "<br>"
                "GitHub: <a href='https://github.com/John-Varghese-EH/ShadowMask'>"
                "https://github.com/John-Varghese-EH/ShadowMask</a><br>"
                "<br>"
                "Developed by Cyber_Trinity (J0X) with ❤️"
            )
        )

def main():
    app = QApplication(sys.argv)
    window = ShadowMaskApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
