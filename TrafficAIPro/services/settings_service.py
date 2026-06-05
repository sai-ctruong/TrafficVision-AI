"""QSettings wrapper."""

from __future__ import annotations

from PyQt6.QtCore import QSettings
from qfluentwidgets import Theme

from ..utils.paths import DEFAULT_MODEL_PATH


class SettingsService:
    """Persist user preferences."""

    def __init__(self) -> None:
        self._settings = QSettings("TrafficAI", "TrafficAI Pro")

    @property
    def theme(self) -> Theme:
        value = self._settings.value("theme", "light", str)
        return Theme.DARK if value == "dark" else Theme.LIGHT

    @theme.setter
    def theme(self, value: Theme) -> None:
        self._settings.setValue("theme", "dark" if value == Theme.DARK else "light")

    @property
    def model_path(self) -> str:
        return self._settings.value("model_path", str(DEFAULT_MODEL_PATH), str)

    @model_path.setter
    def model_path(self, value: str) -> None:
        self._settings.setValue("model_path", value)

    @property
    def confidence(self) -> float:
        return float(self._settings.value("confidence", 0.5))

    @confidence.setter
    def confidence(self, value: float) -> None:
        self._settings.setValue("confidence", max(0.05, min(0.95, value)))
