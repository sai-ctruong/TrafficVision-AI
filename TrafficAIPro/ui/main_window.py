"""Main application window with custom header and sidebar."""

from __future__ import annotations

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from qfluentwidgets import Theme, setTheme

from ..database.history_repository import HistoryRepository
from ..pages.analytics import AnalyticsPage
from ..pages.dashboard import DashboardPage
from ..pages.detection import VehicleDetectionPage
from ..pages.history import HistoryPage
from ..pages.image_processing import ImageProcessingPage
from ..pages.video_analysis import VideoAnalysisPage
from ..services.detection_service import VehicleDetectionService
from ..services.arduino_service import ArduinoService
from ..services.image_service import ImageEnhancementService
from ..services.settings_service import SettingsService
from ..utils.theme import APP_BACKGROUND, app_style_sheet
from ..widgets.app_header import AppHeader
from ..widgets.sidebar import Sidebar


ARDUINO_MOCK_MODE = False
ARDUINO_PORT = "COM3"  # Example real port: "COM3"


class TrafficAIWindow(QMainWindow):
    """Commercial-grade TrafficAI Pro window with custom layout."""

    def __init__(self) -> None:
        super().__init__()
        
        # Services
        self.settings_service = SettingsService()
        setTheme(self.settings_service.theme)
        self.image_service = ImageEnhancementService()
        self.detection_service = VehicleDetectionService(self.settings_service.model_path)
        self.arduino_service = ArduinoService(
            mock_mode=ARDUINO_MOCK_MODE,
            port=ARDUINO_PORT,
        )
        self.arduino_service.connect()
        self.history_repository = HistoryRepository()

        # Window setup
        self.setWindowTitle("TrafficAI Pro")
        self.resize(1520, 920)
        self.setMinimumSize(QSize(1280, 800))
        
        # Main container
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.header = AppHeader()
        main_layout.addWidget(self.header)

        # Content area: sidebar + pages
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)

        # Pages stack
        self.pages_stack = QStackedWidget()
        self.pages_stack.setStyleSheet("background: transparent;")
        
        # Initialize pages
        self.dashboard = DashboardPage()
        self._update_hardware_status()
        self.processing = ImageProcessingPage(self.image_service)
        self.detection = VehicleDetectionPage(
            self.detection_service,
            self.settings_service,
            self.history_repository,
        )
        self.video = VideoAnalysisPage(
            self.image_service,
            self.detection_service,
            self.settings_service,
            self.arduino_service,
        )
        self.analytics = AnalyticsPage()
        self.history = HistoryPage(self.history_repository)

        # Add pages to stack
        self.pages_map = {
            "dashboard": self.dashboard,
            "processing": self.processing,
            "detection": self.detection,
            "video": self.video,
            "analytics": self.analytics,
            "history": self.history,
        }
        
        for page in self.pages_map.values():
            self.pages_stack.addWidget(page)
        
        content_layout.addWidget(self.pages_stack, 1)
        main_layout.addLayout(content_layout, 1)

        # Connect signals
        self._connect_signals()
        
        # Show dashboard
        self.show_page("dashboard")

        # Apply global Warm Editorial QSS
        self.setStyleSheet(
            f"QMainWindow {{ background: {APP_BACKGROUND}; }}" + app_style_sheet()
        )
        QTimer.singleShot(0, self._auto_load_model)

    def _connect_signals(self) -> None:
        """Connect all signal handlers."""
        # Header actions
        self.header.upload_image_requested.connect(self._handle_upload_image)
        
        # Sidebar navigation
        self.sidebar.page_requested.connect(self.show_page)
        
        # Page interactions
        self.processing.image_changed.connect(self.detection.set_image)
        self.detection.detection_completed.connect(self._handle_detection_complete)
        self.detection.model_status_changed.connect(self._update_model_status)
        self.video.hardware_status_changed.connect(self._update_hardware_status)

    def show_page(self, key: str) -> None:
        """Switch to specified page."""
        if key in self.pages_map:
            self.pages_stack.setCurrentWidget(self.pages_map[key])
            self.sidebar.set_current(key)
            eyebrow_map = {
                "dashboard": "Workspace",
                "processing": "Pre-processing",
                "detection": "Inference",
                "video": "Live Tracking",
                "analytics": "Reports",
                "history": "Detection History",
            }
            if hasattr(self.header, "set_eyebrow"):
                self.header.set_eyebrow(eyebrow_map.get(key, "Workspace"))

    def _handle_upload_image(self) -> None:
        """Handle upload image button click."""
        self.show_page("processing")
        # The processing page has its own upload button

    def _auto_load_model(self) -> None:
        """Load the configured YOLO model once when the application starts."""
        self._update_model_status("Loading model...")
        try:
            self.detection_service.load_model(self.settings_service.model_path)
        except Exception as exc:
            self._update_model_status(f"Model error: {exc}")
            return
        self._update_model_status(f"Model loaded: {self.detection_service.model_name}")

    def _handle_detection_complete(self, summary) -> None:
        """Update UI after detection completes."""
        self.dashboard.update_summary(summary, self.detection_service.model_name)
        self._send_vehicle_count_to_arduino(summary)
        self.analytics.add_summary(summary)
        self._update_enhancement_analytics(summary)
        self.history.refresh()
        
        self._update_model_status(f"Model loaded: {self.detection_service.model_name}")

    def _update_enhancement_analytics(self, enhanced_summary) -> None:
        """Update original vs enhanced analytics without storing duplicate history."""
        original_image = self.processing.original_image
        enhanced_image = self.processing.enhanced_image
        if enhanced_image is None:
            enhanced_image = self.detection.current_image
        original_summary = None

        if original_image is not None and self.detection_service.is_loaded:
            try:
                _, original_summary = self.detection_service.detect(
                    original_image,
                    f"Original {enhanced_summary.image_name}",
                    0.25,
                )
            except Exception:
                original_summary = None

        self.analytics.update_enhancement_comparison(
            original_image,
            enhanced_image,
            original_summary,
            enhanced_summary,
        )

    def _update_model_status(self, message: str) -> None:
        """Update model status in header."""
        message_lower = message.lower()
        
        if "loaded" in message_lower and "not" not in message_lower:
            state = "loaded"
            text = message
        elif "loading" in message_lower:
            state = "loading"
            text = message
        elif "processing" in message_lower:
            state = "processing"
            text = message
        else:
            state = "not_loaded"
            text = message
        
        self.header.set_status(text, state)
        sidebar_palette = {
            "loaded": "#4A6741",
            "loading": "#C9882A",
            "processing": "#C9882A",
            "error": "#C4512A",
            "not_loaded": "#C4512A",
        }
        self.sidebar.set_status(text, sidebar_palette.get(state, "#9A7560"))

    def _send_vehicle_count_to_arduino(self, summary) -> None:
        """Send the latest detection counts to the optional Arduino service."""
        try:
            self.arduino_service.send_vehicle_count(
                summary.counts.get("car", 0),
                summary.counts.get("bus", 0),
                summary.counts.get("truck", 0),
                summary.counts.get("van", 0),
            )
        except Exception as exc:
            print(f"[ArduinoService] Vehicle count send skipped: {exc}")
        finally:
            self._update_hardware_status()

    def _update_hardware_status(self) -> None:
        self.dashboard.update_hardware_status(
            self.arduino_service.mode_label,
            self.arduino_service.traffic_light_label,
            self.arduino_service.last_sent_data,
        )

    def _toggle_theme(self, dark: bool) -> None:
        """Toggle between light and dark theme."""
        theme = Theme.DARK if dark else Theme.LIGHT
        self.settings_service.theme = theme
        setTheme(theme)

    def _set_model_path(self, path: str) -> None:
        """Update model path in detection service."""
        self.detection_service.model_path = path
        filename = path.split('/')[-1] if '/' in path else path.split('\\')[-1]
        self.header.set_status(f"Selected: {filename}", "processing")

    def closeEvent(self, event) -> None:
        self.arduino_service.disconnect()
        super().closeEvent(event)
