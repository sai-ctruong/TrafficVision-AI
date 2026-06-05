"""Dashboard hero and welcome empty state."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QGraphicsBlurEffect, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, FluentIcon, PrimaryPushButton, StrongBodyLabel

from ..utils.paths import APP_ROOT


class HeroPanel(QFrame):
    """Hero empty state shown before an image is uploaded."""

    upload_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("HeroPanel")
        self.setMinimumHeight(360)
        self.setStyleSheet(
            """
            #HeroPanel {
                border-radius: 18px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0B1220, stop:0.55 #102A43, stop:1 #0F6CBD);
            }
            """
        )

        self.background = QLabel(self)
        self.background.setScaledContents(True)
        blur = QGraphicsBlurEffect(self.background)
        blur.setBlurRadius(4)
        self.background.setGraphicsEffect(blur)

        self.overlay = QLabel(self)
        self.overlay.setStyleSheet("background: rgba(5, 10, 18, 178); border-radius: 18px;")

        content = QWidget(self)
        content.setObjectName("HeroContent")
        content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(48, 42, 48, 42)
        layout.setSpacing(12)

        badge = BodyLabel("Powered by YOLO26 + OpenCV")
        badge.setStyleSheet(
            "color: #D7EAFF; background: rgba(255,255,255,34); border-radius: 14px; padding: 6px 12px;"
        )
        badge.setFixedHeight(30)

        title = StrongBodyLabel("TrafficAI Pro")
        title.setStyleSheet("font-size: 44px; font-weight: 800; color: white;")
        subtitle = StrongBodyLabel("Smart Traffic Vehicle Detection\n& Analytics System")
        subtitle.setStyleSheet("font-size: 26px; font-weight: 650; color: white;")
        subtitle.setWordWrap(True)
        workflow = BodyLabel("Enhance  •  Detect  •  Count  •  Analyze")
        workflow.setStyleSheet("font-size: 16px; color: #D7EAFF;")

        button_row = QHBoxLayout()
        upload = PrimaryPushButton(FluentIcon.PHOTO, "Upload Image")
        upload.setFixedHeight(44)
        upload.clicked.connect(self.upload_requested)
        button_row.addWidget(upload)
        button_row.addStretch(1)

        layout.addWidget(badge, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addSpacing(8)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(workflow)
        layout.addSpacing(12)
        layout.addLayout(button_row)
        layout.addStretch(1)

        self.content = content
        self._pixmap = self._load_pixmap()
        self._render_background()

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        rect = self.rect()
        self.background.setGeometry(rect)
        self.overlay.setGeometry(rect)
        self.content.setGeometry(rect)
        self._render_background()
        self.background.lower()
        self.overlay.raise_()
        self.content.raise_()

    def _load_pixmap(self) -> QPixmap | None:
        """Find the provided traffic hero image from common project locations."""
        candidates = []
        for folder in (APP_ROOT / "assets", APP_ROOT / "resources", APP_ROOT.parent):
            if not folder.exists():
                continue
            images = [
                path
                for path in folder.iterdir()
                if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
            ]
            images.sort(
                key=lambda path: (
                    not any(token in path.stem.lower() for token in ("hero", "dashboard", "traffic", "city")),
                    path.name.lower(),
                )
            )
            candidates.extend(images)

        for path in candidates:
            pixmap = QPixmap(str(path))
            if not pixmap.isNull():
                return pixmap
        return None

    def _render_background(self) -> None:
        if self._pixmap is None or self.width() <= 0 or self.height() <= 0:
            self.background.clear()
            return
        scaled = self._pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.background.setPixmap(scaled)
