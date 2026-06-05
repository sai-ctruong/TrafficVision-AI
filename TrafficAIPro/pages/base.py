"""Base page helpers."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import ScrollArea, TitleLabel


class BackgroundView(QWidget):
    """Page body with a soft traffic image behind the content."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PageView")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        backgrounds_dir = Path(__file__).resolve().parents[1] / "assets" / "backgrounds"
        background_path = backgrounds_dir / "background_traffic_blur.jpg"
        if not background_path.exists():
            background_path = backgrounds_dir / "background_traffic.jpg"

        self._background_pixmap = QPixmap(str(background_path))
        self.background = QLabel(self)
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.background.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.overlay = QLabel(self)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.overlay.setStyleSheet("background: rgba(243, 246, 250, 135);")
        self.background.lower()

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        rect = self.rect()
        self.background.setGeometry(rect)
        self.overlay.setGeometry(rect)
        self._render_background()
        self.background.lower()

    def _render_background(self) -> None:
        if self._background_pixmap.isNull() or self.width() <= 0 or self.height() <= 0:
            self.background.clear()
            return
        scaled = self._background_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.background.setPixmap(scaled)


class Page(ScrollArea):
    """Scrollable page with a title and content body."""

    def __init__(self, title: str, object_name: str) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.viewport().setStyleSheet("background: transparent;")
        self.view = BackgroundView()
        self.setWidget(self.view)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(18)
        self.layout.addWidget(TitleLabel(title))

