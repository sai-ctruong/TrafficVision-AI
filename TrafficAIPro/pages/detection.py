"""Vehicle detection page."""

from __future__ import annotations

import hashlib

import numpy as np
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QGridLayout
from qfluentwidgets import FluentIcon, InfoBar, InfoBarPosition

from ..database.history_repository import HistoryRepository
from ..models.detection import DetectionSummary, VEHICLE_CLASSES
from .base import Page
from ..services.detection_service import VehicleDetectionService
from ..services.settings_service import SettingsService
from ..utils.theme import (
    GOLD_LIGHT,
    RUST_LIGHT,
    SAGE_LIGHT,
    SLATE_LIGHT,
    VEHICLE_COLORS,
)
from ..widgets.image_viewer import ImageViewer
from ..widgets.metric_card import MetricCard


DEFAULT_DETECTION_CONFIDENCE = 0.25


class VehicleDetectionPage(Page):
    """YOLO26 vehicle detection workflow."""

    detection_completed = pyqtSignal(object)
    model_status_changed = pyqtSignal(str)

    def __init__(
        self,
        detection_service: VehicleDetectionService,
        settings: SettingsService,
        history: HistoryRepository,
    ) -> None:
        super().__init__("Vehicle Detection", "VehicleDetectionPage")
        self.detection_service = detection_service
        self.settings = settings
        self.history = history
        self.current_image: np.ndarray | None = None
        self.current_name = ""
        self._pending_signature = ""
        self._last_detected_signature = ""
        self._auto_detect_timer = QTimer(self)
        self._auto_detect_timer.setSingleShot(True)
        self._auto_detect_timer.setInterval(450)
        self._auto_detect_timer.timeout.connect(self.run_detection)

        self.result_view = ImageViewer("Detection Result")
        self.layout.addWidget(self.result_view, 0, Qt.AlignmentFlag.AlignHCenter)

        grid = QGridLayout()
        grid.setSpacing(14)
        self.cards = {
            "car":   MetricCard("Cars",           "0", FluentIcon.CAR,        VEHICLE_COLORS["car"],   "CAR",   SLATE_LIGHT),
            "bus":   MetricCard("Buses",          "0", FluentIcon.BUS,        VEHICLE_COLORS["bus"],   "BUS",   RUST_LIGHT),
            "truck": MetricCard("Trucks",         "0", FluentIcon.TRAIN,      VEHICLE_COLORS["truck"], "TRUCK", GOLD_LIGHT),
            "van":   MetricCard("Vans",           "0", FluentIcon.TAG,        VEHICLE_COLORS["van"],   "VAN",   SAGE_LIGHT),
            "total": MetricCard("Total Vehicles", "0", FluentIcon.SPEED_HIGH, VEHICLE_COLORS["total"], "TOTAL", RUST_LIGHT),
        }
        for index, card in enumerate(self.cards.values()):
            grid.addWidget(card, 0, index)
        self.layout.addLayout(grid)
        self.layout.addStretch(1)

    def set_image(self, image: np.ndarray, image_name: str) -> None:
        signature = self._image_signature(image, image_name)
        if signature == self._last_detected_signature:
            self.result_view.status_label.setText("Latest preview already detected")
            return
        self.current_image = image
        self.current_name = image_name
        self._pending_signature = signature
        self.detection_service.reset_inference_state()
        self.result_view.status_label.setText("Waiting for automatic detection...")
        self._auto_detect_timer.start()

    def run_detection(self) -> None:
        if self.current_image is None:
            return
        if not self.detection_service.is_loaded:
            self.model_status_changed.emit("Model not loaded")
            return
        self.model_status_changed.emit("Processing image...")
        self.result_view.status_label.setText("Running YOLO detection...")
        try:
            annotated, summary = self.detection_service.detect(
                self.current_image,
                self.current_name,
                DEFAULT_DETECTION_CONFIDENCE,
            )
            self.result_view.set_image(annotated, f"{summary.total} vehicles detected")
            self._update_cards(summary)
            if self._pending_signature != self._last_detected_signature:
                self.history.add(summary, annotated)
                self._last_detected_signature = self._pending_signature
            self.detection_completed.emit(summary)
        except Exception as exc:
            InfoBar.error("Detection failed", str(exc), parent=self, position=InfoBarPosition.TOP_RIGHT)

    def _update_cards(self, summary: DetectionSummary) -> None:
        for key in VEHICLE_CLASSES:
            self.cards[key].set_value(summary.counts.get(key, 0))
        self.cards["total"].set_value(summary.total)

    def _image_signature(self, image: np.ndarray, image_name: str) -> str:
        contiguous = np.ascontiguousarray(image)
        digest = hashlib.blake2b(digest_size=16)
        digest.update(image_name.encode("utf-8", errors="ignore"))
        digest.update(str(contiguous.shape).encode("ascii"))
        digest.update(contiguous.data)
        return digest.hexdigest()
