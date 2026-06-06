"""Base page helpers."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import ScrollArea, TitleLabel


class BackgroundView(QWidget):
    """Page body with traffic city background and soft overlay."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PageView")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        backgrounds_dir = Path(__file__).resolve().parents[1] / "assets" / "backgrounds"
        # Use the less blurred version
        background_path = backgrounds_dir / "background_traffic.jpg"
        if not background_path.exists():
            background_path = backgrounds_dir / "background_traffic_blur.jpg"

        self._background_pixmap = QPixmap(str(background_path))
        self.background = QLabel(self)
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.background.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # Softer overlay for readability
        self.overlay = QLabel(self)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.overlay.setStyleSheet(
            """
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(248, 250, 252, 0.88),
                stop:0.5 rgba(243, 246, 250, 0.85),
                stop:1 rgba(238, 242, 248, 0.90));
            """
        )
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
    """Scrollable page with content body and traffic background."""

    def __init__(self, title: str, object_name: str) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.viewport().setStyleSheet("background: transparent;")
        self.view = BackgroundView()
        self.setWidget(self.view)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(32, 28, 32, 32)
        self.layout.setSpacing(20)
        
        # Modern page title
        page_title = TitleLabel(title)
        page_title.setStyleSheet(
            """
            font-size: 28px;
            font-weight: 700;
            color: #1a1a1a;
            letter-spacing: -0.5px;
            """
        )
        self.layout.addWidget(page_title)

