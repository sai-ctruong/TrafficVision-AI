<h1 align="center">TrafficVision AI</h1>

<h3 align="center">YOLOv26 Vehicle Detection, Video Tracking & Traffic Analytics Desktop App</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/PyQt6-Desktop_UI-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/OpenCV-Image_Processing-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/Ultralytics-YOLO-111111?style=for-the-badge" alt="Ultralytics YOLO">
  <img src="https://img.shields.io/badge/SQLite-History_DB-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</p>

<p align="center">
  <strong>TrafficVision AI</strong> là hệ thống thị giác máy tính phục vụ nhận diện phương tiện, phân tích mật độ giao thông và trình bày báo cáo trong một ứng dụng desktop hiện đại. Ứng dụng chạy dưới tên <strong>TrafficAI Pro</strong>, kết hợp PyQt6, QFluentWidgets, OpenCV, Ultralytics YOLO, PyQtGraph, SQLite và tích hợp Arduino tùy chọn.
</p>

<p align="center">
  <img src="TrafficAIPro/assets/backgrounds/background_traffic.jpg" alt="TrafficVision AI background" width="880">
</p>

---

## Tổng Quan

TrafficVision AI được xây dựng cho môn **Digital Image Processing** tại **Ho Chi Minh City University of Technology and Engineering (HCMUTE)**, năm học **2025-2026**. Project tập trung vào một pipeline hoàn chỉnh:

```text
Image / Video
    -> Image Enhancement
    -> YOLOv26 Detection / Tracking
    -> Vehicle Classification
    -> Analytics Dashboard
    -> SQLite History / CSV Export
    -> Optional Arduino Traffic Light Signal
```

Ứng dụng nhận diện 4 nhóm phương tiện chính: `car`, `bus`, `truck`, `van`.

## Điểm Nổi Bật

| Module            | Khả năng                                                                                                        |
| ----------------- | --------------------------------------------------------------------------------------------------------------- |
| Dashboard         | Hiển thị tổng số phương tiện, thống kê từng loại xe, model đang chạy, hiệu năng inference và trạng thái Arduino |
| Image Processing  | Upload ảnh, preview ảnh gốc và ảnh đã cải thiện, tinh chỉnh CLAHE, gamma, brightness, contrast và median filter |
| Vehicle Detection | Tự động chạy YOLO trên ảnh đã xử lý, vẽ bounding box, đếm phương tiện và lưu kết quả vào lịch sử                |
| Video Analysis    | Phân tích video, tracking bằng ByteTrack hoặc BoT-SORT, hiển thị Track ID, counting line, FPS và confidence     |
| Analytics         | Biểu đồ phân bố phương tiện, bar chart, so sánh ảnh gốc/ảnh enhance và đánh giá tác động xử lý ảnh              |
| History           | Lưu lịch sử detection bằng SQLite, xem lại ảnh annotated, tìm kiếm, sắp xếp, xóa record và export CSV           |
| Arduino Service   | Gửi payload mật độ giao thông theo dạng `LEVEL,CAR,BUS,TRUCK,VAN,TOTAL` qua serial hoặc chạy mock mode          |

## Giao Diện Chính

Ứng dụng có sidebar điều hướng theo 3 nhóm:

| Nhóm    | Màn hình                                            |
| ------- | --------------------------------------------------- |
| MAIN    | Dashboard                                           |
| DETECT  | Image Processing, Vehicle Detection, Video Analysis |
| REPORTS | Analytics, History, Project Information             |

Ngoài ra repo có sẵn `SegmentationDemoPage` như một module mở rộng cho Otsu thresholding, adaptive thresholding và CLAHE + adaptive thresholding.

## Công Nghệ Sử Dụng

| Công nghệ            | Vai trò                                           |
| -------------------- | ------------------------------------------------- |
| Python               | Ngôn ngữ chính                                    |
| PyQt6                | Xây dựng desktop application                      |
| PyQt6-Fluent-Widgets | Component UI theo phong cách Fluent               |
| OpenCV               | Xử lý ảnh, video, thresholding, motion extraction |
| Ultralytics YOLO     | Detection và tracking phương tiện                 |
| NumPy                | Xử lý dữ liệu ảnh và tính toán metric             |
| Pillow               | Hỗ trợ thao tác ảnh                               |
| PyQtGraph            | Biểu đồ và trực quan hóa dữ liệu                  |
| SQLite               | Lưu detection history                             |
| pyserial             | Kết nối Arduino qua cổng COM                      |

## Cấu Trúc Project

```text
.
├── main.py                         # Launcher chính cho ứng dụng desktop
├── run.bat                         # Script chạy nhanh trên Windows
├── requirements.txt                # Danh sách dependency Python
├── test_video.mp4                  # Video mẫu cho Video Analysis
├── README.md                       # Tài liệu project
├── legacy/                         # Code phiên bản cũ, giữ lại để tham khảo
└── TrafficAIPro/
    ├── main.py                     # Khởi tạo QApplication và main window
    ├── assets/
    │   └── backgrounds/            # Ảnh nền giao diện
    ├── database/
    │   └── detected_images/        # Ảnh kết quả detection được lưu runtime
    ├── models/
    │   ├── detection.py            # DetectionBox, DetectionSummary
    │   └── weights/
    │       └── Car_YOLO26_Best.pt  # Model mặc định
    ├── pages/                      # Các màn hình chính của app
    ├── services/                   # Image, detection, settings, Arduino services
    ├── ui/                         # Main window và điều hướng
    ├── utils/                      # Path helpers, theme, style constants
    └── widgets/                    # Component UI tái sử dụng
```

