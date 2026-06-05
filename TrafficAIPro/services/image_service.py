"""OpenCV image enhancement service."""

from __future__ import annotations

import cv2
import numpy as np


class ImageEnhancementService:
    """Apply traffic-image enhancement operations."""

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

