"""Application header with primary workflow actions and model status."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, FluentIcon, IconWidget, PrimaryPushButton, PushButton, StrongBodyLabel

from ..utils.theme import CARD_BACKGROUND, CARD_BORDER, ERROR, PRIMARY, SECONDARY_TEXT, SUCCESS, WARNING


class AppHeader(QFrame):
    """Top product header for the TrafficAI Pro shell."""

    load_model_requested = pyqtSignal()
    upload_image_requested = pyqtSignal()
    run_detection_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("AppHeader")
        self.setFixedHeight(92)
        self.setStyleSheet(
            f"""
            #AppHeader {{
                background: {CARD_BACKGROUND};
                border-bottom: 1px solid {CARD_BORDER};
            }}
            QLabel#StatusDot {{
                border-radius: 5px;
                background: {ERROR};
            }}
            """
        )

        root = QHBoxLayout(self)
        root.setContentsMargins(28, 14, 28, 14)
        root.setSpacing(18)

        logo = QWidget()
        logo.setFixedSize(48, 48)
        logo.setStyleSheet(f"background: #EAF3FF; border-radius: 14px;")
        logo_layout = QHBoxLayout(logo)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_icon = IconWidget(FluentIcon.CAR)
        logo_icon.setFixedSize(28, 28)
        logo_layout.addWidget(logo_icon, 0, Qt.AlignmentFlag.AlignCenter)
        root.addWidget(logo)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        title = StrongBodyLabel("TrafficAI Pro")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        subtitle = BodyLabel("Smart Traffic Vehicle Detection & Analytics System")
        subtitle.setStyleSheet(f"font-size: 13px; color: {SECONDARY_TEXT};")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        root.addLayout(title_box, 1)

        self.load_button = PushButton(FluentIcon.ROBOT, "Load Model")
        self.upload_button = PushButton(FluentIcon.PHOTO, "Upload Image")
        self.run_button = PrimaryPushButton(FluentIcon.PLAY, "Run Detection")
        self.load_button.clicked.connect(self.load_model_requested)
        self.upload_button.clicked.connect(self.upload_image_requested)
        self.run_button.clicked.connect(self.run_detection_requested)
        root.addWidget(self.load_button)
        root.addWidget(self.upload_button)
        root.addWidget(self.run_button)

        status_box = QWidget()
        status_box.setObjectName("HeaderStatus")
        status_box.setStyleSheet(
            f"""
            #HeaderStatus {{
                background: #F8FAFC;
                border: 1px solid {CARD_BORDER};
                border-radius: 18px;
            }}
            """
        )
        status_layout = QHBoxLayout(status_box)
        status_layout.setContentsMargins(14, 7, 14, 7)
        status_layout.setSpacing(8)
        self.status_label = BodyLabel("Model: Not Loaded")
        self.status_label.setStyleSheet(f"color: {SECONDARY_TEXT}; font-weight: 600;")
        self.status_dot = QLabel()
        self.status_dot.setObjectName("StatusDot")
        self.status_dot.setFixedSize(10, 10)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.status_dot)
        root.addWidget(status_box)

    def set_status(self, text: str, state: str) -> None:
        """Set model status chip state."""
        color = {"loaded": SUCCESS, "processing": WARNING, "error": ERROR}.get(state, ERROR)
        self.status_label.setText(text)
        self.status_dot.setStyleSheet(f"border-radius: 5px; background: {color};")

