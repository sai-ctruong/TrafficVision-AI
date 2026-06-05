"""Vehicle detection page."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout
from qfluentwidgets import FluentIcon, InfoBar, InfoBarPosition, PrimaryPushButton, ProgressRing, PushButton

from ..database.history_repository import HistoryRepository
from ..models.detection import DetectionSummary, VEHICLE_CLASSES
from .base import Page
from ..services.detection_service import VehicleDetectionService
from ..services.settings_service import SettingsService
from ..widgets.image_viewer import ImageViewer
from ..widgets.metric_card import MetricCard


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

        actions = QHBoxLayout()
        self.load_model_button = PushButton(FluentIcon.ROBOT, "Load YOLO26 Model")
        self.load_model_button.clicked.connect(self.load_model)
        self.run_button = PrimaryPushButton(FluentIcon.PLAY, "Run Detection")
        self.run_button.clicked.connect(self.run_detection)
        self.ring = ProgressRing()
        self.ring.setFixedSize(34, 34)
        self.ring.hide()
        actions.addWidget(self.load_model_button)
        actions.addWidget(self.run_button)
        actions.addWidget(self.ring)
        actions.addStretch(1)
        self.layout.addLayout(actions)

        self.result_view = ImageViewer("Detection Result")
        self.layout.addWidget(self.result_view)

        grid = QGridLayout()
        grid.setSpacing(14)
        self.cards = {
            "car": MetricCard("Car Count", "0", FluentIcon.CAR),
            "bus": MetricCard("Bus Count", "0", FluentIcon.BUS),
            "truck": MetricCard("Truck Count", "0", FluentIcon.TRAIN),
            "van": MetricCard("Van Count", "0", FluentIcon.TAG),
            "total": MetricCard("Total Vehicles", "0", FluentIcon.SPEED_HIGH),
        }
        for index, card in enumerate(self.cards.values()):
            grid.addWidget(card, 0, index)
        self.layout.addLayout(grid)
        self.layout.addStretch(1)

    def set_image(self, image: np.ndarray, image_name: str) -> None:
        self.current_image = image
        self.current_name = image_name

    def load_model(self) -> None:
        path = self.settings.model_path
        if not Path(path).exists():
            selected, _ = QFileDialog.getOpenFileName(self, "Select YOLO model", "", "YOLO Weights (*.pt)")
            if not selected:
                return
            path = selected
            self.settings.model_path = path
        try:
            self.detection_service.load_model(path)
            self.model_status_changed.emit(f"Model loaded: {Path(path).name}")
            InfoBar.success("Model ready", f"Loaded {Path(path).name}", parent=self, position=InfoBarPosition.TOP_RIGHT)
        except Exception as exc:
            InfoBar.error("Model error", str(exc), parent=self, position=InfoBarPosition.TOP_RIGHT)

    def run_detection(self) -> None:
        if self.current_image is None:
            InfoBar.warning("No image", "Upload and enhance an image first", parent=self, position=InfoBarPosition.TOP_RIGHT)
            return
        if not self.detection_service.is_loaded:
            self.load_model()
            if not self.detection_service.is_loaded:
                return
        self.ring.show()
        self.ring.setValue(0)
        try:
            annotated, summary = self.detection_service.detect(
                self.current_image,
                self.current_name,
                self.settings.confidence,
            )
            self.result_view.set_image(annotated)
            self._update_cards(summary)
            self.history.add(summary)
            self.detection_completed.emit(summary)
            InfoBar.success("Detection complete", f"{summary.total} vehicles found", parent=self, position=InfoBarPosition.TOP_RIGHT)
        except Exception as exc:
            InfoBar.error("Detection failed", str(exc), parent=self, position=InfoBarPosition.TOP_RIGHT)
        finally:
            self.ring.hide()

    def _update_cards(self, summary: DetectionSummary) -> None:
        for key in VEHICLE_CLASSES:
            self.cards[key].set_value(summary.counts.get(key, 0))
        self.cards["total"].set_value(summary.total)
