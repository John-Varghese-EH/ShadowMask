# src/shadowmask/gui.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox

class ShadowMaskGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShadowMask - Privacy AI Cloak")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        self.label = QLabel("ShadowMask\nProtect your images from AI recognition.")
        layout.addWidget(self.label)

        self.open_btn = QPushButton("Open Image")
        self.open_btn.clicked.connect(self.open_image)
        layout.addWidget(self.open_btn)

        self.attack_btn = QPushButton("Apply Privacy Attack")
        self.attack_btn.clicked.connect(self.apply_attack)
        layout.addWidget(self.attack_btn)

        self.setLayout(layout)
        self.image_path = None

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.label.setText(f"Loaded: {file_path}")

    def apply_attack(self):
        if not self.image_path:
            QMessageBox.warning(self, "No Image", "Please open an image first.")
            return
        # Here you would call your core logic, e.g.:
        # result = core.apply_alpha_attack(self.image_path)
        QMessageBox.information(self, "Done", "Privacy attack applied (dummy).")

def main():
    app = QApplication(sys.argv)
    gui = ShadowMaskGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
