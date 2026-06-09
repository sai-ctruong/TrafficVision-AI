"""Base page scaffolding — warm cream canvas + editorial page header."""

from __future__ import annotations

from pathlib import Path

import cv2
from PyQt6.QtCore import QPointF, Qt, QTimer
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QImage,
    QLinearGradient,
    QPainter,
    QPixmap,
    QRadialGradient,
)
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, ScrollArea

from ..utils.theme import (
    APP_BACKGROUND,
    FONT_SERIF,
    INK,
    INK_3,
    SECONDARY_TEXT,
)


PAGE_DESCRIPTIONS: dict[str, str] = {
    "Dashboard": "Overview of recent traffic detections and model performance.",
    "Image Processing": "Enhance frames before inference — CLAHE, gamma, and noise control.",
    "Vehicle Detection": "Run YOLO26 on a single image and inspect class counts.",
    "Video Analysis": "Detect, track, and count vehicles crossing a counting line.",
    "Analytics": "Compare original vs. enhanced detections at a glance.",
    "History": "Searchable record of every detection run.",
    "Project Information": "A polished overview of the TrafficVision AI project, team, and architecture.",
    "Settings": "Theme, model weights, and confidence preferences.",
}


class BackgroundView(QWidget):
    """Flat cream canvas.

    ``background`` / ``overlay`` attributes are retained for backwards
    compatibility with pages that toggle them (e.g. ``analytics.py``).
    They are inert by default.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PageView")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"#PageView {{ background: {APP_BACKGROUND}; }}")

        # Optional atmospheric depth blobs + looping traffic video background.
        # Enable per-page with ``self.view.depth_blobs = True`` and/or
        # ``self.view.enable_video_background([...candidate_paths])``.
        self.depth_blobs = False
        self._video_cap: cv2.VideoCapture | None = None
        self._video_pixmap: QPixmap | None = None
        self._video_timer: QTimer | None = None

        self.background = QLabel(self)
        self.background.hide()
        self.overlay = QLabel(self)
        self.overlay.hide()

    # ------------------------------------------------------------------
    # Video background
    # ------------------------------------------------------------------
    def enable_video_background(self, candidate_paths: list[str | Path]) -> bool:
        """Try each path in order; first that opens is looped as the background."""
        for path in candidate_paths:
            try:
                cap = cv2.VideoCapture(str(path))
                if cap.isOpened():
                    self._video_cap = cap
                    break
                cap.release()
            except Exception:
                continue
        if self._video_cap is None:
            return False
        self._video_timer = QTimer(self)
        self._video_timer.timeout.connect(self._advance_video)
        self._video_timer.start(40)  # ~25 fps
        return True

    def _advance_video(self) -> None:
        cap = self._video_cap
        if cap is None:
            return
        ok, frame = cap.read()
        if not ok:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = cap.read()
            if not ok:
                return
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888).copy()
        self._video_pixmap = QPixmap.fromImage(qimg)
        self.update()

    def showEvent(self, event):  # type: ignore[override]
        super().showEvent(event)
        if self._video_timer is not None and not self._video_timer.isActive():
            self._video_timer.start(40)

    def hideEvent(self, event):  # type: ignore[override]
        super().hideEvent(event)
        if self._video_timer is not None:
            self._video_timer.stop()

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------
    def paintEvent(self, event):  # type: ignore[override]
        super().paintEvent(event)
        if self._video_pixmap is None and not self.depth_blobs:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect()

        # Traffic video frame — cover fill, centered
        if self._video_pixmap is not None and not self._video_pixmap.isNull():
            scaled = self._video_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)

            # Warm cream→sand tint — keeps the warm palette dominant,
            # video shows through as subtle motion / texture.
            tint = QLinearGradient(QPointF(0, 0), QPointF(0, self.height()))
            top = QColor("#FAF8F3"); top.setAlphaF(0.72)
            mid = QColor("#F3EFE6"); mid.setAlphaF(0.74)
            bot = QColor("#EAE4D9"); bot.setAlphaF(0.78)
            tint.setColorAt(0.0, top)
            tint.setColorAt(0.5, mid)
            tint.setColorAt(1.0, bot)
            painter.fillRect(rect, tint)

        # Atmospheric color blobs (rust + gold + sage)
        if self.depth_blobs:
            self._paint_depth_blobs(painter, rect)

    def _paint_depth_blobs(self, painter: QPainter, rect) -> None:
        wash_size = max(rect.width(), rect.height())

        # Rust — top-left
        g1 = QRadialGradient(
            QPointF(rect.left() + rect.width() * 0.16, rect.top() + 80),
            wash_size * 0.78,
        )
        a1 = QColor("#C4512A"); a1.setAlphaF(0.22)
        b1 = QColor("#C4512A"); b1.setAlphaF(0.0)
        g1.setColorAt(0.0, a1); g1.setColorAt(1.0, b1)
        painter.setBrush(QBrush(g1)); painter.drawRect(rect)

        # Gold — right-middle
        g2 = QRadialGradient(
            QPointF(rect.right() - 30, rect.center().y() - 40),
            wash_size * 0.66,
        )
        a2 = QColor("#C9882A"); a2.setAlphaF(0.18)
        b2 = QColor("#C9882A"); b2.setAlphaF(0.0)
        g2.setColorAt(0.0, a2); g2.setColorAt(1.0, b2)
        painter.setBrush(QBrush(g2)); painter.drawRect(rect)

        # Sage — bottom-center
        g3 = QRadialGradient(
            QPointF(rect.center().x() - 120, rect.bottom() + 60),
            wash_size * 0.80,
        )
        a3 = QColor("#4A6741"); a3.setAlphaF(0.16)
        b3 = QColor("#4A6741"); b3.setAlphaF(0.0)
        g3.setColorAt(0.0, a3); g3.setColorAt(1.0, b3)
        painter.setBrush(QBrush(g3)); painter.drawRect(rect)

        # Vignette
        v = QRadialGradient(
            QPointF(rect.center().x(), rect.center().y()),
            wash_size * 0.85,
        )
        va = QColor("#1A1208"); va.setAlphaF(0.0)
        vb = QColor("#1A1208"); vb.setAlphaF(0.07)
        v.setColorAt(0.5, va); v.setColorAt(1.0, vb)
        painter.setBrush(QBrush(v)); painter.drawRect(rect)


class Page(ScrollArea):
    """Scrollable page with an editorial header (serif title + descriptor)."""

    def __init__(self, title: str, object_name: str) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.viewport().setStyleSheet("background: transparent;")

        self.view = BackgroundView()
        self.setWidget(self.view)

        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(32, 28, 32, 36)
        self.layout.setSpacing(20)

        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)

        # Editorial serif title — Fraunces-style
        page_title = QLabel(title)
        page_title.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 30px;
            font-weight: 700;
            color: {INK};
            letter-spacing: -0.8px;
            """
        )
        header_layout.addWidget(page_title)

        descriptor = PAGE_DESCRIPTIONS.get(title, "")
        if descriptor:
            desc = BodyLabel(descriptor)
            desc.setWordWrap(True)
            desc.setStyleSheet(
                f"""
                font-size: 14px;
                color: {INK_3};
                font-weight: 400;
                line-height: 1.5;
                """
            )
            header_layout.addWidget(desc)

        self.layout.addWidget(header)
        self.layout.addSpacing(2)
