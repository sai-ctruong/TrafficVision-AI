"""Main Fluent window."""

from __future__ import annotations

from PyQt6.QtCore import QSize
from qfluentwidgets import BodyLabel, FluentIcon, FluentWindow, NavigationItemPosition, Theme, setTheme

from ..database.history_repository import HistoryRepository
from ..pages.analytics import AnalyticsPage
from ..pages.dashboard import DashboardPage
from ..pages.detection import VehicleDetectionPage
from ..pages.history import HistoryPage
from ..pages.image_processing import ImageProcessingPage
from ..pages.settings import SettingsPage
from ..services.detection_service import VehicleDetectionService
from ..services.image_service import ImageEnhancementService
from ..services.settings_service import SettingsService


class TrafficAIWindow(FluentWindow):
    """Production-style shell for TrafficAI Pro."""

    def __init__(self) -> None:
        self.settings_service = SettingsService()
        setTheme(self.settings_service.theme)
        super().__init__()
        self.setWindowTitle("TrafficAI Pro - Smart Traffic Vehicle Detection & Analytics System")
        self.resize(1480, 900)
        self.setMinimumSize(QSize(1180, 760))

        self.image_service = ImageEnhancementService()
        self.detection_service = VehicleDetectionService(self.settings_service.model_path)
        self.history_repository = HistoryRepository()

        self.dashboard = DashboardPage()
        self.processing = ImageProcessingPage(self.image_service)
        self.detection = VehicleDetectionPage(
            self.detection_service,
            self.settings_service,
            self.history_repository,
        )
        self.analytics = AnalyticsPage()
        self.history = HistoryPage(self.history_repository)
        self.settings = SettingsPage(self.settings_service)

        self._init_navigation()
        self._connect_signals()
        self._init_status_bar()
        self.setStyleSheet(
            """
            QWidget { font-family: 'Segoe UI', 'Microsoft YaHei UI'; }
            QScrollArea { border: none; background: transparent; }
            #MetricValue { color: #0078d4; }
            """
        )

    def _init_navigation(self) -> None:
        self.addSubInterface(self.dashboard, FluentIcon.HOME, "Dashboard")
        self.addSubInterface(self.processing, FluentIcon.PHOTO, "Image Processing")
        self.addSubInterface(self.detection, FluentIcon.ROBOT, "Vehicle Detection")
        self.addSubInterface(self.analytics, FluentIcon.PIE_SINGLE, "Analytics")
        self.addSubInterface(self.history, FluentIcon.HISTORY, "History")
        self.addSubInterface(
            self.settings,
            FluentIcon.SETTING,
            "Settings",
            NavigationItemPosition.BOTTOM,
        )

    def _connect_signals(self) -> None:
        self.processing.image_changed.connect(self.detection.set_image)
        self.detection.detection_completed.connect(self._handle_detection_complete)
        self.detection.model_status_changed.connect(self._set_model_status)
        self.settings.theme_changed.connect(self._toggle_theme)
        self.settings.model_path_changed.connect(self._set_model_path)

    def _init_status_bar(self) -> None:
        self.status = BodyLabel("Model status: not loaded  |  Ready")
        self.status.setFixedHeight(32)
        self.status.setStyleSheet("padding-left: 16px; color: #6b6b6b;")
        self.widgetLayout.addWidget(self.status)

    def _handle_detection_complete(self, summary) -> None:
        self.dashboard.update_summary(summary, self.detection_service.model_name)
        self.analytics.add_summary(summary)
        self.history.refresh()
        self.status.setText(
            f"Model status: {self.detection_service.model_name}  |  "
            f"Last run: {summary.total} vehicles in {summary.processing_time:.2f}s"
        )

    def _set_model_status(self, message: str) -> None:
        self.status.setText(f"Model status: {message}  |  Ready")

    def _toggle_theme(self, dark: bool) -> None:
        theme = Theme.DARK if dark else Theme.LIGHT
        self.settings_service.theme = theme
        setTheme(theme)

    def _set_model_path(self, path: str) -> None:
        self.detection_service.model_path = path
        self.status.setText(f"Model status: selected {path}")
