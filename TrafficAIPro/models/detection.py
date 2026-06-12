"""Detection result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


VEHICLE_CLASSES = ("car", "bus", "truck", "van")


class DetectionMode(str, Enum):
    """Supported inference backends."""

    YOLO = "YOLO"
    SAHI = "SAHI"

    @property
    def display_name(self) -> str:
        return "YOLO + SAHI" if self is DetectionMode.SAHI else "YOLO"


@dataclass
class SahiSettings:
    """Runtime settings for sliced inference."""

    slice_width: int = 320
    slice_height: int = 320
    overlap_width_ratio: float = 0.2
    overlap_height_ratio: float = 0.2


@dataclass
class DetectionBox:
    """Single object detection."""

    label: str
    confidence: float
    bbox: tuple[int, int, int, int]

    def as_dict(self) -> dict[str, object]:
        return {
            "class_name": self.label,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "count": 1,
        }


@dataclass
class DetectionSummary:
    """Aggregated detection output."""

    image_name: str = ""
    counts: dict[str, int] = field(default_factory=lambda: {k: 0 for k in VEHICLE_CLASSES})
    average_confidence: float = 0.0
    processing_time: float = 0.0
    detections: list[DetectionBox] = field(default_factory=list)
    detection_mode: DetectionMode = DetectionMode.YOLO
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> int:
        """Total vehicle count."""
        return sum(self.counts.values())

    @property
    def fps(self) -> float:
        """Frames-per-second equivalent for the inference call."""
        return 1.0 / self.processing_time if self.processing_time > 0 else 0.0
