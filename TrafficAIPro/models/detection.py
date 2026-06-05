"""Detection result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


VEHICLE_CLASSES = ("car", "bus", "truck", "van")


@dataclass
class DetectionBox:
    """Single object detection."""

    label: str
    confidence: float
    bbox: tuple[int, int, int, int]


@dataclass
class DetectionSummary:
    """Aggregated detection output."""

    image_name: str = ""
    counts: dict[str, int] = field(default_factory=lambda: {k: 0 for k in VEHICLE_CLASSES})
    average_confidence: float = 0.0
    processing_time: float = 0.0
    detections: list[DetectionBox] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> int:
        """Total vehicle count."""
        return sum(self.counts.values())
