"""Image processing page."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, CheckBox, FluentIcon, PrimaryPushButton, Slider

from .base import Page
from ..services.image_service import ImageEnhancementService
from ..widgets.image_viewer import ImageViewer


class ImageProcessingPage(Page):
    """Upload and enhance images with live preview."""

    image_changed = pyqtSignal(object, str)

    def __init__(self, image_service: ImageEnhancementService) -> None:
        super().__init__("Image Processing", "ImageProcessingPage")
        self.image_service = image_service
        self.image_path = ""
        self.original_image: np.ndarray | None = None
        self.enhanced_image: np.ndarray | None = None

        actions = QHBoxLayout()
        self.upload_button = PrimaryPushButton(FluentIcon.ADD, "Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        actions.addWidget(self.upload_button)
        actions.addStretch(1)
        self.layout.addLayout(actions)

        preview_grid = QGridLayout()
        preview_grid.setSpacing(14)
        self.original_view = ImageViewer("Original Image")
        self.enhanced_view = ImageViewer("Enhanced Image")
        preview_grid.addWidget(self.original_view, 0, 0)
        preview_grid.addWidget(self.enhanced_view, 0, 1)
        self.layout.addLayout(preview_grid)

        controls = QGridLayout()
        controls.setSpacing(14)
        self.clahe_check = CheckBox("CLAHE")
        self.clahe_check.setChecked(True)
        controls.addWidget(self.clahe_check, 0, 0)
        self.gamma = self._slider("Gamma", 10, 30, 10, controls, 0, 1)
        self.brightness = self._slider("Brightness", -60, 60, 0, controls, 1, 0)
        self.contrast = self._slider("Contrast", 5, 25, 10, controls, 1, 1)
        self.median = self._slider("Median Filter", 1, 9, 1, controls, 2, 0)
        self.layout.addLayout(controls)
        self.layout.addStretch(1)
        self.clahe_check.stateChanged.connect(self.apply_live_preview)

    def _slider(self, label: str, minimum: int, maximum: int, value: int, layout: QGridLayout, row: int, col: int) -> Slider:
        wrapper = QVBoxLayout()
        wrapper.addWidget(BodyLabel(label))
        slider = Slider()
        slider.setRange(minimum, maximum)
        slider.setValue(value)
        slider.valueChanged.connect(self.apply_live_preview)
        wrapper.addWidget(slider)
        layout.addLayout(wrapper, row, col)
        return slider

    def upload_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open traffic image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)",
        )
        if not path:
            return
        self.image_path = path
        self.original_image = self.image_service.load(path)
        self.original_view.set_image(self.original_image)
        self.apply_live_preview()

    def apply_live_preview(self) -> None:
        if self.original_image is None:
            return
        self.enhanced_image = self.image_service.enhance(
            self.original_image,
            use_clahe=self.clahe_check.isChecked(),
            gamma=self.gamma.value() / 10,
            brightness=self.brightness.value(),
            contrast=self.contrast.value() / 10,
            median_kernel=self.median.value(),
        )
        self.enhanced_view.set_image(self.enhanced_image)
        self.image_changed.emit(self.enhanced_image, Path(self.image_path).name)
