"""Image processing page with modern UI."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtGui import QColor
from qfluentwidgets import BodyLabel, CardWidget, CheckBox, FluentIcon, IconWidget, PrimaryPushButton, PushButton, Slider, StrongBodyLabel, SubtitleLabel

from .base import Page
from ..services.image_service import ImageEnhancementService
from ..widgets.image_viewer import ImageViewer
from ..utils.theme import PRIMARY, SECONDARY_TEXT, SUCCESS


class SliderWithLabel(QWidget):
    """Slider with value label."""
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self, min_val: int, max_val: int, default: int, suffix: str = "") -> None:
        super().__init__()
        self.suffix = suffix
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        # Slider and value in horizontal layout
        slider_row = QHBoxLayout()
        slider_row.setSpacing(12)
        
        self.slider = Slider(Qt.Orientation.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(default)
        self.slider.valueChanged.connect(self._on_value_changed)
        slider_row.addWidget(self.slider, 1)
        
        self.value_label = BodyLabel(f"{default}{suffix}")
        self.value_label.setFixedWidth(50)
        self.value_label.setStyleSheet(
            """
            font-size: 13px;
            font-weight: 700;
            color: #0F6CBD;
            """
        )
        slider_row.addWidget(self.value_label)
        
        layout.addLayout(slider_row)
    
    def _on_value_changed(self, value: int) -> None:
        self.value_label.setText(f"{value}{self.suffix}")
        self.valueChanged.emit(value)
    
    def value(self) -> int:
        return self.slider.value()
    
    def setValue(self, value: int) -> None:
        self.slider.setValue(value)


class ControlCard(CardWidget):
    """Premium control card for image adjustments."""

    def __init__(self, title: str, icon: FluentIcon) -> None:
        super().__init__()
        self.setBorderRadius(14)
        self.setStyleSheet(
            """
            CardWidget {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            """
        )
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(22, 20, 22, 20)
        self.main_layout.setSpacing(16)

        # Header with icon
        header = QHBoxLayout()
        header.setSpacing(12)
        
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(24, 24)
        header.addWidget(icon_widget)
        
        title_label = SubtitleLabel(title)
        title_label.setStyleSheet(
            f"""
            font-size: 16px;
            font-weight: 700;
            color: {PRIMARY};
            """
        )
        header.addWidget(title_label)
        header.addStretch(1)
        
        self.main_layout.addLayout(header)

    def add_control(self, label: str, widget: QWidget) -> None:
        """Add a control widget with label."""
        control_layout = QVBoxLayout()
        control_layout.setSpacing(8)
        
        label_widget = BodyLabel(label)
        label_widget.setStyleSheet(
            f"""
            font-size: 13px;
            font-weight: 600;
            color: #1a1a1a;
            """
        )
        control_layout.addWidget(label_widget)
        control_layout.addWidget(widget)
        
        self.main_layout.addLayout(control_layout)


class ImageProcessingPage(Page):
    """Upload and enhance images with live preview."""

    image_changed = pyqtSignal(object, str)

    def __init__(self, image_service: ImageEnhancementService) -> None:
        super().__init__("Image Processing", "ImageProcessingPage")
        self.image_service = image_service
        self.image_path = ""
        self.original_image: np.ndarray | None = None
        self.enhanced_image: np.ndarray | None = None

        # Action buttons
        actions = QHBoxLayout()
        actions.setSpacing(12)
        
        self.upload_button = PrimaryPushButton("Upload Image")
        self.upload_button.setIcon(FluentIcon.PHOTO)
        self.upload_button.setFixedHeight(44)
        self.upload_button.setMinimumWidth(140)
        self.upload_button.clicked.connect(self.upload_image)
        actions.addWidget(self.upload_button)
        
        self.reset_button = PushButton("Reset to Default")
        self.reset_button.setIcon(FluentIcon.RETURN)
        self.reset_button.setFixedHeight(44)
        self.reset_button.setMinimumWidth(140)
        self.reset_button.clicked.connect(self.reset_controls)
        actions.addWidget(self.reset_button)
        
        self.apply_button = PushButton("Apply & Continue")
        self.apply_button.setIcon(FluentIcon.ACCEPT)
        self.apply_button.setFixedHeight(44)
        self.apply_button.setMinimumWidth(140)
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.apply_and_continue)
        actions.addWidget(self.apply_button)
        
        actions.addStretch(1)
        self.layout.addLayout(actions)
        self.layout.addSpacing(8)

        # Image preview grid
        preview_grid = QGridLayout()
        preview_grid.setSpacing(20)
        self.original_view = ImageViewer("Original Image")
        self.enhanced_view = ImageViewer("Enhanced Preview")
        preview_grid.addWidget(self.original_view, 0, 0)
        preview_grid.addWidget(self.enhanced_view, 0, 1)
        self.layout.addLayout(preview_grid)
        self.layout.addSpacing(8)

        # Control panels - vertical layout for better display
        controls_container = QVBoxLayout()
        controls_container.setSpacing(20)

        # Row 1: Basic and Advanced
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        # Basic adjustments card
        basic_card = ControlCard("Basic Adjustments", FluentIcon.PALETTE)
        
        self.gamma_slider = SliderWithLabel(5, 30, 10, "")
        self.gamma_slider.valueChanged.connect(self.apply_live_preview)
        basic_card.add_control("Gamma Correction", self.gamma_slider)
        
        self.brightness_slider = SliderWithLabel(-60, 60, 0, "")
        self.brightness_slider.valueChanged.connect(self.apply_live_preview)
        basic_card.add_control("Brightness", self.brightness_slider)
        
        self.contrast_slider = SliderWithLabel(5, 25, 10, "")
        self.contrast_slider.valueChanged.connect(self.apply_live_preview)
        basic_card.add_control("Contrast", self.contrast_slider)
        
        row1.addWidget(basic_card)

        # Advanced filters card
        advanced_card = ControlCard("Advanced Filters", FluentIcon.BRUSH)
        
        self.clahe_check = CheckBox("Enable CLAHE Enhancement")
        self.clahe_check.setChecked(True)
        self.clahe_check.stateChanged.connect(self.apply_live_preview)
        self.clahe_check.setStyleSheet(
            """
            CheckBox {
                font-size: 14px;
                font-weight: 600;
                color: #1a1a1a;
                margin: 8px 0px;
                padding-left: 2px;
            }
            """
        )
        advanced_card.main_layout.addWidget(self.clahe_check)
        
        self.median_slider = SliderWithLabel(1, 9, 1, " px")
        self.median_slider.valueChanged.connect(self.apply_live_preview)
        advanced_card.add_control("Median Filter Kernel", self.median_slider)
        
        row1.addWidget(advanced_card)

        # Info card
        info_card = ControlCard("Image Information", FluentIcon.INFO)
        info_card.setMinimumWidth(280)
        
        self.image_info = BodyLabel("No image loaded\n\nUpload an image to start processing.")
        self.image_info.setWordWrap(True)
        self.image_info.setStyleSheet(
            f"""
            font-size: 13px;
            color: {SECONDARY_TEXT};
            line-height: 1.8;
            """
        )
        info_card.main_layout.addWidget(self.image_info)
        
        info_card.main_layout.addSpacing(8)
        
        self.status_label = BodyLabel("● Ready")
        self.status_label.setStyleSheet(
            f"""
            font-size: 13px;
            color: {SUCCESS};
            font-weight: 600;
            """
        )
        info_card.main_layout.addWidget(self.status_label)
        
        row1.addWidget(info_card)

        controls_container.addLayout(row1)

        self.layout.addLayout(controls_container)
        self.layout.addStretch(1)

    def upload_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Traffic Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)",
        )
        if not path:
            return
        
        self.image_path = path
        self.original_image = self.image_service.load(path)
        self.original_view.set_image(self.original_image)
        
        # Update info
        filename = Path(path).name
        height, width = self.original_image.shape[:2]
        self.image_info.setText(
            f"File: {filename}\n"
            f"Size: {width} × {height} px\n"
            f"Channels: {self.original_image.shape[2] if len(self.original_image.shape) > 2 else 1}"
        )
        
        self.apply_button.setEnabled(True)
        self.apply_live_preview()

    def apply_live_preview(self) -> None:
        if self.original_image is None:
            return
        
        self.status_label.setText("● Processing...")
        self.status_label.setStyleSheet("font-size: 13px; color: #F59E0B; font-weight: 600;")
        
        self.enhanced_image = self.image_service.enhance(
            self.original_image,
            use_clahe=self.clahe_check.isChecked(),
            gamma=self.gamma_slider.value() / 10,
            brightness=self.brightness_slider.value(),
            contrast=self.contrast_slider.value() / 10,
            median_kernel=self.median_slider.value(),
        )
        self.enhanced_view.set_image(self.enhanced_image)
        self.image_changed.emit(self.enhanced_image, Path(self.image_path).name)
        
        self.status_label.setText("● Preview Updated")
        self.status_label.setStyleSheet(f"font-size: 13px; color: {SUCCESS}; font-weight: 600;")

    def reset_controls(self) -> None:
        """Reset all controls to default values."""
        self.gamma_slider.setValue(10)
        self.brightness_slider.setValue(0)
        self.contrast_slider.setValue(10)
        self.median_slider.setValue(1)
        self.clahe_check.setChecked(True)
        
        if self.original_image is not None:
            self.apply_live_preview()

    def apply_and_continue(self) -> None:
        """Apply enhancements and switch to detection page."""
        if self.enhanced_image is None:
            return
        
        # Show success message
        from qfluentwidgets import InfoBar, InfoBarPosition
        InfoBar.success(
            title="Success",
            content=f"Image enhanced! Switching to Vehicle Detection...",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        
        # Emit signal with enhanced image
        self.image_changed.emit(self.enhanced_image, Path(self.image_path).name)
        
        # Switch to detection page
        # Find parent window and switch page
        from PyQt6.QtWidgets import QApplication
        main_window = None
        for widget in QApplication.topLevelWidgets():
            if widget.objectName() == '' and hasattr(widget, 'show_page'):
                main_window = widget
                break
        
        if main_window:
            # Small delay to show the success message
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(500, lambda: main_window.show_page("detection"))
