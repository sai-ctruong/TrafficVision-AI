"""Application entry point for TrafficAI Pro."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from .ui.main_window import TrafficAIWindow
from .utils.paths import ensure_app_dirs


def main() -> int:
    """Start the desktop application."""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("TrafficAI Pro")
    app.setOrganizationName("TrafficAI")
    app.installTranslator(FluentTranslator())

    ensure_app_dirs()
    window = TrafficAIWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
