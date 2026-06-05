# TrafficAI Pro

TrafficAI Pro là ứng dụng desktop hỗ trợ xử lý ảnh, nhận diện phương tiện giao thông bằng YOLO và theo dõi thống kê lịch sử phát hiện. Giao diện được xây dựng bằng Python, PyQt6, QFluentWidgets, OpenCV, Ultralytics YOLO và SQLite.

## Tính năng chính

- Dashboard tổng quan số lượng phương tiện: tổng xe, ô tô, xe buýt, xe tải và xe van.
- Xử lý ảnh đầu vào với CLAHE, gamma, brightness, contrast và median filter.
- Nhận diện phương tiện bằng model YOLO `.pt`.
- Hiển thị ảnh gốc, ảnh đã cải thiện và ảnh kết quả detection.
- Lưu lịch sử phát hiện vào SQLite.
- Thống kê bằng biểu đồ PyQtGraph.
- Tìm kiếm, sắp xếp, xoá lịch sử và xuất CSV.
- Cấu hình theme, đường dẫn model và ngưỡng confidence.
- Background dashboard dùng ảnh giao thông mờ trong `assets/backgrounds`.

## Công nghệ sử dụng

| Thành phần | Mục đích |
| --- | --- |
| Python | Ngôn ngữ chính của project |
| PyQt6 | Xây dựng giao diện desktop |
| QFluentWidgets | Component giao diện phong cách Fluent UI |
| OpenCV | Xử lý ảnh |
| Ultralytics YOLO | Nhận diện phương tiện |
| PyQtGraph | Vẽ biểu đồ thống kê |
| SQLite | Lưu lịch sử phát hiện |

## Cấu trúc thư mục

```text
.
├── main.py                     # Entry point chính, dùng để chạy app
├── run.bat                     # File chạy nhanh trên Windows
├── requirements.txt            # Danh sách thư viện cần cài
├── INSTALL.md                  # Ghi chú cài đặt
├── START_HERE.md               # Hướng dẫn bắt đầu nhanh
├── README.md                   # Tài liệu tổng quan project
├── legacy/                     # Code phiên bản cũ, giữ lại để tham khảo
│   ├── config.py
│   ├── detector.py
│   ├── image_processor.py
│   ├── test_modules.py
│   └── ui_main.py
└── TrafficAIPro/
    ├── main.py                 # Entry point nội bộ của app
    ├── assets/
    │   └── backgrounds/        # Ảnh nền giao diện
    ├── database/               # SQLite database runtime
    ├── exports/                # File export CSV
    ├── models/
    │   ├── detection.py        # Dataclass/model dữ liệu detection
    │   └── weights/            # File model YOLO .pt
    ├── pages/                  # Các màn hình chính
    │   ├── dashboard.py
    │   ├── image_processing.py
    │   ├── detection.py
    │   ├── analytics.py
    │   ├── history.py
    │   └── settings.py
    ├── services/               # Logic xử lý ảnh, detection, settings
    ├── ui/                     # Main window và navigation
    ├── utils/                  # Đường dẫn, theme, helper dùng chung
    └── widgets/                # Component giao diện tái sử dụng
```

## Cài đặt

Yêu cầu khuyến nghị:

- Windows 10/11
- Python 3.9 trở lên
- Model YOLO dạng `.pt`

Cài thư viện:

```powershell
pip install -r requirements.txt
```

## Chuẩn bị model

Đặt file model YOLO tại:

```text
TrafficAIPro/models/weights/best_oto.pt
```

Nếu muốn dùng model khác, mở app rồi chọn lại đường dẫn trong màn hình `Settings`.

## Cách chạy

Chạy bằng terminal:

```powershell
python main.py
```

Hoặc chạy nhanh trên Windows bằng cách double-click:

```text
run.bat
```

`run.bat` chỉ là file tiện ích để gọi `python main.py` và giữ cửa sổ lại nếu app bị lỗi.

## Cách sử dụng

1. Mở app bằng `python main.py` hoặc `run.bat`.
2. Vào `Image Processing` để chọn ảnh và tinh chỉnh chất lượng ảnh nếu cần.
3. Vào `Vehicle Detection` để chạy model YOLO trên ảnh hiện tại.
4. Xem tổng quan kết quả ở `Dashboard`.
5. Xem biểu đồ ở `Analytics`.
6. Xem lại lịch sử ở `History`, có thể tìm kiếm, xoá hoặc export CSV.
7. Vào `Settings` để đổi theme, model path hoặc confidence threshold.

## Các file dữ liệu sinh ra khi chạy

| Đường dẫn | Ý nghĩa |
| --- | --- |
| `TrafficAIPro/database/trafficai_history.sqlite3` | Database lưu lịch sử detection |
| `TrafficAIPro/exports/` | Nơi lưu file CSV export |
| `__pycache__/` | Cache Python tự sinh, có thể xoá |

Các file runtime như database, export và cache đã được cấu hình trong `.gitignore`.

## Ghi chú về background

Ảnh nền hiện nằm trong:

```text
TrafficAIPro/assets/backgrounds/background_traffic.jpg
TrafficAIPro/assets/backgrounds/background_traffic_blur.jpg
```

App đang dùng bản `background_traffic_blur.jpg` để nền mềm hơn nhưng vẫn đủ rõ. Nếu muốn đổi độ rõ, có thể chỉnh overlay trong:

```text
TrafficAIPro/pages/base.py
```

## Ghi chú phát triển

- `main.py` ở root là launcher chính, nên ưu tiên chạy từ file này.
- `TrafficAIPro/main.py` chứa logic khởi tạo `QApplication`.
- `legacy/` chỉ giữ code cũ để tham khảo, app mới không import từ thư mục này.
- Model mặc định được quản lý trong `TrafficAIPro/utils/paths.py`.
- Nếu app từng lưu đường dẫn model cũ, service settings sẽ tự fallback về `TrafficAIPro/models/weights/best_oto.pt` khi đường dẫn cũ không còn tồn tại.
