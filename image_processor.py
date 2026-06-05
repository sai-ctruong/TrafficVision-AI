"""
Image Enhancement Module
Handles CLAHE, Gamma Correction, Brightness/Contrast, and Denoising
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class ImageProcessor:
    """Process and enhance images for better YOLO detection"""
    
    def __init__(self):
        self.original_image = None
        self.enhanced_image = None
        
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """Load image from file path"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image: {image_path}")
            self.original_image = image.copy()
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def apply_clahe(self, image: np.ndarray, clip_limit: float = 2.0, 
                    tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """
        Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        Works on LAB color space to preserve color information
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        l_clahe = clahe.apply(l)
        
        # Merge channels and convert back to BGR
        lab_clahe = cv2.merge([l_clahe, a, b])
        enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def apply_gamma_correction(self, image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
        """
        Apply gamma correction to adjust image brightness
        gamma < 1: brighter, gamma > 1: darker
        """
        # Build lookup table
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 
                         for i in range(256)]).astype("uint8")
        
        # Apply gamma correction using lookup table
        return cv2.LUT(image, table)
    
    def adjust_brightness_contrast(self, image: np.ndarray, 
                                   brightness: int = 0, 
                                   contrast: float = 1.0) -> np.ndarray:
        """
        Adjust brightness and contrast
        brightness: -100 to 100
        contrast: 0.5 to 2.5
        """
        # Apply contrast and brightness
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        return adjusted
    
    def apply_denoising(self, image: np.ndarray, strength: int = 10) -> np.ndarray:
        """
        Apply Non-local Means Denoising
        strength: 0 to 30 (higher = more denoising)
        """
        if strength == 0:
            return image
        
        # Apply fastNlMeansDenoisingColored for color images
        denoised = cv2.fastNlMeansDenoisingColored(
            image, None, h=strength, hColor=strength, 
            templateWindowSize=7, searchWindowSize=21
        )
        return denoised
    
    def enhance_image(self, image: np.ndarray,
                     clahe_clip: float = 2.0,
                     clahe_grid: Tuple[int, int] = (8, 8),
                     gamma: float = 1.0,
                     brightness: int = 0,
                     contrast: float = 1.0,
                     denoise_strength: int = 0) -> np.ndarray:
        """
        Apply full enhancement pipeline
        """
        try:
            # Step 1: CLAHE
            enhanced = self.apply_clahe(image, clahe_clip, clahe_grid)
            
            # Step 2: Gamma correction
            enhanced = self.apply_gamma_correction(enhanced, gamma)
            
            # Step 3: Brightness and contrast
            enhanced = self.adjust_brightness_contrast(enhanced, brightness, contrast)
            
            # Step 4: Denoising (optional)
            if denoise_strength > 0:
                enhanced = self.apply_denoising(enhanced, denoise_strength)
            
            self.enhanced_image = enhanced
            return enhanced
            
        except Exception as e:
            print(f"Error during enhancement: {e}")
            return image
    
    def reset_to_original(self) -> Optional[np.ndarray]:
        """Reset to original image"""
        if self.original_image is not None:
            return self.original_image.copy()
        return None
    
    def save_image(self, image: np.ndarray, output_path: str) -> bool:
        """Save image to file"""
        try:
            cv2.imwrite(output_path, image)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
