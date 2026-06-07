"""Academic segmentation demonstration page."""

from __future__ import annotations

import numpy as np
from PyQt6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, CardWidget, CheckBox, FluentIcon, PrimaryPushButton

from ..services.image_service import ImageEnhancementService
from ..utils.theme import CARD_BORDER, PRIMARY, SECONDARY_TEXT, TEXT
from ..widgets.image_viewer import ImageViewer
from .base import Page


class SegmentationMetricCard(CardWidget):
    """Compact metric card for thresholded masks."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setBorderRadius(10)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: #FFFFFF;
                border: 1px solid {CARD_BORDER};
            }}
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        title_label = BodyLabel(title)
        title_label.setStyleSheet(f"font-size: 13px; font-weight: 800; color: {TEXT};")
        layout.addWidget(title_label)

        self.area_label = BodyLabel("Segmented Area: --")
        self.components_label = BodyLabel("Connected Components: --")
        for label in (self.area_label, self.components_label):
            label.setStyleSheet(f"font-size: 12px; font-weight: 650; color: {SECONDARY_TEXT};")
            layout.addWidget(label)

    def set_metrics(self, metrics: dict[str, int]) -> None:
        self.area_label.setText(f"Segmented Area: {metrics['area']}")
        self.components_label.setText(f"Connected Components: {metrics['components']}")


class SegmentationDemoPage(Page):
    """Compare automatic thresholding methods under traffic-lighting conditions."""

    def __init__(self, image_service: ImageEnhancementService) -> None:
        super().__init__("Segmentation Demo", "SegmentationDemoPage")
        self.image_service = image_service
        self.current_image: np.ndarray | None = None

        actions = QHBoxLayout()
        actions.setSpacing(12)
        self.upload_button = PrimaryPushButton("Upload Image")
        self.upload_button.setIcon(FluentIcon.PHOTO)
        self.upload_button.setFixedHeight(44)
        self.upload_button.clicked.connect(self.upload_image)
        actions.addWidget(self.upload_button)

        self.otsu_check = CheckBox("Otsu Threshold")
        self.gaussian_check = CheckBox("Adaptive Gaussian Threshold")
        self.mean_check = CheckBox("Adaptive Mean Threshold")
        for check in (self.otsu_check, self.gaussian_check, self.mean_check):
            check.setChecked(True)
            check.stateChanged.connect(self.refresh_results)
            actions.addWidget(check)
        actions.addStretch(1)
        self.layout.addLayout(actions)

        explanation = BodyLabel(
            "This demo compares automatic segmentation methods and shows how CLAHE-enhanced adaptive "
            "thresholding handles non-uniform illumination better than raw histogram thresholding."
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet(
            f"""
            font-size: 13px;
            color: {SECONDARY_TEXT};
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid {CARD_BORDER};
            border-radius: 10px;
            padding: 12px;
            """
        )
        self.layout.addWidget(explanation)

        image_grid = QGridLayout()
        image_grid.setSpacing(14)
        self.views = {
            "original": ImageViewer("Original Image"),
            "otsu": ImageViewer("Otsu Thresholding"),
            "gaussian": ImageViewer("Adaptive Gaussian Thresholding"),
            "mean": ImageViewer("Adaptive Mean Thresholding"),
            "enhanced": ImageViewer("CLAHE + Adaptive Thresholding"),
        }
        positions = {
            "original": (0, 0),
            "otsu": (0, 1),
            "gaussian": (0, 2),
            "mean": (1, 0),
            "enhanced": (1, 1),
        }
        for key, view in self.views.items():
            row, column = positions[key]
            image_grid.addWidget(view, row, column)
        self.layout.addLayout(image_grid)

        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(12)
        self.metric_cards = {
            "otsu": SegmentationMetricCard("Otsu Thresholding"),
            "gaussian": SegmentationMetricCard("Adaptive Gaussian"),
            "mean": SegmentationMetricCard("Adaptive Mean"),
            "enhanced": SegmentationMetricCard("CLAHE + Adaptive"),
        }
        for index, card in enumerate(self.metric_cards.values()):
            metrics_grid.addWidget(card, index // 2, index % 2)
        self.layout.addLayout(metrics_grid)
        self.layout.addStretch(1)

    def upload_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Traffic Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)",
        )
        if not path:
            return
        self.current_image = self.image_service.load(path)
        self.views["original"].set_image(self.current_image)
        self.refresh_results()

    def refresh_results(self) -> None:
        if self.current_image is None:
            return

        otsu = self.image_service.otsu_threshold(self.current_image)
        gaussian = self.image_service.adaptive_threshold(self.current_image, gaussian=True)
        mean = self.image_service.adaptive_threshold(self.current_image, gaussian=False)
        enhanced = self.image_service.enhanced_adaptive_threshold(self.current_image)

        if self.otsu_check.isChecked():
            self.views["otsu"].set_image(otsu)
        if self.gaussian_check.isChecked():
            self.views["gaussian"].set_image(gaussian)
        if self.mean_check.isChecked():
            self.views["mean"].set_image(mean)
        self.views["enhanced"].set_image(enhanced)

        results = {
            "otsu": otsu,
            "gaussian": gaussian,
            "mean": mean,
            "enhanced": enhanced,
        }
        for key, image in results.items():
            self.metric_cards[key].set_metrics(self.image_service.segmentation_metrics(image))
