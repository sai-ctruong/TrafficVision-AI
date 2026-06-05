"""
Main UI Module using PyQt6 and qfluentwidgets
Modern Windows 11 Fluent Design Interface
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFileDialog, QGridLayout, QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QImage, QFont, QPalette, QColor
from qfluentwidgets import (PrimaryPushButton, PushButton, Slider, ComboBox,
                           CardWidget, TitleLabel, SubtitleLabel, BodyLabel,
                           StrongBodyLabel, FluentIcon, InfoBar, InfoBarPosition,
                           ProgressRing, setTheme, Theme, isDarkTheme, ScrollArea)
import cv2
import numpy as np
from typing import Optional
import time
from datetime import datetime


class ImageLabel(QLabel):
    """Custom QLabel for displaying images with proper scaling"""
    
    def __init__(self, text="No Image", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #F8F8F8;
                border: 2px dashed #CCCCCC;
                border-radius: 8px;
                color: #999999;
                font-size: 13px;
                padding: 10px;
            }
        """)
        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setScaledContents(False)
        self._pixmap = None
    
    def setImageFromArray(self, image_array: np.ndarray):
        """Convert numpy array to QPixmap and display"""
        if image_array is None:
            return
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        
        # Create QImage
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self._pixmap = QPixmap.fromImage(q_image)
        
        # Scale to fit label while maintaining aspect ratio
        scaled_pixmap = self._pixmap.scaled(
            self.size(), 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
        self.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;
                border: 1px solid #DDDDDD;
                border-radius: 8px;
                padding: 8px;
            }
        """)
    
    def resizeEvent(self, event):
        """Handle resize events to rescale image"""
        super().resizeEvent(event)
        if self._pixmap:
            scaled_pixmap = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)


class StatCard(CardWidget):
    """Modern statistics card with Fluent Design"""
    
    def __init__(self, title: str, value: str = "0", icon: FluentIcon = None, parent=None):
        super().__init__(parent)
        self.setFixedHeight(95)
        
        self.setStyleSheet("""
            CardWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #DDDDDD;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(6)
        
        # Title
        self.title_label = BodyLabel(title)
        self.title_label.setStyleSheet("color: #666666; font-size: 12px;")
        
        # Value
        self.value_label = TitleLabel(value)
        self.value_label.setStyleSheet("color: #0078D4; font-weight: bold; font-size: 20px;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
    
    def setValue(self, value: str):
        """Update card value"""
        self.value_label.setText(value)


class PipelineIndicator(CardWidget):
    """Visual pipeline progress indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(75)
        
        self.setStyleSheet("""
            CardWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #DDDDDD;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(12)
        
        self.steps = [
            "Upload Image",
            "Enhance Image",
            "YOLO Detection",
            "Count Cars"
        ]
        
        self.step_labels = []
        self.arrows = []
        
        for i, step in enumerate(self.steps):
            # Step label
            label = BodyLabel(step)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                color: #999999; 
                padding: 6px 12px;
                border-radius: 6px;
                background-color: #F5F5F5;
                font-size: 12px;
            """)
            self.step_labels.append(label)
            layout.addWidget(label)
            
            # Arrow (except for last step)
            if i < len(self.steps) - 1:
                arrow = BodyLabel("→")
                arrow.setStyleSheet("color: #CCCCCC; font-size: 20px;")
                self.arrows.append(arrow)
                layout.addWidget(arrow)
    
    def setActiveStep(self, step_index: int):
        """Highlight active step"""
        for i, label in enumerate(self.step_labels):
            if i <= step_index:
                label.setStyleSheet("""
                    color: white; 
                    font-weight: bold;
                    background-color: #0078D4;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                """)
            else:
                label.setStyleSheet("""
                    color: #999999; 
                    padding: 6px 12px;
                    border-radius: 6px;
                    background-color: #F5F5F5;
                    font-size: 12px;
                """)
        
        # Update arrows
        for i, arrow in enumerate(self.arrows):
            if i < step_index:
                arrow.setStyleSheet("color: #0078D4; font-size: 20px;")
            else:
                arrow.setStyleSheet("color: #CCCCCC; font-size: 20px;")


class ControlPanel(CardWidget):
    """Right-side control panel for image enhancement parameters"""
    
    # Signals
    enhancementChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(320)
        
        self.setStyleSheet("""
            CardWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #DDDDDD;
            }
        """)
        
        # Create scroll area for controls
        scroll = ScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = SubtitleLabel("Image Enhancement")
        title.setStyleSheet("font-size: 15px; font-weight: bold; color: #333333;")
        layout.addWidget(title)
        
        # Add separator
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #DDDDDD;")
        layout.addWidget(separator)
        
        # CLAHE Clip Limit
        clahe_label = BodyLabel("CLAHE Clip Limit")
        clahe_label.setStyleSheet("color: #555555; font-size: 12px;")
        layout.addWidget(clahe_label)
        
        clahe_layout = QHBoxLayout()
        self.clahe_slider = Slider(Qt.Orientation.Horizontal)
        self.clahe_slider.setRange(10, 50)  # 1.0 to 5.0 (x10)
        self.clahe_slider.setValue(20)  # Default 2.0
        self.clahe_value = BodyLabel("2.0")
        self.clahe_value.setStyleSheet("color: #0078D4; font-weight: bold; min-width: 35px;")
        self.clahe_slider.valueChanged.connect(
            lambda v: self.clahe_value.setText(f"{v/10:.1f}")
        )
        clahe_layout.addWidget(self.clahe_slider)
        clahe_layout.addWidget(self.clahe_value)
        layout.addLayout(clahe_layout)
        
        # CLAHE Tile Grid Size
        grid_label = BodyLabel("CLAHE Tile Grid Size")
        grid_label.setStyleSheet("color: #555555; font-size: 12px;")
        layout.addWidget(grid_label)
        self.grid_combo = ComboBox()
        self.grid_combo.addItems(["4x4", "8x8", "16x16"])
        self.grid_combo.setCurrentIndex(1)  # Default 8x8
        layout.addWidget(self.grid_combo)
        
        # Gamma
        gamma_label = BodyLabel("Gamma Correction")
        gamma_label.setStyleSheet("color: #555555; font-size: 12px;")
        layout.addWidget(gamma_label)
        
        gamma_layout = QHBoxLayout()
        self.gamma_slider = Slider(Qt.Orientation.Horizontal)
        self.gamma_slider.setRange(5, 30)  # 0.5 to 3.0 (x10)
        self.gamma_slider.setValue(10)  # Default 1.0
        self.gamma_value = BodyLabel("1.0")
        self.gamma_value.setStyleSheet("color: #0078D4; font-weight: bold; min-width: 35px;")
        self.gamma_slider.valueChanged.connect(
            lambda v: self.gamma_value.setText(f"{v/10:.1f}")
        )
        gamma_layout.addWidget(self.gamma_slider)
        gamma_layout.addWidget(self.gamma_value)
        layout.addLayout(gamma_layout)
        
        # Brightness
        brightness_label = BodyLabel("Brightness")
        brightness_label.setStyleSheet("color: #555555; font-size: 12px;")
        layout.addWidget(brightness_label)
        
        brightness_layout = QHBoxLayout()
        self.brightness_slider = Slider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_value = BodyLabel("0")
        self.brightness_value.setStyleSheet("color: #0078D4; font-weight: bold; min-width: 35px;")
        self.brightness_slider.valueChanged.connect(
            lambda v: self.brightness_value.setText(str(v))
        )
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_value)
        layout.addLayout(brightness_layout)
        
        # Contrast
        contrast_label = BodyLabel("Contrast")
        contrast_label.setStyleSheet("color: #555555; font-size: 12px;")
        layout.addWidget(contrast_label)
        
        contrast_layout = QHBoxLayout()
        self.contrast_slider = Slider(Qt.Orientation.Horizontal)
        self.contrast_slider.setRange(5, 25)  # 0.5 to 2.5 (x10)
        self.contrast_slider.setValue(10)  # Default 1.0
        self.contrast_value = BodyLabel("1.0")
        self.contrast_value.setStyleSheet("color: #0078D4; font-weight: bold; min-width: 35px;")
        self.contrast_slider.valueChanged.connect(
            lambda v: self.contrast_value.setText(f"{v/10:.1f}")
        )
        contrast_layout.addWidget(self.contrast_slider)
        contrast_layout.addWidget(self.contrast_value)
        layout.addLayout(contrast_layout)
        
        # Denoising
        denoise_label = BodyLabel("Denoising Strength")
        denoise_label.setStyleSheet("color: #555555; font-size: 12px;")
        layout.addWidget(denoise_label)
        
        denoise_layout = QHBoxLayout()
        self.denoise_slider = Slider(Qt.Orientation.Horizontal)
        self.denoise_slider.setRange(0, 30)
        self.denoise_slider.setValue(0)
        self.denoise_value = BodyLabel("0")
        self.denoise_value.setStyleSheet("color: #0078D4; font-weight: bold; min-width: 35px;")
        self.denoise_slider.valueChanged.connect(
            lambda v: self.denoise_value.setText(str(v))
        )
        denoise_layout.addWidget(self.denoise_slider)
        denoise_layout.addWidget(self.denoise_value)
        layout.addLayout(denoise_layout)
        
        # Confidence Threshold
        confidence_label = BodyLabel("Confidence Threshold")
        confidence_label.setStyleSheet("color: #555555; font-size: 12px;")
        layout.addWidget(confidence_label)
        
        confidence_layout = QHBoxLayout()
        self.confidence_slider = Slider(Qt.Orientation.Horizontal)
        self.confidence_slider.setRange(1, 9)  # 0.1 to 0.9 (x10)
        self.confidence_slider.setValue(5)  # Default 0.5
        self.confidence_value = BodyLabel("0.5")
        self.confidence_value.setStyleSheet("color: #0078D4; font-weight: bold; min-width: 35px;")
        self.confidence_slider.valueChanged.connect(
            lambda v: self.confidence_value.setText(f"{v/10:.1f}")
        )
        confidence_layout.addWidget(self.confidence_slider)
        confidence_layout.addWidget(self.confidence_value)
        layout.addLayout(confidence_layout)
        
        layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def get_parameters(self) -> dict:
        """Get all enhancement parameters"""
        grid_map = {"4x4": (4, 4), "8x8": (8, 8), "16x16": (16, 16)}
        
        return {
            'clahe_clip': self.clahe_slider.value() / 10.0,
            'clahe_grid': grid_map[self.grid_combo.currentText()],
            'gamma': self.gamma_slider.value() / 10.0,
            'brightness': self.brightness_slider.value(),
            'contrast': self.contrast_slider.value() / 10.0,
            'denoise_strength': self.denoise_slider.value(),
            'confidence': self.confidence_slider.value() / 10.0
        }
    
    def reset_parameters(self):
        """Reset all parameters to default"""
        self.clahe_slider.setValue(20)
        self.grid_combo.setCurrentIndex(1)
        self.gamma_slider.setValue(10)
        self.brightness_slider.setValue(0)
        self.contrast_slider.setValue(10)
        self.denoise_slider.setValue(0)
        self.confidence_slider.setValue(5)



