"""Analytics page."""

from __future__ import annotations

import cv2
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, IconWidget, StrongBodyLabel, SubtitleLabel

from ..models.detection import DetectionSummary, VEHICLE_CLASSES
from ..utils.theme import PRIMARY, SECONDARY_TEXT, SUCCESS, TEXT, WARNING
from ..widgets.chart_widgets import ChartCard, PieChartWidget, VehicleBarChartWidget
from .base import Page


class GlassCard(CardWidget):
    """Shared glassmorphism card shell for analytics widgets."""

    def __init__(self, title: str, icon: FluentIcon | None = None) -> None:
        super().__init__()
        self.setBorderRadius(14)
        self.setStyleSheet(
            """
            CardWidget {
                background: #FFFFFF;
                border: 1px solid #E5EAF2;
            }
            """
        )

        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(20, 18, 20, 20)
        self.body.setSpacing(14)

        header = QHBoxLayout()
        header.setSpacing(10)
        if icon is not None:
            icon_widget = IconWidget(icon)
            icon_widget.setFixedSize(24, 24)
            header.addWidget(icon_widget)

        title_label = SubtitleLabel(title)
        title_label.setStyleSheet(
            f"""
            font-size: 17px;
            font-weight: 700;
            color: {TEXT};
            """
        )
        header.addWidget(title_label)
        header.addStretch(1)
        self.body.addLayout(header)


