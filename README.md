# TrafficAI Pro

Smart Traffic Vehicle Detection & Analytics System built with Python, PyQt6, qfluentwidgets, OpenCV, Ultralytics YOLO and SQLite.

## Highlights

- Windows 11 Fluent-style desktop shell with sidebar navigation.
- Dashboard summary cards for total vehicles, cars, buses, trucks and vans.
- Image enhancement workspace with CLAHE, gamma, brightness, contrast and median filter controls.
- YOLO model loading and detection result preview with confidence labels.
- PyQtGraph analytics dashboard with distribution, count, confidence and timing charts.
- SQLite history with search, sorting, delete and CSV export.
- Settings for light/dark theme, model path and default confidence threshold.

## Project Structure

```text
TrafficAIPro/
├── ui/
├── pages/
├── widgets/
├── models/
├── services/
├── database/
├── resources/
├── assets/
├── utils/
└── main.py
```

## Run

```powershell
pip install -r requirements.txt
python main.py
```

Place `best_oto.pt` in the project root or select a model in Settings.

## Notes

The previous single-window files are kept in the repository for reference. The production-style app entry point is now `TrafficAIPro/main.py`, launched through root `main.py`.
