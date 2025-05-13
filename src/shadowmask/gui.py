"""
GUI for ShadowMask using PyQt5
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QCheckBox, QSlider,
    QProgressBar, QMessageBox, QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon, QMovie
from .core import ShadowMask
from .banner import BANNER, ABOUT

class WorkerThread(QThread):
    """Worker thread for image processing"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, image_path, output_path, methods, intensity):
        super().__init__()
        self.image_path = image_path
        self.output_path = output_path
        self.methods = methods
        self.intensity = intensity
        
    def run(self):
        try:
            shadowmask = ShadowMask()
            shadowmask.protect_image(
                self.image_path,
                methods=self.methods,
                output_path=self.output_path,
                intensity=self.intensity
            )
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))

class ShadowMaskApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ShadowMask - Your Face, Your Rules")
        self.setMinimumSize(1000, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Logo and title
        logo_group = QGroupBox()
        logo_layout = QHBoxLayout()
        
        # Load and display animated logo
        self.logo_label = QLabel()
        self.logo_movie = QMovie(os.path.join(os.path.dirname(__file__), "logo.gif"))
        self.logo_movie.setScaledSize(QSize(100, 100))
        self.logo_label.setMovie(self.logo_movie)
        self.logo_movie.start()
        
        title_label = QLabel("ShadowMask")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(title_label)
        logo_layout.addStretch()
        logo_group.setLayout(logo_layout)
        layout.addWidget(logo_group)
        
        # Image preview
        preview_group = QGroupBox("Image Preview")
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(400, 300)
        self.preview_label.setStyleSheet("border: 2px dashed #ccc;")
        preview_layout.addWidget(self.preview_label)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Controls
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        self.select_btn = QPushButton("Select Image")
        self.select_btn.clicked.connect(self.select_image)
        file_layout.addWidget(self.select_btn)
        controls_layout.addLayout(file_layout)
        
        # Protection methods
        method_group = QGroupBox("Protection Methods")
        method_layout = QVBoxLayout()
        self.method_checkboxes = {
            'alpha_layer': QCheckBox("Alpha Layer Attack"),
            'adversarial': QCheckBox("Adversarial Pattern"),
            'encoder': QCheckBox("Encoder Attack"),
            'diffusion': QCheckBox("Diffusion Attack")
        }
        for checkbox in self.method_checkboxes.values():
            method_layout.addWidget(checkbox)
        method_group.setLayout(method_layout)
        controls_layout.addWidget(method_group)
        
        # Intensity slider
        intensity_layout = QHBoxLayout()
        intensity_layout.addWidget(QLabel("Protection Intensity:"))
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setMinimum(0)
        self.intensity_slider.setMaximum(100)
        self.intensity_slider.setValue(50)
        self.intensity_slider.setTickPosition(QSlider.TicksBelow)
        intensity_layout.addWidget(self.intensity_slider)
        controls_layout.addLayout(intensity_layout)
        
        # Protect button
        button_layout = QHBoxLayout()
        self.protect_btn = QPushButton("Protect Image")
        self.protect_btn.clicked.connect(self.protect_image)
        self.protect_btn.setEnabled(False)
        button_layout.addWidget(self.protect_btn)
        controls_layout.addLayout(button_layout)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # About section
        about_group = QGroupBox("About")
        about_layout = QVBoxLayout()
        about_text = QLabel(ABOUT)
        about_text.setWordWrap(True)
        about_text.setOpenExternalLinks(True)
        about_layout.addWidget(about_text)
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        self.current_image = None
        
    def select_image(self):
        """Handle image selection"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            try:
                self.current_image = file_name
                pixmap = QPixmap(file_name)
                if pixmap.isNull():
                    raise ValueError("Failed to load image")
                    
                scaled_pixmap = pixmap.scaled(
                    self.preview_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled_pixmap)
                self.protect_btn.setEnabled(True)
                self.statusBar().showMessage(f"Selected: {os.path.basename(file_name)}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to load image: {str(e)}"
                )
                self.current_image = None
                self.protect_btn.setEnabled(False)
            
    def protect_image(self):
        """Handle image protection"""
        if not self.current_image:
            return
            
        # Get output path
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Protected Image",
            "",
            "PNG Files (*.png)"
        )
        
        if not output_path:
            return
            
        # Get selected methods
        methods = [
            method for method, checkbox in self.method_checkboxes.items()
            if checkbox.isChecked()
        ]
        
        if not methods:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select at least one protection method"
            )
            return
        
        # Get intensity
        intensity = self.intensity_slider.value() / 100.0
        
        # Create and start worker thread
        self.worker = WorkerThread(
            self.current_image,
            output_path,
            methods,
            intensity
        )
        self.worker.finished.connect(self.protection_finished)
        self.worker.error.connect(self.protection_error)
        
        # Update UI
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.protect_btn.setEnabled(False)
        self.select_btn.setEnabled(False)
        self.statusBar().showMessage("Protecting image...")
        
        self.worker.start()
        
    def protection_finished(self, output_path):
        """Handle protection completion"""
        self.progress_bar.setVisible(False)
        self.protect_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        self.statusBar().showMessage(f"Protected image saved: {os.path.basename(output_path)}")
        
        try:
            # Show preview of protected image
            pixmap = QPixmap(output_path)
            if pixmap.isNull():
                raise ValueError("Failed to load protected image")
                
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
            
            QMessageBox.information(
                self,
                "Success",
                "Image has been protected successfully!"
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Warning",
                f"Image was protected but preview failed: {str(e)}"
            )
        
    def protection_error(self, error_msg):
        """Handle protection error"""
        self.progress_bar.setVisible(False)
        self.protect_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        self.statusBar().showMessage("Error occurred")
        
        QMessageBox.critical(
            self,
            "Error",
            f"Failed to protect image: {error_msg}"
        )

def run():
    """Run the application"""
    app = QApplication(sys.argv)
    window = ShadowMaskApp()
    window.show()
    
    # Show banner in message box
    QMessageBox.information(
        window,
        "Welcome to ShadowMask",
        f"{BANNER}\n{ABOUT}"
    )
    
    sys.exit(app.exec_())
