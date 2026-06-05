"""Settings page."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, LineEdit, PrimaryPushButton, PushButton, Slider, SwitchButton

from .base import Page
from ..services.settings_service import SettingsService


class SettingsPage(Page):
    """Theme, model and export preferences."""

    theme_changed = pyqtSignal(bool)
    model_path_changed = pyqtSignal(str)

    def __init__(self, settings: SettingsService) -> None:
        super().__init__("Settings", "SettingsPage")
        self.settings = settings

        card = CardWidget()
        card.setBorderRadius(8)
        grid = QGridLayout(card)
        grid.setContentsMargins(18, 16, 18, 16)
        grid.setSpacing(14)

        self.theme_switch = SwitchButton()
        self.theme_switch.setChecked(settings.theme.name.lower() == "dark")
        self.theme_switch.checkedChanged.connect(self.theme_changed.emit)
        grid.addWidget(BodyLabel("Theme Switch"), 0, 0)
        grid.addWidget(self.theme_switch, 0, 1)

        self.model_path = LineEdit()
        self.model_path.setText(settings.model_path)
        self.browse = PushButton(FluentIcon.FOLDER, "Browse")
        self.browse.clicked.connect(self.pick_model)
        model_row = QHBoxLayout()
        model_row.addWidget(self.model_path, 1)
        model_row.addWidget(self.browse)
        grid.addWidget(BodyLabel("Model Path"), 1, 0)
        grid.addLayout(model_row, 1, 1)

        confidence_box = QVBoxLayout()
        self.confidence = Slider()
        self.confidence.setRange(5, 95)
        self.confidence.setValue(int(settings.confidence * 100))
        self.confidence.valueChanged.connect(self.save_confidence)
        self.confidence_label = BodyLabel(f"{self.confidence.value()}%")
        confidence_box.addWidget(self.confidence)
        confidence_box.addWidget(self.confidence_label)
        grid.addWidget(BodyLabel("Default Confidence Threshold"), 2, 0)
        grid.addLayout(confidence_box, 2, 1)

        self.save_button = PrimaryPushButton(FluentIcon.SAVE, "Save Settings")
        self.save_button.clicked.connect(self.save)
        grid.addWidget(BodyLabel("Export Settings"), 3, 0)
        grid.addWidget(BodyLabel("CSV history export and annotated image export ready"), 3, 1)
        grid.addWidget(self.save_button, 4, 1)
        self.layout.addWidget(card)
        self.layout.addStretch(1)

    def pick_model(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select model", self.model_path.text(), "YOLO Weights (*.pt)")
        if path:
            self.model_path.setText(path)
            self.save()

    def save_confidence(self, value: int) -> None:
        self.confidence_label.setText(f"{value}%")
        self.settings.confidence = value / 100

    def save(self) -> None:
        self.settings.model_path = self.model_path.text()
        self.model_path_changed.emit(self.settings.model_path)
