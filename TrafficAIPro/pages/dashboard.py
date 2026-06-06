"""Dashboard page."""

from __future__ import annotations

from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QColor
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, StrongBodyLabel, SubtitleLabel

from ..models.detection import DetectionSummary, VEHICLE_CLASSES
from .base import Page
from ..widgets.metric_card import MetricCard


class DashboardPage(Page):
    """Executive overview of traffic detections."""

    def __init__(self) -> None:
        super().__init__("Dashboard", "DashboardPage")
        self.cards = {
            "total": MetricCard("Total Vehicles", "0", FluentIcon.SPEED_HIGH),
            "car": MetricCard("Cars", "0", FluentIcon.CAR),
            "bus": MetricCard("Buses", "0", FluentIcon.BUS),
            "truck": MetricCard("Trucks", "0", FluentIcon.TRAIN),
            "van": MetricCard("Vans", "0", FluentIcon.TAG),
        }

        grid = QGridLayout()
        grid.setSpacing(20)
        for index, card in enumerate(self.cards.values()):
            grid.addWidget(card, index // 5, index % 5)
        self.layout.addLayout(grid)
        self.layout.addSpacing(8)

        panels = QHBoxLayout()
        panels.setSpacing(20)
        self.summary = self._info_card("Recent Detection Summary", "No recent detection")
        self.stats = self._info_card("Quick Statistics", "Cars 0  |  Buses 0  |  Trucks 0  |  Vans 0")
        self.performance = self._info_card("Performance Metrics", "Processing time 0.00s  |  Average confidence 0%")
        self.model = self._info_card("Model Information", "YOLO26 model pending")
        for panel in (self.summary, self.stats, self.performance, self.model):
            panels.addWidget(panel)
        self.layout.addLayout(panels)
        self.layout.addStretch(1)

    def _info_card(self, title: str, body: str) -> CardWidget:
        """Create glassmorphism info card."""
        card = CardWidget()
        card.setBorderRadius(14)
        card.setStyleSheet(
            """
            CardWidget {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            """
        )
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        card.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)
        
        title_label = SubtitleLabel(title)
        title_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #1a1a1a;")
        layout.addWidget(title_label)
        
        label = BodyLabel(body)
        label.setWordWrap(True)
        label.setStyleSheet("font-size: 13px; color: #6B7280; line-height: 1.6;")
        card.body_label = label  # type: ignore[attr-defined]
        layout.addWidget(label)
        layout.addStretch(1)
        return card

    def update_summary(self, summary: DetectionSummary, model_name: str) -> None:
        self.cards["total"].set_value(summary.total)
        for key in VEHICLE_CLASSES:
            self.cards[key].set_value(summary.counts.get(key, 0))
        self.summary.body_label.setText(f"{summary.image_name}: {summary.total} vehicles detected")  # type: ignore[attr-defined]
        self.stats.body_label.setText(  # type: ignore[attr-defined]
            "  |  ".join(f"{key.title()} {summary.counts.get(key, 0)}" for key in VEHICLE_CLASSES)
        )
        self.performance.body_label.setText(  # type: ignore[attr-defined]
            f"Processing time {summary.processing_time:.2f}s  |  Average confidence {summary.average_confidence:.0%}"
        )
        self.model.body_label.setText(f"Active model: {model_name}")  # type: ignore[attr-defined]
