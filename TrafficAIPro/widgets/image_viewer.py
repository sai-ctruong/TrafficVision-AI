"""Square media preview cards for images and video frames."""

from __future__ import annotations

import cv2
import numpy as np
from PyQt6.QtCore import QRectF, QSize, Qt
from PyQt6.QtGui import QColor, QImage, QPainter, QPainterPath, QPen, QPixmap
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QSizePolicy, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, CardWidget

from ..utils.theme import BORDER, INK, INK_3, RADIUS_LG, SAND


MEDIA_BG = "#0F172A"
MEDIA_BORDER = "#263244"


class SquareMediaCanvas(QWidget):
    """A 1:1 dark canvas that paints centered media without distortion."""

    def __init__(self) -> None:
        super().__init__()
        self._pixmap: QPixmap | None = None
        self._empty_text = "No media loaded"
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(320, 320)
        self.setMaximumSize(480, 480)

    def hasHeightForWidth(self) -> bool:  # type: ignore[override]
        return True

    def heightForWidth(self, width: int) -> int:  # type: ignore[override]
        return width

    def sizeHint(self) -> QSize:  # type: ignore[override]
        return QSize(440, 440)

    def minimumSizeHint(self) -> QSize:  # type: ignore[override]
        return QSize(320, 320)

    def set_pixmap(self, pixmap: QPixmap | None, empty_text: str = "No media loaded") -> None:
        self._pixmap = pixmap
        self._empty_text = empty_text
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        side = min(self.width(), self.height())
        x = (self.width() - side) // 2
        y = (self.height() - side) // 2
        canvas = self.rect().adjusted(x, y, -x, -y)

        path = QPainterPath()
        path.addRoundedRect(QRectF(canvas), 10, 10)
        painter.fillPath(path, QColor(MEDIA_BG))
        painter.setPen(QPen(QColor(MEDIA_BORDER), 1))
        painter.drawPath(path)

        if self._pixmap is None or self._pixmap.isNull():
            painter.setPen(QColor(148, 163, 184))
            painter.drawText(canvas, Qt.AlignmentFlag.AlignCenter, self._empty_text)
            return

        inner = canvas.adjusted(14, 14, -14, -14)
        scaled = self._pixmap.scaled(
            inner.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        px = inner.x() + (inner.width() - scaled.width()) // 2
        py = inner.y() + (inner.height() - scaled.height()) // 2
        painter.drawPixmap(px, py, scaled)


class ImageViewer(CardWidget):
    """Modern AI-dashboard media card with a square preview canvas."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self._pixmap: QPixmap | None = None
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setMaximumWidth(540)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(22)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(15, 23, 42, 28))
        self.setGraphicsEffect(shadow)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 14, 18, 16)
        root.setSpacing(10)

        self.title_label = BodyLabel(title)
        self.title_label.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 700;
            color: {INK};
            letter-spacing: 0;
            """
        )
        root.addWidget(self.title_label)

        self.image_label = SquareMediaCanvas()
        root.addWidget(self.image_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.status_label = BodyLabel("Waiting for input")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            f"""
            font-size: 11px;
            font-weight: 500;
            color: {INK_3};
            """
        )
        root.addWidget(self.status_label)

    def set_image(self, image: np.ndarray, status: str | None = None) -> None:
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
        self.image_label.set_pixmap(self._pixmap)
        self.status_label.setText(status or f"{width} x {height}px")

    def clear(self, message: str = "No media loaded", status: str = "Waiting for input") -> None:
        self._pixmap = None
        self.image_label.set_pixmap(None, message)
        self.status_label.setText(status)

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self.image_label.update()
