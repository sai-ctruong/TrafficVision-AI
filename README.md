# Smart Traffic Car Counting System

A modern desktop application for traffic car counting using Image Enhancement and YOLO11 detection.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)
![YOLO](https://img.shields.io/badge/YOLO-11-red.svg)

## Features

✨ **Modern UI Design**
- Windows 11 Fluent Design interface
- Clean, professional look with qfluentwidgets
- Real-time image preview with three-panel comparison
- Interactive parameter controls with live feedback

🖼️ **Advanced Image Enhancement**
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Gamma Correction
- Brightness and Contrast adjustment
- Non-local Means Denoising
- Real-time parameter tuning

🚗 **YOLO11 Car Detection**
- State-of-the-art object detection
- Custom trained model support
- Adjustable confidence threshold
- Bounding box visualization
- Accurate car counting

📊 **Statistics & Export**
- Real-time detection statistics
- Processing time tracking
- Export enhanced images
- Export detection results
- Generate detailed reports

## Screenshots

### Main Interface
The application features a three-panel layout showing:
1. Original uploaded image
2. Enhanced image with applied filters
3. Detection result with bounding boxes

### Control Panel
Intuitive sliders for adjusting:
- CLAHE parameters
- Gamma correction
- Brightness/Contrast
- Denoising strength
- Detection confidence

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (recommended for Fluent Design)

### Step 1: Clone or Download
```bash
cd d:\UTE\Digital_Image_Processing\YOLO_PROJECT
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Prepare YOLO Model
Ensure your trained YOLO model is named `best_oto.pt` and placed in the project root directory.

## Usage

### Running the Application
```bash
python main.py
```

### Workflow

1. **Upload Image**
   - Click "Upload Image" button
   - Select a traffic image (PNG, JPG, JPEG, BMP)
   - Image appears in the "Original Image" panel

2. **Adjust Enhancement Parameters**
   - Use the right-side control panel
   - Adjust CLAHE, Gamma, Brightness, Contrast, Denoising
   - Click "Apply Enhancement" to see results

3. **Run Detection**
   - After enhancement, click "Run Detection"
   - YOLO11 processes the enhanced image
   - Results appear in "Detection Result" panel
   - Statistics update automatically

4. **Export Results**
   - Click "Export Result" to save
   - Choose output directory
   - Saves: enhanced image, detection result, and text report

## Project Structure

```
YOLO_PROJECT/
├── main.py                 # Application entry point
├── ui_main.py             # Main window and UI components
├── image_processor.py     # Image enhancement module
├── detector.py            # YOLO detection module
├── requirements.txt       # Python dependencies
├── best_oto.pt           # YOLO11 trained model
└── README.md             # This file
```

## Configuration

### Enhancement Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| CLAHE Clip Limit | 1.0 - 5.0 | 2.0 | Contrast enhancement strength |
| CLAHE Grid Size | 4x4, 8x8, 16x16 | 8x8 | Tile size for local enhancement |
| Gamma | 0.5 - 3.0 | 1.0 | Brightness curve adjustment |
| Brightness | -100 - 100 | 0 | Linear brightness shift |
| Contrast | 0.5 - 2.5 | 1.0 | Contrast multiplier |
| Denoising | 0 - 30 | 0 | Noise reduction strength |
| Confidence | 0.1 - 0.9 | 0.5 | Detection threshold |

## Technical Details

### Image Enhancement Pipeline
1. **CLAHE on LAB Color Space**: Enhances contrast while preserving colors
2. **Gamma Correction**: Adjusts overall brightness non-linearly
3. **Brightness/Contrast**: Fine-tunes image appearance
4. **Denoising**: Reduces noise using Non-local Means algorithm

### YOLO Detection
- Uses Ultralytics YOLO11 framework
- Processes enhanced images for better detection
- Filters detections by confidence threshold
- Counts only "car" class objects
- Draws bounding boxes with confidence scores

## Dependencies

- **PyQt6**: Modern Qt6 bindings for Python
- **qfluentwidgets**: Windows 11 Fluent Design components
- **OpenCV**: Image processing and computer vision
- **Ultralytics**: YOLO11 object detection framework
- **NumPy**: Numerical computing
- **Pillow**: Image file handling

## Troubleshooting

### Model Not Found
**Error**: "Failed to load best_oto.pt"
**Solution**: Ensure `best_oto.pt` is in the project root directory

### Import Errors
**Error**: "No module named 'qfluentwidgets'"
**Solution**: Run `pip install -r requirements.txt`

### Image Not Loading
**Error**: Image appears blank
**Solution**: Ensure image format is supported (PNG, JPG, JPEG, BMP)

### Detection Not Working
**Error**: No cars detected
**Solution**: 
- Try adjusting confidence threshold
- Ensure image enhancement is applied
- Check if model is trained for car detection

## Performance Tips

1. **Image Size**: Larger images take longer to process
2. **Denoising**: High denoising values increase processing time
3. **Confidence**: Lower threshold detects more objects but may include false positives

## Export Format

### Report File (report_YYYYMMDD_HHMMSS.txt)
```
==================================================
Smart Traffic Car Counting System - Report
==================================================

Image: path/to/image.jpg
Date: 2024-01-01 12:00:00

Cars Detected: 15
Processing Time: 1.23s
Image Resolution: 1920 x 1080
Average Confidence: 0.87

Enhancement Parameters:
  CLAHE Clip Limit: 2.0
  CLAHE Grid Size: (8, 8)
  Gamma: 1.0
  Brightness: 0
  Contrast: 1.0
  Denoising: 0
  Confidence Threshold: 0.5
```

## Credits

**Project**: Digital Image Processing - UTE
**Framework**: PyQt6 + qfluentwidgets
**Detection**: Ultralytics YOLO11
**UI Design**: Windows 11 Fluent Design

## License

This project is created for educational purposes as part of a university project.

## Support

For issues or questions, please contact your project supervisor or teaching assistant.

---

**Made with ❤️ for Digital Image Processing Course**
