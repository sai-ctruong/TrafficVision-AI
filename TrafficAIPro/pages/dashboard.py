"""Dashboard page."""

from __future__ import annotations

from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
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
        grid.setSpacing(14)
        for index, card in enumerate(self.cards.values()):
            grid.addWidget(card, index // 5, index % 5)
        self.layout.addLayout(grid)

        panels = QHBoxLayout()
        panels.setSpacing(14)
        self.summary = self._info_card("Recent Detection Summary", "No recent detection")
        self.stats = self._info_card("Quick Statistics", "Cars 0  |  Buses 0  |  Trucks 0  |  Vans 0")
        self.performance = self._info_card("Performance Metrics", "Processing time 0.00s  |  Average confidence 0%")
        self.model = self._info_card("Model Information", "YOLO26 model pending")
        for panel in (self.summary, self.stats, self.performance, self.model):
            panels.addWidget(panel)
        self.layout.addLayout(panels)
        self.layout.addStretch(1)

    def _info_card(self, title: str, body: str) -> CardWidget:
        card = CardWidget()
        card.setBorderRadius(8)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)
        layout.addWidget(SubtitleLabel(title))
        label = BodyLabel(body)
        label.setWordWrap(True)
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
