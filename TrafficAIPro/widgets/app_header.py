"""Professional application header with workflow actions and model status."""

from __future__ import annotations

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, FluentIcon, IconWidget, IndeterminateProgressRing, PrimaryPushButton, PushButton, StrongBodyLabel

from ..utils.theme import CARD_BORDER, ERROR, PRIMARY, SECONDARY_TEXT, SUCCESS, WARNING


class ModelStatusPill(QWidget):
    """Modern status indicator pill with colored dot, text, and loading animation."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("StatusPill")
        self.setStyleSheet(
            f"""
            #StatusPill {{
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid {CARD_BORDER};
                border-radius: 20px;
                padding: 8px 16px;
            }}
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)

        # Status dot
        self.dot = QLabel()
        self.dot.setFixedSize(10, 10)
        self.dot.setStyleSheet(
            f"""
            background: {ERROR};
            border-radius: 5px;
            """
        )
        layout.addWidget(self.dot)

        # Loading spinner (hidden by default)
        self.spinner = IndeterminateProgressRing(self)
        self.spinner.setFixedSize(16, 16)
        self.spinner.setStrokeWidth(2)
        self.spinner.hide()
        layout.addWidget(self.spinner)

        # Status text
        self.label = BodyLabel("Model Not Loaded")
        self.label.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 600;
            color: {SECONDARY_TEXT};
            """
        )
        layout.addWidget(self.label)

    def set_status(self, text: str, state: str) -> None:
        """Update status pill appearance."""
        color_map = {
            "loaded": SUCCESS,
            "loading": WARNING,
            "processing": WARNING,
            "error": ERROR,
            "not_loaded": ERROR,
        }
        color = color_map.get(state, ERROR)
        
        # Update dot color
        self.dot.setStyleSheet(
            f"""
            background: {color};
            border-radius: 5px;
            """
        )
        
        # Show/hide spinner for loading states
        if state in ["loading", "processing"]:
            self.dot.hide()
            self.spinner.show()
        else:
            self.spinner.hide()
            self.dot.show()
        
        # Update text
        self.label.setText(text)


class AppHeader(QFrame):
    """72px professional header with branding and actions."""

    load_model_requested = pyqtSignal()
    upload_image_requested = pyqtSignal()
    run_detection_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("AppHeader")
        self.setFixedHeight(72)
        self.setStyleSheet(
            f"""
            #AppHeader {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:0.5 #FAFBFD, stop:1 #F8FAFC);
                border-bottom: 1px solid {CARD_BORDER};
            }}
            """
        )

        root = QHBoxLayout(self)
        root.setContentsMargins(32, 16, 32, 16)
        root.setSpacing(24)

        # Left: Branding
        brand_container = QWidget()
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(2)

        title = StrongBodyLabel("TrafficAI Pro")
        title.setStyleSheet(
            """
            font-size: 20px;
            font-weight: 700;
            color: #1a1a1a;
            letter-spacing: -0.4px;
            """
        )
        brand_layout.addWidget(title)

        subtitle = BodyLabel("Smart Traffic Vehicle Detection & Analytics System")
        subtitle.setStyleSheet(
            f"""
            font-size: 12px;
            color: {SECONDARY_TEXT};
            font-weight: 500;
            """
        )
        brand_layout.addWidget(subtitle)

        root.addWidget(brand_container)
        root.addStretch(1)

        # Right: Action buttons + status
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)

        self.load_button = PushButton("Load Model")
        self.load_button.setIcon(FluentIcon.ROBOT)
        
        self.upload_button = PushButton("Upload Image")
        self.upload_button.setIcon(FluentIcon.PHOTO)
        
        self.run_button = PrimaryPushButton("Run Detection")
        self.run_button.setIcon(FluentIcon.PLAY)

        # Set button sizes
        for btn in [self.load_button, self.upload_button, self.run_button]:
            btn.setFixedHeight(40)
            btn.setMinimumWidth(120)

        self.load_button.clicked.connect(self.load_model_requested)
        self.upload_button.clicked.connect(self.upload_image_requested)
        self.run_button.clicked.connect(self.run_detection_requested)

        actions_layout.addWidget(self.load_button)
        actions_layout.addWidget(self.upload_button)
        actions_layout.addWidget(self.run_button)

        # Separator
        separator = QWidget()
        separator.setFixedSize(1, 40)
        separator.setStyleSheet(f"background: {CARD_BORDER};")
        actions_layout.addWidget(separator)

        # Status pill
        self.status_pill = ModelStatusPill()
        actions_layout.addWidget(self.status_pill)

        root.addLayout(actions_layout)

    def set_status(self, text: str, state: str) -> None:
        """Update model status pill."""
        self.status_pill.set_status(text, state)