## Cài Đặt

Yêu cầu khuyến nghị:

- Windows 10/11
- Python 3.10 trở lên
- GPU CUDA nếu muốn inference nhanh hơn, CPU vẫn chạy được
- Model YOLO dạng `.pt`

Tạo môi trường ảo:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Cài dependency:

```powershell
pip install -r requirements.txt
```

## Chuẩn Bị Model

Model mặc định được code trỏ tới:

```text
TrafficAIPro/models/weights/Car_YOLO26_Best.pt
```

Nếu muốn thay model khác, có thể cập nhật giá trị trong `QSettings` thông qua `SettingsService`, hoặc chỉnh đường dẫn mặc định tại:

```text
TrafficAIPro/utils/paths.py
```

Ứng dụng sẽ tự fallback về `DEFAULT_MODEL_PATH` nếu đường dẫn model đã lưu không còn tồn tại.

## Cách Chạy

Chạy từ terminal:

```powershell
python main.py
```

Hoặc dùng script Windows:

```powershell
.\run.bat
```

Khi khởi động, app sẽ:

1. Tạo các thư mục runtime cần thiết.
2. Load theme và cấu hình đã lưu.
3. Khởi tạo YOLO model mặc định.
4. Kết nối Arduino service ở mock mode.
5. Mở cửa sổ **TrafficAI Pro**.

## Workflow Sử Dụng

1. Vào **Image Processing** và upload ảnh giao thông.
2. Tinh chỉnh CLAHE, gamma, brightness, contrast hoặc median filter.
3. Ảnh enhanced sẽ được gửi tự động sang **Vehicle Detection**.
4. YOLO chạy inference, vẽ bounding box và đếm `car`, `bus`, `truck`, `van`.
5. Kết quả được cập nhật lên **Dashboard**, **Analytics** và **History**.
6. Vào **Video Analysis** để mở video, bật tracking, Track ID, counting line và xem thống kê live.
7. Vào **History** để tìm kiếm, xem lại ảnh annotated, xóa record hoặc export CSV.

## Video Analysis

Video page hỗ trợ:

- Mở file `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`
- Chọn tracker `ByteTrack` hoặc `BoT-SORT`
- Điều chỉnh confidence và IoU threshold
- Bật/tắt enhancement trước inference
- Bật/tắt Track ID
- Chọn counting line ngang hoặc dọc
- Theo dõi frame, FPS, thời gian xử lý và confidence trung bình

App mặc định chạy inference mỗi 2 frame để giữ trải nghiệm video mượt hơn.

## Arduino Integration

Arduino service nằm tại:

```text
TrafficAIPro/services/arduino_service.py
```

Cấu hình mặc định trong `TrafficAIPro/ui/main_window.py`:

```python
ARDUINO_MOCK_MODE = True
ARDUINO_PORT = None  # Ví dụ khi dùng thật: "COM3"
```

Payload gửi sang Arduino:

```text
LEVEL,CAR,BUS,TRUCK,VAN,TOTAL
```

Quy tắc mức giao thông:

| Tổng xe   | Level | Đèn    |
| --------- | ----- | ------ |
| `< 10`    | `G`   | Green  |
| `10 - 19` | `Y`   | Yellow |
| `>= 20`   | `R`   | Red    |

## Dữ Liệu Runtime

| Đường dẫn                                         | Ý nghĩa                                   |
| ------------------------------------------------- | ----------------------------------------- |
| `TrafficAIPro/database/trafficai_history.sqlite3` | SQLite database lưu lịch sử detection     |
| `TrafficAIPro/database/detected_images/`          | Ảnh annotated được lưu sau mỗi lần detect |
| `TrafficAIPro/exports/trafficai_history.csv`      | File CSV export từ History                |
| `__pycache__/`                                    | Cache Python sinh tự động                 |

Các file runtime như database, export và cache đã được cấu hình trong `.gitignore`.

## Ghi Chú Phát Triển

- `main.py` ở root là launcher nên ưu tiên chạy file này.
- `TrafficAIPro/main.py` chứa logic khởi tạo `QApplication`.
- `TrafficAIPro/ui/main_window.py` là nơi wire service, sidebar và page stack.
- `TrafficAIPro/services/detection_service.py` xử lý load model, detection ảnh và tracking video.
- `TrafficAIPro/database/history_repository.py` quản lý SQLite và export CSV.
- `legacy/` chỉ dùng để tham khảo, app mới không phụ thuộc vào thư mục này.

---

<p align="center">
  <strong>TrafficVision AI</strong> - Computer Vision for Smarter Traffic Understanding
</p>
