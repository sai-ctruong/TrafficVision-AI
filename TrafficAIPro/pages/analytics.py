"""Analytics page."""

from __future__ import annotations

import pyqtgraph as pg
from PyQt6.QtWidgets import QGridLayout

from ..models.detection import DetectionSummary, VEHICLE_CLASSES
from .base import Page
from ..widgets.chart_widgets import ChartCard, PieChartWidget


class AnalyticsPage(Page):
    """Professional detection analytics dashboard."""

    def __init__(self) -> None:
        super().__init__("Analytics", "AnalyticsPage")
        pg.setConfigOptions(antialias=True)

        self.pie = PieChartWidget()
        self.bar = pg.PlotWidget()
        self.confidence = pg.PlotWidget()
        self.processing = pg.PlotWidget()
        for plot in (self.bar, self.confidence, self.processing):
            plot.setBackground(None)
            plot.showGrid(x=True, y=True, alpha=0.18)

        grid = QGridLayout()
        grid.setSpacing(14)
        grid.addWidget(ChartCard("Vehicle Distribution", self.pie), 0, 0)
        grid.addWidget(ChartCard("Vehicle Count Bar Chart", self.bar), 0, 1)
        grid.addWidget(ChartCard("Detection Confidence", self.confidence), 1, 0)
        grid.addWidget(ChartCard("Processing Time Statistics", self.processing), 1, 1)
        self.layout.addLayout(grid)
        self.layout.addStretch(1)
        self._summaries: list[DetectionSummary] = []
        self.refresh()

    def add_summary(self, summary: DetectionSummary) -> None:
        self._summaries.append(summary)
        self.refresh()

    def refresh(self) -> None:
        totals = {key: 0 for key in VEHICLE_CLASSES}
        for summary in self._summaries:
            for key in VEHICLE_CLASSES:
                totals[key] += summary.counts.get(key, 0)
        self.pie.set_values(totals)

        self.bar.clear()
        x = list(range(len(VEHICLE_CLASSES)))
        y = [totals[key] for key in VEHICLE_CLASSES]
        self.bar.addItem(pg.BarGraphItem(x=x, height=y, width=0.55, brush="#0078d4"))
        self.bar.getAxis("bottom").setTicks([list(zip(x, [key.title() for key in VEHICLE_CLASSES]))])

        self.confidence.clear()
        confidence_values = [summary.average_confidence * 100 for summary in self._summaries[-12:]]
        if confidence_values:
            self.confidence.plot(confidence_values, pen=pg.mkPen("#107c10", width=3), symbol="o", symbolBrush="#107c10")
        self.confidence.setLabel("left", "Confidence", units="%")

        self.processing.clear()
        processing_values = [summary.processing_time for summary in self._summaries[-12:]]
        if processing_values:
            self.processing.plot(processing_values, pen=pg.mkPen("#e81123", width=3), symbol="s", symbolBrush="#e81123")
        self.processing.setLabel("left", "Seconds")
