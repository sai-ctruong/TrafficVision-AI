"""
YOLO Detection Module
Handles YOLO11 model loading and car detection
"""

import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple, List, Dict, Optional
import time


class CarDetector:
    """YOLO-based car detector"""
    
    def __init__(self, model_path: str = "best_oto.pt"):
        self.model_path = model_path
        self.model = None
        self.last_results = None
        self.processing_time = 0
        
    def load_model(self) -> bool:
        """Load YOLO model from file"""
        try:
            self.model = YOLO(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def detect_cars(self, image: np.ndarray, 
                   confidence_threshold: float = 0.5) -> Tuple[np.ndarray, int, float]:
        """
        Run YOLO detection on image
        Returns: (annotated_image, car_count, avg_confidence)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        start_time = time.time()
        
        try:
            # Run inference
            results = self.model(image, conf=confidence_threshold, verbose=False)
            self.last_results = results
            
            # Get the first result (single image)
            result = results[0]
            
            # Count cars and calculate average confidence
            car_count = 0
            confidences = []
            
            # Filter for car detections
            if result.boxes is not None:
                for box in result.boxes:
                    # Get class name
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id].lower()
                    
                    # Count only cars
                    if 'car' in class_name or 'vehicle' in class_name or class_id == 2:
                        car_count += 1
                        confidences.append(float(box.conf[0]))
            
            # Calculate average confidence
            avg_confidence = np.mean(confidences) if confidences else 0.0
            
            # Draw bounding boxes on image
            annotated_image = result.plot()
            
            # Calculate processing time
            self.processing_time = time.time() - start_time
            
            return annotated_image, car_count, avg_confidence
            
        except Exception as e:
            print(f"Error during detection: {e}")
            self.processing_time = time.time() - start_time
            return image, 0, 0.0
    
    def get_detection_details(self) -> List[Dict]:
        """Get detailed information about each detection"""
        if self.last_results is None:
            return []
        
        details = []
        result = self.last_results[0]
        
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                confidence = float(box.conf[0])
                bbox = box.xyxy[0].cpu().numpy()
                
                details.append({
                    'class': class_name,
                    'confidence': confidence,
                    'bbox': bbox.tolist()
                })
        
        return details
    
    def draw_custom_boxes(self, image: np.ndarray, 
                         confidence_threshold: float = 0.5,
                         box_color: Tuple[int, int, int] = (0, 255, 0),
                         text_color: Tuple[int, int, int] = (255, 255, 255)) -> Tuple[np.ndarray, int]:
        """
        Draw custom styled bounding boxes
        Returns: (annotated_image, car_count)
        """
        if self.last_results is None:
            return image, 0
        
        annotated = image.copy()
        result = self.last_results[0]
        car_count = 0
        
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id].lower()
                confidence = float(box.conf[0])
                
                # Filter for cars only
                if 'car' in class_name or 'vehicle' in class_name or class_id == 2:
                    if confidence >= confidence_threshold:
                        car_count += 1
                        
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                        
                        # Draw rectangle
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, 2)
                        
                        # Draw label background
                        label = f"Car {confidence:.2f}"
                        (label_w, label_h), _ = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                        )
                        cv2.rectangle(annotated, (x1, y1 - label_h - 10), 
                                    (x1 + label_w, y1), box_color, -1)
                        
                        # Draw label text
                        cv2.putText(annotated, label, (x1, y1 - 5),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        
        return annotated, car_count
