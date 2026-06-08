"""Dark editorial image preview — warm-ink canvas with subtle radial wash."""

from __future__ import annotations

import cv2
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout
from qfluentwidgets import BodyLabel, CardWidget

from ..utils.theme import (
    BORDER,
    INK,
    RADIUS_LG,
    SAND,
    SIDEBAR_BG,
)


class ImageViewer(CardWidget):
    """Rounded card with title strip + dark image canvas."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self._pixmap: QPixmap | None = None
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 14, 18, 16)
        root.setSpacing(10)

        self.title_label = BodyLabel(title)
        self.title_label.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 700;
            color: {INK};
            letter-spacing: 0.1px;
            """
        )
        root.addWidget(self.title_label)

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(320)
        self.image_label.setStyleSheet(self._empty_style())
        root.addWidget(self.image_label, 1)

    def _empty_style(self) -> str:
        # Dark warm-ink canvas + subtle radial color washes (rust + sage tints)
        return (
            f"""
            QLabel {{
                background: qradialgradient(cx:0.25, cy:0.35, radius:0.75,
                    fx:0.25, fy:0.35,
                    stop:0 rgba(196, 81, 42, 0.10),
                    stop:0.55 {SIDEBAR_BG},
                    stop:1 {SIDEBAR_BG});
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.25);
                font-size: 12px;
                font-weight: 500;
            }}
            """
        )

    def set_image(self, image: np.ndarray) -> None:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb.shape
        qimage = QImage(
            rgb.data,
            width,
            height,
            channels * width,
            QImage.Format.Format_RGB888,
        ).copy()
        self._pixmap = QPixmap.fromImage(qimage)
        self.image_label.setStyleSheet(
            f"""
            QLabel {{
                background: {SIDEBAR_BG};
                border-radius: 8px;
            }}
            """
        )
        self.image_label.setText("")
        self._render()

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self._render()

    def _render(self) -> None:
        if self._pixmap is None:
            return
        scaled = self._pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)