class AnalyticsImagePanel(CardWidget):
    """Compact image preview used by the enhancement comparison."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setBorderRadius(10)
        self._pixmap: QPixmap | None = None
        self.setStyleSheet(
            """
            CardWidget {
                background: rgba(248, 250, 252, 0.96);
                border: 1px solid rgba(229, 234, 242, 0.9);
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.title_label = BodyLabel(title)
        self.title_label.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 700;
            color: {PRIMARY};
            """
        )
        layout.addWidget(self.title_label)

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(210)
        self.image_label.setStyleSheet(
            """
            QLabel {
                background: rgba(15, 108, 189, 0.08);
                border-radius: 8px;
                color: #7A869A;
                font-size: 13px;
                font-weight: 600;
            }
            """
        )
        layout.addWidget(self.image_label, 1)

    def set_image(self, image: np.ndarray | None) -> None:
        if image is None:
            self._pixmap = None
            self.image_label.setPixmap(QPixmap())
            self.image_label.setText("No image loaded")
            return

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb.shape
        qimage = QImage(rgb.data, width, height, channels * width, QImage.Format.Format_RGB888).copy()
        self._pixmap = QPixmap.fromImage(qimage)
        self._render()

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self._render()

    def _render(self) -> None:
        if self._pixmap is None:
            return
        scaled = self._pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setText("")
        self.image_label.setPixmap(scaled)


class ComparisonMetricCard(CardWidget):
    """Original/enhanced metric comparison card."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setBorderRadius(10)
        self.setStyleSheet(
            """
            CardWidget {
                background: rgba(255, 255, 255, 0.96);
                border: 1px solid rgba(229, 234, 242, 0.95);
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        title_label = BodyLabel(title)
        title_label.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 800;
            color: {TEXT};
            """
        )
        layout.addWidget(title_label)

        self.original_label = BodyLabel("Original: --")
        self.enhanced_label = BodyLabel("Enhanced: --")
        for label in (self.original_label, self.enhanced_label):
            label.setStyleSheet(
                f"""
                font-size: 13px;
                color: {SECONDARY_TEXT};
                font-weight: 600;
                """
            )
            layout.addWidget(label)

    def set_values(self, original: str, enhanced: str) -> None:
        self.original_label.setText(f"Original: {original}")
        self.enhanced_label.setText(f"Enhanced: {enhanced}")


class KpiCard(CardWidget):
    """Modern KPI card with progress indicator."""

    def __init__(self, title: str, icon: FluentIcon, accent: str = PRIMARY) -> None:
        super().__init__()
        self.accent = accent
        self.setBorderRadius(12)
        self.setMinimumHeight(128)
        self.setStyleSheet(
            """
            CardWidget {
                background: rgba(255, 255, 255, 0.96);
                border: 1px solid rgba(229, 234, 242, 0.95);
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(10)
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(24, 24)
        header.addWidget(icon_widget)

        title_label = BodyLabel(title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 700;
            color: {SECONDARY_TEXT};
            """
        )
        header.addWidget(title_label, 1)
        layout.addLayout(header)

        self.value_label = StrongBodyLabel("--")
        self.value_label.setStyleSheet(
            f"""
            font-size: 30px;
            font-weight: 800;
            color: {accent};
            """
        )
        layout.addWidget(self.value_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet(
            f"""
            QProgressBar {{
                background: rgba(15, 108, 189, 0.10);
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background: {accent};
                border-radius: 4px;
            }}
            """
        )
        layout.addWidget(self.progress)

    def set_value(self, value: str, progress: int) -> None:
        self.value_label.setText(value)
        self.progress.setValue(max(0, min(100, progress)))


class StoryStep(QFrame):
    """Small story chip for the image-processing narrative."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self.setStyleSheet(
            """
            QFrame {
                background: rgba(15, 108, 189, 0.08);
                border: 1px solid rgba(15, 108, 189, 0.16);
                border-radius: 12px;
            }
            """
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        label = BodyLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"""
            font-size: 12px;
            font-weight: 800;
            color: {PRIMARY};
            """
        )
        layout.addWidget(label)


class AnalyticsPage(Page):
    """Digital image processing analytics dashboard."""

    def __init__(self) -> None:
        super().__init__("Analytics", "AnalyticsPage")
        self.view.background.hide()
        self.view.overlay.hide()
        self.view.setStyleSheet("#PageView { background: #F3F6FA; }")

        self.pie = PieChartWidget()
        self.bar = VehicleBarChartWidget()

        top_grid = QGridLayout()
        top_grid.setSpacing(14)
        top_grid.addWidget(ChartCard("Vehicle Distribution", self.pie), 0, 0)
        top_grid.addWidget(ChartCard("Vehicle Count Bar Chart", self.bar), 0, 1)
        top_grid.setColumnStretch(0, 1)
        top_grid.setColumnStretch(1, 1)
        self.layout.addLayout(top_grid)

        bottom_grid = QGridLayout()
        bottom_grid.setSpacing(14)
        self.comparison_card = self._build_comparison_card()
        self.impact_card = self._build_impact_card()
        bottom_grid.addWidget(self.comparison_card, 0, 0)
        bottom_grid.addWidget(self.impact_card, 0, 1)
        bottom_grid.setColumnStretch(0, 1)
        bottom_grid.setColumnStretch(1, 1)
        self.layout.addLayout(bottom_grid)
        self.layout.addStretch(1)

        self._summaries: list[DetectionSummary] = []
        self.refresh()

    def _build_comparison_card(self) -> GlassCard:
        card = GlassCard("Image Enhancement Comparison", FluentIcon.PHOTO)

        image_row = QHBoxLayout()
        image_row.setSpacing(12)
        self.original_panel = AnalyticsImagePanel("Original Image")
        self.enhanced_panel = AnalyticsImagePanel("Enhanced Image")
        image_row.addWidget(self.original_panel)
        image_row.addWidget(self.enhanced_panel)
        card.body.addLayout(image_row)

        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(10)
        self.comparison_metrics = {
            "brightness": ComparisonMetricCard("Brightness"),
            "contrast": ComparisonMetricCard("Contrast"),
            "vehicles": ComparisonMetricCard("Detected Vehicles"),
            "confidence": ComparisonMetricCard("Average Confidence"),
        }
        for index, metric in enumerate(self.comparison_metrics.values()):
            metrics_grid.addWidget(metric, index // 2, index % 2)
        card.body.addLayout(metrics_grid)
        return card

    def _build_impact_card(self) -> GlassCard:
        card = GlassCard("Enhancement Effectiveness", FluentIcon.SPEED_HIGH)

        story = QVBoxLayout()
        story.setSpacing(6)
        for index, text in enumerate(
            (
                "Original Image",
                "Image Enhancement",
                "Better Detection",
                "Higher Vehicle Count",
                "Higher Confidence",
            )
        ):
            story.addWidget(StoryStep(text))
            if index < 4:
                arrow = BodyLabel("v")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arrow.setStyleSheet(f"font-size: 13px; font-weight: 900; color: {SECONDARY_TEXT};")
                story.addWidget(arrow)
        card.body.addLayout(story)

        techniques = BodyLabel("CLAHE + Gamma Correction + Median Filter + Brightness Adjustment")
        techniques.setWordWrap(True)
        techniques.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 700;
            color: {SECONDARY_TEXT};
            padding: 2px 0px 4px 0px;
            """
        )
        card.body.addWidget(techniques)

        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(12)
        self.kpis = {
            "detection": KpiCard("Detection Improvement", FluentIcon.CAR, SUCCESS),
            "confidence": KpiCard("Confidence Improvement", FluentIcon.SPEED_HIGH, PRIMARY),
            "additional": KpiCard("Additional Vehicles Detected", FluentIcon.ADD, WARNING),
            "quality": KpiCard("Image Quality Score", FluentIcon.PALETTE, "#7C3AED"),
        }
        for index, widget in enumerate(self.kpis.values()):
            kpi_grid.addWidget(widget, index // 2, index % 2)
        card.body.addLayout(kpi_grid, 1)
        return card

    def add_summary(self, summary: DetectionSummary) -> None:
        self._summaries.append(summary)
        self.refresh()

    def update_enhancement_comparison(
        self,
        original_image: np.ndarray | None,
        enhanced_image: np.ndarray | None,
        original_summary: DetectionSummary | None,
        enhanced_summary: DetectionSummary,
    ) -> None:
        """Update the DIP effectiveness section with image and detection metrics."""
        self.original_panel.set_image(original_image)
        self.enhanced_panel.set_image(enhanced_image)

        original_brightness, original_contrast = self._image_metrics(original_image)
        enhanced_brightness, enhanced_contrast = self._image_metrics(enhanced_image)

        original_total = original_summary.total if original_summary else 0
        enhanced_total = enhanced_summary.total
        original_confidence = original_summary.average_confidence if original_summary else 0.0
        enhanced_confidence = enhanced_summary.average_confidence

        self.comparison_metrics["brightness"].set_values(
            self._number_or_dash(original_brightness),
            self._number_or_dash(enhanced_brightness),
        )
        self.comparison_metrics["contrast"].set_values(
            self._number_or_dash(original_contrast),
            self._number_or_dash(enhanced_contrast),
        )
        self.comparison_metrics["vehicles"].set_values(str(original_total), str(enhanced_total))
        self.comparison_metrics["confidence"].set_values(
            self._percent(original_confidence),
            self._percent(enhanced_confidence),
        )

        detection_improvement = self._relative_gain(original_total, enhanced_total)
        confidence_improvement = (enhanced_confidence - original_confidence) * 100
        additional = enhanced_total - original_total
        quality_score = self._quality_score(enhanced_brightness, enhanced_contrast, enhanced_confidence)

        self.kpis["detection"].set_value(
            self._signed_percent(detection_improvement),
            int(min(100, max(0, detection_improvement))),
        )
        self.kpis["confidence"].set_value(
            self._signed_delta(confidence_improvement),
            int(min(100, max(0, confidence_improvement * 4))),
        )
        self.kpis["additional"].set_value(
            f"{additional:+d}",
            int(min(100, max(0, additional * 20))),
        )
        self.kpis["quality"].set_value(f"{quality_score}/100", quality_score)

    def refresh(self) -> None:
        totals = {key: 0 for key in VEHICLE_CLASSES}
        for summary in self._summaries:
            for key in VEHICLE_CLASSES:
                totals[key] += summary.counts.get(key, 0)
        self.pie.set_values(totals)

        self.bar.set_values(totals)

    def _image_metrics(self, image: np.ndarray | None) -> tuple[float | None, float | None]:
        if image is None:
            return None, None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return float(np.mean(gray)), float(np.std(gray))

    def _quality_score(
        self,
        brightness: float | None,
        contrast: float | None,
        confidence: float,
    ) -> int:
        if brightness is None or contrast is None:
            return 0
        brightness_score = max(0.0, 100.0 - abs(brightness - 145.0) * 0.7)
        contrast_score = min(100.0, contrast / 70.0 * 100.0)
        confidence_score = confidence * 100.0
        score = brightness_score * 0.28 + contrast_score * 0.32 + confidence_score * 0.40
        return int(round(max(0.0, min(100.0, score))))

    def _relative_gain(self, original: int, enhanced: int) -> float:
        if original <= 0:
            return 100.0 if enhanced > 0 else 0.0
        return (enhanced - original) / original * 100.0

    def _number_or_dash(self, value: float | None) -> str:
        return "--" if value is None else f"{value:.0f}"

    def _percent(self, value: float) -> str:
        return f"{value * 100:.1f}%"

    def _signed_percent(self, value: float) -> str:
        return f"{value:+.0f}%"

    def _signed_delta(self, value: float) -> str:
        return f"{value:+.1f}%"
