"""OpenCV image enhancement service."""

from __future__ import annotations

import cv2
import numpy as np


class ImageEnhancementService:
    """Apply traffic-image enhancement operations."""

    def __init__(self) -> None:
        self.motion_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=32,
            detectShadows=True,
        )

    def load(self, path: str) -> np.ndarray:
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Unable to load image: {path}")
        return image

    def enhance(
        self,
        image: np.ndarray,
        use_clahe: bool = True,
        gamma: float = 1.0,
        brightness: int = 0,
        contrast: float = 1.0,
        median_kernel: int = 1,
    ) -> np.ndarray:
        """Apply enhancement pipeline and return BGR image."""
        output = image.copy()
        if use_clahe:
            lab = cv2.cvtColor(output, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(8, 8))
            output = cv2.cvtColor(
                cv2.merge((clahe.apply(l_channel), a_channel, b_channel)),
                cv2.COLOR_LAB2BGR,
            )

        gamma = max(gamma, 0.05)
        table = np.array(
            [((value / 255.0) ** (1.0 / gamma)) * 255 for value in range(256)]
        ).astype("uint8")
        output = cv2.LUT(output, table)
        output = cv2.convertScaleAbs(output, alpha=contrast, beta=brightness)

        if median_kernel > 1:
            kernel = median_kernel if median_kernel % 2 == 1 else median_kernel + 1
            output = cv2.medianBlur(output, kernel)
        return output

    def quality_metrics(self, image: np.ndarray) -> dict[str, float]:
        """Compute histogram-oriented image quality metrics."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        noise = cv2.Laplacian(gray, cv2.CV_64F).std()
        return {
            "brightness": float(np.mean(gray)),
            "contrast": float(np.std(gray)),
            "dynamic_range": float(np.max(gray) - np.min(gray)),
            "noise": float(noise),
        }

    def grayscale_histogram(self, image: np.ndarray) -> np.ndarray:
        """Return a 256-bin grayscale histogram."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        return hist.astype(float)

    def otsu_threshold(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    def adaptive_threshold(self, image: np.ndarray, gaussian: bool = True) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C if gaussian else cv2.ADAPTIVE_THRESH_MEAN_C
        binary = cv2.adaptiveThreshold(gray, 255, method, cv2.THRESH_BINARY, 31, 5)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    def enhanced_adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        enhanced = self.enhance(
            image,
            use_clahe=True,
            gamma=1.1,
            brightness=8,
            contrast=1.2,
            median_kernel=3,
        )
        return self.adaptive_threshold(enhanced, gaussian=True)

    def segmentation_metrics(self, binary_bgr: np.ndarray) -> dict[str, int]:
        gray = cv2.cvtColor(binary_bgr, cv2.COLOR_BGR2GRAY)
        mask = gray > 0
        components, _ = cv2.connectedComponents(mask.astype("uint8"))
        return {
            "area": int(np.count_nonzero(mask)),
            "components": max(0, int(components) - 1),
        }

    def extract_moving_objects(self, frame: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return foreground mask and extracted moving-object image."""
        mask = self.motion_subtractor.apply(frame)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        extracted = cv2.bitwise_and(frame, frame, mask=mask)
        return mask, extracted

    def reset_motion_model(self) -> None:
        self.motion_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=32,
            detectShadows=True,
        )

