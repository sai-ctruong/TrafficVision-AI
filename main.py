"""
Smart Traffic Car Counting System
Main Entry Point

A modern desktop application for traffic car counting using:
- Image Enhancement (CLAHE, Gamma, Brightness/Contrast, Denoising)
- YOLO11 Object Detection
- PyQt6 + qfluentwidgets UI

Author: Digital Image Processing Project
Date: 2024
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui_main import MainWindow


def main():
    """Main application entry point"""
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Smart Traffic Car Counting System")
    app.setOrganizationName("UTE Digital Image Processing")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