class MainWindow(QMainWindow):
    """Main application window with Fluent Design"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Traffic Car Counting System")
        self.resize(1600, 900)
        
        # Import modules
        from image_processor import ImageProcessor
        from detector import CarDetector
        
        # Initialize processors
        self.image_processor = ImageProcessor()
        self.detector = CarDetector("best_oto.pt")
        
        # State variables
        self.current_image = None
        self.enhanced_image = None
        self.detection_image = None
        self.image_path = None
        
        # Setup UI
        self.setup_ui()
        
        # Load YOLO model
        self.load_model()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(18)
        
        # Header section
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Content section (images + control panel)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)
        
        # Left side: Images
        images_layout = self.create_images_section()
        content_layout.addLayout(images_layout, stretch=3)
        
        # Right side: Control panel
        self.control_panel = ControlPanel()
        content_layout.addWidget(self.control_panel, stretch=1)
        
        main_layout.addLayout(content_layout, stretch=1)
        
        # Pipeline indicator
        self.pipeline = PipelineIndicator()
        main_layout.addWidget(self.pipeline)
        
        # Statistics section
        stats_layout = self.create_stats_section()
        main_layout.addLayout(stats_layout)
        
        # Set light theme
        setTheme(Theme.LIGHT)
        self.setStyleSheet("QMainWindow { background-color: #F0F0F0; }")
    
    def create_header(self) -> QVBoxLayout:
        """Create header with title and action buttons"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Title
        title = TitleLabel("Smart Traffic Car Counting System")
        title.setStyleSheet("color: #0078D4; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = SubtitleLabel("Image Enhancement + YOLO11 Detection")
        subtitle.setStyleSheet("color: #666666; font-size: 14px;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(8)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.upload_btn = PrimaryPushButton("Upload Image")
        self.upload_btn.setIcon(FluentIcon.FOLDER_ADD)
        self.upload_btn.setFixedHeight(36)
        self.upload_btn.clicked.connect(self.upload_image)
        
        self.enhance_btn = PushButton("Apply Enhancement")
        self.enhance_btn.setIcon(FluentIcon.EDIT)
        self.enhance_btn.setFixedHeight(36)
        self.enhance_btn.clicked.connect(self.apply_enhancement)
        self.enhance_btn.setEnabled(False)
        
        self.detect_btn = PushButton("Run Detection")
        self.detect_btn.setIcon(FluentIcon.SEARCH)
        self.detect_btn.setFixedHeight(36)
        self.detect_btn.clicked.connect(self.run_detection)
        self.detect_btn.setEnabled(False)
        
        self.export_btn = PushButton("Export Result")
        self.export_btn.setIcon(FluentIcon.SAVE)
        self.export_btn.setFixedHeight(36)
        self.export_btn.clicked.connect(self.export_result)
        self.export_btn.setEnabled(False)
        
        self.reset_btn = PushButton("Reset")
        self.reset_btn.setIcon(FluentIcon.SYNC)
        self.reset_btn.setFixedHeight(36)
        self.reset_btn.clicked.connect(self.reset_image)
        self.reset_btn.setEnabled(False)
        
        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.enhance_btn)
        button_layout.addWidget(self.detect_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        return layout
    
    def create_images_section(self) -> QVBoxLayout:
        """Create three-image comparison section"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Image cards in horizontal layout
        images_layout = QHBoxLayout()
        images_layout.setSpacing(15)
        
        # Original Image Card
        original_card = CardWidget()
        original_card.setStyleSheet("""
            CardWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #DDDDDD;
            }
        """)
        original_layout = QVBoxLayout(original_card)
        original_layout.setContentsMargins(15, 15, 15, 15)
        original_layout.setSpacing(10)
        original_title = StrongBodyLabel("Original Image")
        original_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        original_title.setStyleSheet("font-size: 13px; color: #555555;")
        self.original_label = ImageLabel("No Image Loaded")
        original_layout.addWidget(original_title)
        original_layout.addWidget(self.original_label)
        images_layout.addWidget(original_card)
        
        # Enhanced Image Card
        enhanced_card = CardWidget()
        enhanced_card.setStyleSheet("""
            CardWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #DDDDDD;
            }
        """)
        enhanced_layout = QVBoxLayout(enhanced_card)
        enhanced_layout.setContentsMargins(15, 15, 15, 15)
        enhanced_layout.setSpacing(10)
        enhanced_title = StrongBodyLabel("Enhanced Image")
        enhanced_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        enhanced_title.setStyleSheet("font-size: 13px; color: #555555;")
        self.enhanced_label = ImageLabel("No Enhancement Applied")
        enhanced_layout.addWidget(enhanced_title)
        enhanced_layout.addWidget(self.enhanced_label)
        images_layout.addWidget(enhanced_card)
        
        # Detection Result Card
        detection_card = CardWidget()
        detection_card.setStyleSheet("""
            CardWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #DDDDDD;
            }
        """)
        detection_layout = QVBoxLayout(detection_card)
        detection_layout.setContentsMargins(15, 15, 15, 15)
        detection_layout.setSpacing(10)
        detection_title = StrongBodyLabel("Detection Result")
        detection_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detection_title.setStyleSheet("font-size: 13px; color: #555555;")
        self.detection_label = ImageLabel("No Detection Run")
        detection_layout.addWidget(detection_title)
        detection_layout.addWidget(self.detection_label)
        images_layout.addWidget(detection_card)
        
        layout.addLayout(images_layout)
        
        return layout
    
    def create_stats_section(self) -> QHBoxLayout:
        """Create statistics cards section"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        self.cars_card = StatCard("Cars Detected", "0")
        self.time_card = StatCard("Processing Time", "0.00s")
        self.resolution_card = StatCard("Image Resolution", "0 x 0")
        self.confidence_card = StatCard("Avg Confidence", "0.00")
        
        layout.addWidget(self.cars_card)
        layout.addWidget(self.time_card)
        layout.addWidget(self.resolution_card)
        layout.addWidget(self.confidence_card)
        
        return layout
    
    def load_model(self):
        """Load YOLO model"""
        success = self.detector.load_model()
        if not success:
            InfoBar.error(
                title="Model Error",
                content="Failed to load best_oto.pt. Please ensure the model file exists.",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self
            )
    
    def upload_image(self):
        """Upload and display image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Traffic Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.image_path = file_path
            image = self.image_processor.load_image(file_path)
            
            if image is not None:
                self.current_image = image
                self.original_label.setImageFromArray(image)
                
                # Update resolution
                h, w = image.shape[:2]
                self.resolution_card.setValue(f"{w} x {h}")
                
                # Enable buttons
                self.enhance_btn.setEnabled(True)
                self.reset_btn.setEnabled(True)
                
                # Update pipeline
                self.pipeline.setActiveStep(0)
                
                # Reset other displays
                self.enhanced_label.setText("Click 'Apply Enhancement'")
                self.detection_label.setText("Click 'Run Detection'")
                self.enhanced_image = None
                self.detection_image = None
                
                InfoBar.success(
                    title="Success",
                    content="Image loaded successfully!",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
    
    def apply_enhancement(self):
        """Apply image enhancement"""
        if self.current_image is None:
            return
        
        params = self.control_panel.get_parameters()
        
        # Show processing message
        InfoBar.info(
            title="Processing",
            content="Applying image enhancement...",
            orient=Qt.Orientation.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
        
        # Apply enhancement
        self.enhanced_image = self.image_processor.enhance_image(
            self.current_image,
            clahe_clip=params['clahe_clip'],
            clahe_grid=params['clahe_grid'],
            gamma=params['gamma'],
            brightness=params['brightness'],
            contrast=params['contrast'],
            denoise_strength=params['denoise_strength']
        )
        
        # Display enhanced image
        self.enhanced_label.setImageFromArray(self.enhanced_image)
        
        # Enable detection button
        self.detect_btn.setEnabled(True)
        
        # Update pipeline
        self.pipeline.setActiveStep(1)
        
        InfoBar.success(
            title="Success",
            content="Enhancement applied successfully!",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    def run_detection(self):
        """Run YOLO detection"""
        if self.enhanced_image is None:
            InfoBar.warning(
                title="Warning",
                content="Please apply enhancement first!",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return
        
        params = self.control_panel.get_parameters()
        
        # Show processing message
        InfoBar.info(
            title="Processing",
            content="Running YOLO11 detection...",
            orient=Qt.Orientation.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
        
        # Run detection
        self.detection_image, car_count, avg_confidence = self.detector.detect_cars(
            self.enhanced_image,
            confidence_threshold=params['confidence']
        )
        
        # Display detection result
        self.detection_label.setImageFromArray(self.detection_image)
        
        # Update statistics
        self.cars_card.setValue(str(car_count))
        self.time_card.setValue(f"{self.detector.processing_time:.2f}s")
        self.confidence_card.setValue(f"{avg_confidence:.2f}")
        
        # Enable export button
        self.export_btn.setEnabled(True)
        
        # Update pipeline
        self.pipeline.setActiveStep(3)
        
        InfoBar.success(
            title="Detection Complete",
            content=f"Found {car_count} cars in the image!",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
    
    def reset_image(self):
        """Reset to original image"""
        if self.current_image is not None:
            self.control_panel.reset_parameters()
            self.enhanced_label.setText("Click 'Apply Enhancement'")
            self.detection_label.setText("Click 'Run Detection'")
            self.enhanced_image = None
            self.detection_image = None
            self.detect_btn.setEnabled(False)
            self.export_btn.setEnabled(False)
            self.pipeline.setActiveStep(0)
            
            InfoBar.info(
                title="Reset",
                content="Image reset to original state",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
    
    def export_result(self):
        """Export detection results"""
        if self.detection_image is None:
            return
        
        # Get save directory
        save_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Export Directory",
            ""
        )
        
        if save_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save enhanced image
            enhanced_path = f"{save_dir}/enhanced_{timestamp}.jpg"
            self.image_processor.save_image(self.enhanced_image, enhanced_path)
            
            # Save detection result
            detection_path = f"{save_dir}/detection_{timestamp}.jpg"
            self.image_processor.save_image(self.detection_image, detection_path)
            
            # Save report
            report_path = f"{save_dir}/report_{timestamp}.txt"
            params = self.control_panel.get_parameters()
            
            with open(report_path, 'w') as f:
                f.write("=" * 50 + "\n")
                f.write("Smart Traffic Car Counting System - Report\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Image: {self.image_path}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Cars Detected: {self.cars_card.value_label.text()}\n")
                f.write(f"Processing Time: {self.time_card.value_label.text()}\n")
                f.write(f"Image Resolution: {self.resolution_card.value_label.text()}\n")
                f.write(f"Average Confidence: {self.confidence_card.value_label.text()}\n\n")
                f.write("Enhancement Parameters:\n")
                f.write(f"  CLAHE Clip Limit: {params['clahe_clip']}\n")
                f.write(f"  CLAHE Grid Size: {params['clahe_grid']}\n")
                f.write(f"  Gamma: {params['gamma']}\n")
                f.write(f"  Brightness: {params['brightness']}\n")
                f.write(f"  Contrast: {params['contrast']}\n")
                f.write(f"  Denoising: {params['denoise_strength']}\n")
                f.write(f"  Confidence Threshold: {params['confidence']}\n")
            
            InfoBar.success(
                title="Export Complete",
                content=f"Results saved to {save_dir}",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
