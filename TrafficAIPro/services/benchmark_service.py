"""Benchmark helpers for standard YOLO versus YOLO + SAHI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from ..models.detection import DetectionBox, DetectionMode, SahiSettings
from .detection_service import VehicleDetectionService


@dataclass
class BenchmarkResult:
    mode: DetectionMode
    image_count: int
    vehicle_count: int
    inference_time: float
    fps: float
    precision: float | None = None
    recall: float | None = None
    map50: float | None = None


class DetectionBenchmarkService:
    """Compare standard YOLO and sliced SAHI inference on image samples."""

    def __init__(self, detection_service: VehicleDetectionService) -> None:
        self.detection_service = detection_service

    def compare(
        self,
        image_paths: list[str | Path],
        confidence_threshold: float = 0.25,
        sahi_settings: SahiSettings | None = None,
        ground_truth: dict[str, list[DetectionBox]] | None = None,
    ) -> dict[str, BenchmarkResult]:
        previous_mode = self.detection_service.detection_mode
        previous_sahi = self.detection_service.sahi_settings
        if sahi_settings is not None:
            self.detection_service.sahi_settings = sahi_settings

        try:
            yolo = self._run_mode(
                DetectionMode.YOLO,
                image_paths,
                confidence_threshold,
                ground_truth,
            )
            sahi = self._run_mode(
                DetectionMode.SAHI,
                image_paths,
                confidence_threshold,
                ground_truth,
            )
        finally:
            self.detection_service.set_detection_mode(previous_mode)
            self.detection_service.sahi_settings = previous_sahi

        return {"YOLO": yolo, "SAHI": sahi}

    def _run_mode(
        self,
        mode: DetectionMode,
        image_paths: list[str | Path],
        confidence_threshold: float,
        ground_truth: dict[str, list[DetectionBox]] | None,
    ) -> BenchmarkResult:
        self.detection_service.set_detection_mode(mode)
        summaries = []
        predictions: dict[str, list[DetectionBox]] = {}
        for image_path in image_paths:
            path = Path(image_path)
            image = cv2.imread(str(path))
            if image is None:
                continue
            _, summary = self.detection_service.detect(image, path.name, confidence_threshold)
            summaries.append(summary)
            predictions[path.name] = summary.detections

        inference_time = sum(summary.processing_time for summary in summaries)
        vehicle_count = sum(summary.total for summary in summaries)
        fps = len(summaries) / inference_time if inference_time > 0 else 0.0
        precision = recall = map50 = None
        if ground_truth:
            precision, recall, map50 = self._evaluate(predictions, ground_truth)

        return BenchmarkResult(
            mode=mode,
            image_count=len(summaries),
            vehicle_count=vehicle_count,
            inference_time=inference_time,
            fps=fps,
            precision=precision,
            recall=recall,
            map50=map50,
        )

    def _evaluate(
        self,
        predictions: dict[str, list[DetectionBox]],
        ground_truth: dict[str, list[DetectionBox]],
        iou_threshold: float = 0.5,
    ) -> tuple[float, float, float]:
        true_positive = 0
        false_positive = 0
        false_negative = 0

        for image_name, truth_boxes in ground_truth.items():
            matched_truth: set[int] = set()
            for prediction in predictions.get(image_name, []):
                best_index = -1
                best_iou = 0.0
                for index, truth in enumerate(truth_boxes):
                    if index in matched_truth or truth.label != prediction.label:
                        continue
                    score = self._iou(prediction.bbox, truth.bbox)
                    if score > best_iou:
                        best_iou = score
                        best_index = index
                if best_index >= 0 and best_iou >= iou_threshold:
                    true_positive += 1
                    matched_truth.add(best_index)
                else:
                    false_positive += 1
            false_negative += len(truth_boxes) - len(matched_truth)

        precision = true_positive / max(1, true_positive + false_positive)
        recall = true_positive / max(1, true_positive + false_negative)
        map50 = float(np.mean([precision, recall]))
        return precision, recall, map50

    def _iou(
        self,
        a: tuple[int, int, int, int],
        b: tuple[int, int, int, int],
    ) -> float:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        inter_x1 = max(ax1, bx1)
        inter_y1 = max(ay1, by1)
        inter_x2 = min(ax2, bx2)
        inter_y2 = min(ay2, by2)
        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
        a_area = max(0, ax2 - ax1) * max(0, ay2 - ay1)
        b_area = max(0, bx2 - bx1) * max(0, by2 - by1)
        union = a_area + b_area - inter_area
        return inter_area / union if union > 0 else 0.0
