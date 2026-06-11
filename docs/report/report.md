# BÁO CÁO ĐỒ ÁN

## ỨNG DỤNG MÔ HÌNH YOLOv26 CHO BÀI TOÁN NHẬN DIỆN VÀ THỐNG KÊ PHƯƠNG TIỆN GIAO THÔNG

**Tên dự án:** TrafficVision AI  
**Tên ứng dụng hiển thị trong mã nguồn:** TrafficAI Pro  
**Môn học:** Xử lý ảnh số / Digital Image Processing  
**Mô hình sử dụng:** YOLOv26 / YOLO26  
**Bộ dữ liệu:** UA-DETRAC chuyển đổi sang định dạng YOLO  
**Giảng viên hướng dẫn:** PGS.TS Hoàng Văn Dũng  

**Nhóm thực hiện:**

| STT | Họ và tên | MSSV |
| --- | --- | --- |
| 1 | Trịnh Nhật Anh | 23110074 |
| 2 | Phạm Công Trường | 23110163 |
| 3 | Trần Minh Huy | 23110106 |

---

# NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN

......................................................................................................................

......................................................................................................................

......................................................................................................................

......................................................................................................................

......................................................................................................................

......................................................................................................................

**Điểm đánh giá:** ..............................................................................................

**Chữ ký giảng viên hướng dẫn:** .........................................................................

---

# LỜI CẢM ƠN

Nhóm chúng em xin gửi lời cảm ơn chân thành đến PGS.TS Hoàng Văn Dũng đã hướng dẫn, góp ý và định hướng cho nhóm trong quá trình thực hiện đề tài TrafficVision AI thuộc môn học Xử lý ảnh số. Những kiến thức về xử lý ảnh, thị giác máy tính và cách triển khai một hệ thống nhận diện thực tế đã giúp nhóm có thêm nền tảng để hoàn thiện sản phẩm.

Nhóm cũng xin cảm ơn nhà trường và thầy cô trong khoa đã tạo điều kiện học tập, thực hành và nghiên cứu. Trong quá trình thực hiện, nhóm đã có cơ hội tìm hiểu sâu hơn về OpenCV, mô hình YOLO, giao diện desktop bằng PyQt6, lưu trữ dữ liệu bằng SQLite và khả năng mở rộng hệ thống với Arduino. Đây là những kiến thức có ý nghĩa thực tiễn, giúp nhóm hiểu rõ hơn cách xây dựng một ứng dụng xử lý ảnh hoàn chỉnh từ dữ liệu đầu vào đến giao diện người dùng.

Do thời gian và kinh nghiệm còn hạn chế, báo cáo và sản phẩm khó tránh khỏi thiếu sót. Nhóm rất mong nhận được nhận xét từ thầy để tiếp tục cải thiện hệ thống trong các phiên bản sau.

---

# TÓM TẮT ĐỀ TÀI

TrafficVision AI là một ứng dụng desktop hỗ trợ nhận diện, phân loại và thống kê phương tiện giao thông từ ảnh hoặc video. Hệ thống sử dụng mô hình YOLOv26 để phát hiện bốn nhóm phương tiện chính gồm Car, Bus, Truck và Van. Bên cạnh phần nhận diện, ứng dụng còn tích hợp các kỹ thuật xử lý ảnh như điều chỉnh độ sáng, độ tương phản, hiệu chỉnh gamma, CLAHE và lọc trung vị nhằm cải thiện chất lượng ảnh đầu vào trước khi đưa vào mô hình.

Ứng dụng được xây dựng bằng Python, PyQt6 và QFluentWidgets, kết hợp OpenCV cho xử lý ảnh, Ultralytics YOLO cho nhận diện, PyQtGraph cho trực quan hóa dữ liệu và SQLite để lưu lịch sử nhận diện. Giao diện hiện tại có các màn hình chính như Dashboard, Image Processing, Vehicle Detection, Video Analysis, Analytics, History và Project Information. Ngoài ra, hệ thống có phần mở rộng Arduino ở chế độ mock hoặc serial thật để mô phỏng tín hiệu đèn giao thông theo tổng số phương tiện phát hiện được.

Trong kho mã nguồn hiện có file trọng số `TrafficAIPro/models/weights/Car_YOLO26_Best.pt`, video mẫu `test_video.mp4`, cơ sở dữ liệu SQLite lịch sử nhận diện và các ảnh kết quả đã lưu trong thư mục runtime. Tuy nhiên, kho mã nguồn chưa chứa các file kết quả huấn luyện như `results.png`, `confusion_matrix.png`, biểu đồ precision-recall, F1 curve hoặc file chia tập dữ liệu train/validation/test. Vì vậy, các phần kết quả huấn luyện trong báo cáo được trình bày bằng placeholder để bổ sung sau khi có dữ liệu chính thức.

---

# DANH MỤC HÌNH ẢNH

| Hình | Tên hình | Ghi chú |
| --- | --- | --- |
| Hình 2.1 | Kiến trúc tổng thể hệ thống TrafficVision AI | Cần chèn sơ đồ kiến trúc |
| Hình 2.2 | Kết quả tăng cường chất lượng ảnh | Cần chèn ảnh trước/sau xử lý |
| Hình 2.3 | Giao diện Dashboard | Cần chèn ảnh màn hình |
| Hình 2.4 | Giao diện Image Processing | Cần chèn ảnh màn hình |
| Hình 2.5 | Giao diện Vehicle Detection có bounding box | Cần chèn ảnh màn hình |
| Hình 2.6 | Giao diện Video Analysis | Cần chèn ảnh màn hình |
| Hình 2.7 | Giao diện Analytics | Cần chèn ảnh màn hình |
| Hình 2.8 | Giao diện History | Cần chèn ảnh màn hình |
| Hình 2.9 | Giao diện Project Information | Cần chèn ảnh màn hình |
| Hình 3.1 | Biểu đồ kết quả huấn luyện `results.png` | Cần bổ sung từ lần huấn luyện |
| Hình 3.2 | Ma trận nhầm lẫn | Cần bổ sung từ lần huấn luyện |
| Hình 3.3 | Precision-Recall Curve | Cần bổ sung từ lần huấn luyện |
| Hình 3.4 | F1 Curve | Cần bổ sung từ lần huấn luyện |
| Hình 3.5 | Kết quả nhận diện trên ảnh | Cần chèn ảnh kết quả |
| Hình 3.6 | Kết quả nhận diện trên video | Cần chèn ảnh kết quả |

---

# DANH MỤC BẢNG

| Bảng | Tên bảng | Ghi chú |
| --- | --- | --- |
| Bảng 1.1 | Mục tiêu chính của đề tài | Trình bày trong Chương 1 |
| Bảng 2.1 | Công nghệ và thư viện sử dụng | Trình bày trong Chương 2 |
| Bảng 2.2 | Quy ước mức độ giao thông cho Arduino | Trình bày trong Chương 2 |
| Bảng 3.1 | Các lớp dữ liệu nhận diện | Trình bày trong Chương 3 |
| Bảng 3.2 | Chia tập dữ liệu train/validation/test | Cần bổ sung số lượng ảnh |
| Bảng 3.3 | Cấu hình huấn luyện mô hình | Cần bổ sung từ file cấu hình huấn luyện |
| Bảng 3.4 | Đánh giá ưu điểm và hạn chế | Trình bày trong Chương 3 |

---

# CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI

## 1.1. Lý do chọn đề tài

Giao thông đô thị ngày càng có mật độ cao, đặc biệt tại các tuyến đường lớn, khu vực gần trường học, khu công nghiệp và trung tâm thành phố. Việc theo dõi lưu lượng phương tiện bằng phương pháp thủ công thường tốn nhân lực, khó duy trì liên tục và khó tổng hợp dữ liệu phục vụ phân tích. Trong bối cảnh đó, thị giác máy tính trở thành một hướng tiếp cận phù hợp vì có thể tự động phát hiện phương tiện từ ảnh hoặc video, sau đó thống kê số lượng theo từng loại xe.

Đề tài TrafficVision AI được lựa chọn nhằm vận dụng kiến thức của môn Xử lý ảnh số vào một bài toán gần với thực tế. Hệ thống không chỉ dừng lại ở việc chạy mô hình nhận diện mà còn kết hợp tiền xử lý ảnh, giao diện sử dụng, lưu trữ lịch sử, biểu đồ phân tích và khả năng mở rộng với phần cứng Arduino. Cách tiếp cận này giúp nhóm hiểu rõ hơn vai trò của xử lý ảnh trong một pipeline hoàn chỉnh, từ dữ liệu đầu vào đến kết quả trực quan cho người dùng.

Mô hình YOLOv26 được sử dụng vì phù hợp với yêu cầu phát hiện đối tượng theo thời gian gần thực, có thể nhận diện nhiều phương tiện trong cùng một khung hình và dễ tích hợp với ứng dụng Python thông qua thư viện Ultralytics. Bộ dữ liệu UA-DETRAC sau khi chuyển đổi sang định dạng YOLO cung cấp các tình huống giao thông đa dạng, phù hợp để huấn luyện và kiểm thử hệ thống nhận diện phương tiện.

## 1.2. Mục tiêu đề tài

Mục tiêu chính của đề tài là xây dựng một ứng dụng desktop có khả năng nhận diện và thống kê phương tiện giao thông từ ảnh hoặc video. Hệ thống cần có giao diện rõ ràng, hỗ trợ xử lý ảnh trước khi nhận diện, lưu lại kết quả và trình bày dữ liệu dưới dạng dễ quan sát.

**Bảng 1.1. Mục tiêu chính của đề tài**

| Nhóm mục tiêu | Nội dung |
| --- | --- |
| Nhận diện phương tiện | Phát hiện các lớp Car, Bus, Truck và Van bằng mô hình YOLOv26 |
| Xử lý ảnh | Cải thiện ảnh đầu vào bằng brightness, contrast, gamma, CLAHE và median filter |
| Thống kê | Đếm số lượng từng loại phương tiện và tổng số phương tiện |
| Giao diện | Xây dựng ứng dụng desktop bằng PyQt6 và QFluentWidgets |
| Lưu trữ | Lưu lịch sử nhận diện bằng SQLite và hỗ trợ xuất CSV |
| Video | Phân tích video, hiển thị tracking và thông tin FPS nếu người dùng mở video |
| Phần cứng mở rộng | Gửi mức độ giao thông sang Arduino thông qua Serial hoặc Mock mode |

## 1.3. Đối tượng và phạm vi nghiên cứu

Đối tượng nghiên cứu của đề tài là các phương tiện giao thông xuất hiện trong ảnh hoặc video đường phố. Trong phạm vi hiện tại, hệ thống tập trung vào bốn lớp phương tiện gồm Car, Bus, Truck và Van. Các lớp khác như xe máy, người đi bộ hoặc biển số xe chưa phải là trọng tâm chính của hệ thống.

Phạm vi nghiên cứu bao gồm việc xây dựng pipeline xử lý ảnh, tích hợp mô hình YOLOv26, thiết kế giao diện desktop, lưu lịch sử nhận diện và trình bày thống kê cơ bản. Phần Arduino được xem là phần mở rộng để minh họa khả năng kết nối hệ thống thị giác máy tính với thiết bị cảnh báo vật lý. Do kho mã nguồn chưa có đầy đủ file kết quả huấn luyện, báo cáo không đưa ra các chỉ số huấn luyện chính thức mà chỉ để placeholder để bổ sung sau.

---

# CHƯƠNG 2: THIẾT KẾ GIẢI PHÁP

## 2.1. Bài toán đặt ra

Bài toán đặt ra là xây dựng một hệ thống có thể nhận ảnh hoặc video giao thông làm đầu vào, xử lý chất lượng ảnh khi cần thiết, phát hiện các phương tiện trong khung hình, phân loại theo nhóm phương tiện và thống kê số lượng. Kết quả cần được hiển thị trực quan để người dùng dễ quan sát, đồng thời được lưu lại để phục vụ tra cứu hoặc xuất báo cáo.

Một khó khăn của bài toán là ảnh giao thông thường chịu ảnh hưởng bởi ánh sáng, thời tiết, góc camera, độ phân giải và hiện tượng che khuất giữa các phương tiện. Ở những cảnh đông xe, bounding box của các phương tiện có thể chồng lấn, khiến mô hình dễ bỏ sót hoặc nhầm lẫn giữa các lớp xe. Vì vậy, hệ thống cần kết hợp cả xử lý ảnh và mô hình học sâu để tăng khả năng nhận diện trong các điều kiện khác nhau.

## 2.2. Giải pháp đề xuất

Giải pháp của đề tài là xây dựng một ứng dụng desktop tên TrafficVision AI. Ứng dụng sử dụng OpenCV để xử lý ảnh đầu vào, sau đó đưa ảnh vào mô hình YOLOv26 thông qua thư viện Ultralytics. Kết quả nhận diện được biểu diễn bằng bounding box, nhãn lớp, độ tin cậy và số lượng từng loại phương tiện.

Về giao diện, ứng dụng được chia thành nhiều màn hình chức năng. Màn hình Image Processing cho phép tải ảnh và điều chỉnh các tham số xử lý ảnh. Màn hình Vehicle Detection hiển thị kết quả nhận diện trên ảnh. Màn hình Video Analysis hỗ trợ mở video, chạy detection hoặc tracking, hiển thị Track ID, counting line, FPS và các thống kê theo thời gian. Màn hình Dashboard và Analytics tổng hợp kết quả, trong khi History lưu lại lịch sử nhận diện bằng SQLite.

Về phần cứng, hệ thống có một service Arduino cho phép gửi tổng số phương tiện theo định dạng `LEVEL,CAR,BUS,TRUCK,VAN,TOTAL`. Trong mã nguồn hiện tại, chế độ mặc định là Mock, nghĩa là ứng dụng có thể mô phỏng quá trình gửi dữ liệu mà chưa cần kết nối phần cứng thật.

## 2.3. Kiến trúc tổng thể hệ thống

[CHÈN HÌNH 2.1. KIẾN TRÚC TỔNG THỂ HỆ THỐNG TRAFFICVISION AI]

**Hình 2.1. Kiến trúc tổng thể hệ thống TrafficVision AI**

Luồng xử lý tổng thể của hệ thống được thiết kế như sau:

```text
Input Image/Video
→ Image Processing
→ YOLOv26 Detection
→ Vehicle Classification
→ Vehicle Counting
→ Dashboard / Analytics / History
→ Arduino Integration
```

Trong kiến trúc này, ảnh hoặc video là dữ liệu đầu vào. Nếu người dùng sử dụng ảnh, hệ thống có thể áp dụng các kỹ thuật tăng cường chất lượng ảnh trước khi chạy nhận diện. Nếu người dùng sử dụng video, từng frame sẽ được xử lý và đưa qua mô hình YOLOv26 để nhận diện hoặc tracking. Kết quả cuối cùng gồm ảnh có bounding box, số lượng phương tiện, thời gian xử lý, độ tin cậy trung bình và dữ liệu lịch sử.

Các thành phần chính trong mã nguồn gồm `TrafficAIPro/services/image_service.py` cho xử lý ảnh, `TrafficAIPro/services/detection_service.py` cho nhận diện và tracking, `TrafficAIPro/database/history_repository.py` cho SQLite, `TrafficAIPro/services/arduino_service.py` cho phần cứng mở rộng và `TrafficAIPro/ui/main_window.py` để kết nối các màn hình trong ứng dụng.

## 2.4. Quy trình hoạt động của hệ thống

Khi ứng dụng khởi động, chương trình tạo các thư mục runtime cần thiết, nạp theme giao diện, khởi tạo service xử lý ảnh, service nhận diện, service Arduino và repository lưu lịch sử. File launcher chính ở thư mục gốc là `main.py`, sau đó gọi vào `TrafficAIPro/main.py` để khởi tạo ứng dụng PyQt6.

Với ảnh tĩnh, người dùng tải ảnh trong màn hình Image Processing. Ứng dụng hiển thị ảnh gốc và ảnh sau xử lý, đồng thời cho phép điều chỉnh gamma, brightness, contrast, bật/tắt CLAHE và chọn kernel cho median filter. Khi ảnh được cập nhật, ảnh đã xử lý được gửi sang màn hình Vehicle Detection. Tại đây, mô hình YOLOv26 chạy inference, vẽ bounding box, đếm từng loại phương tiện và lưu kết quả vào SQLite nếu đây là ảnh mới.

Với video, người dùng mở file video trong màn hình Video Analysis. Ứng dụng đọc từng frame bằng OpenCV, tùy chọn tăng cường ảnh, sau đó chạy YOLO theo chế độ detection hoặc tracking. Trang video hỗ trợ ByteTrack, BoT-SORT, Track ID, counting line ngang hoặc dọc, confidence threshold, IoU threshold và thống kê thời gian thực như tổng xe, từng loại xe, FPS, thời gian xử lý và confidence trung bình.

Sau mỗi lần nhận diện ảnh, Dashboard, Analytics và History được cập nhật. Dashboard hiển thị tổng quan, Analytics hiển thị biểu đồ phân bố và so sánh ảnh gốc với ảnh đã xử lý, còn History cho phép tìm kiếm, sắp xếp, xem lại ảnh kết quả, xóa record và xuất CSV.

## 2.5. Thư viện và công nghệ sử dụng

**Bảng 2.1. Công nghệ và thư viện sử dụng**

| Công nghệ | Vai trò trong hệ thống |
| --- | --- |
| Python | Ngôn ngữ lập trình chính |
| OpenCV | Đọc ảnh/video, xử lý ảnh, vẽ bounding box và thao tác frame |
| PyQt6 | Xây dựng ứng dụng desktop |
| QFluentWidgets | Cung cấp component giao diện theo phong cách Fluent |
| Ultralytics YOLO | Load mô hình YOLOv26, chạy detection và tracking |
| NumPy | Tính toán trên ảnh, histogram và dữ liệu số |
| Pillow | Hỗ trợ thao tác ảnh trong môi trường Python |
| SQLite | Lưu lịch sử nhận diện cục bộ |
| PyQtGraph | Trực quan hóa biểu đồ trong giao diện |
| pyserial | Kết nối Python với Arduino thông qua cổng COM |

### 2.5.1. Python

Python là ngôn ngữ chính được sử dụng để phát triển toàn bộ hệ thống. Python phù hợp với đề tài vì có hệ sinh thái mạnh cho xử lý ảnh, học sâu, giao diện desktop và giao tiếp phần cứng. Các thành phần như OpenCV, Ultralytics, PyQt6 và SQLite đều có thể tích hợp thuận tiện trong một ứng dụng Python.

### 2.5.2. OpenCV

OpenCV được sử dụng để đọc ảnh, đọc video, chuyển đổi không gian màu, áp dụng các kỹ thuật xử lý ảnh và vẽ kết quả nhận diện. Trong service xử lý ảnh, OpenCV hỗ trợ CLAHE trên kênh sáng của không gian màu LAB, hiệu chỉnh gamma bằng bảng tra cứu, điều chỉnh brightness/contrast và lọc trung vị. Trong video, OpenCV còn được dùng để đọc từng frame từ `cv2.VideoCapture` và vẽ counting line.

### 2.5.3. PyQt6 và QFluentWidgets

PyQt6 được sử dụng để xây dựng ứng dụng desktop. Giao diện được tổ chức bằng `QMainWindow`, `QStackedWidget`, layout ngang/dọc, bảng dữ liệu, nút, combobox, slider và các widget hiển thị ảnh. QFluentWidgets được dùng để tạo giao diện hiện đại hơn thông qua các thành phần như `CardWidget`, `PrimaryPushButton`, `TableWidget`, `SearchLineEdit`, `InfoBar` và icon Fluent.

### 2.5.4. Ultralytics YOLO

Ultralytics YOLO là thư viện dùng để load file trọng số `.pt` và chạy nhận diện. Trong mã nguồn, service nhận diện gọi `YOLO(self.model_path)` để nạp model, sau đó dùng `model(...)` cho ảnh và `model.track(...)` cho video tracking. File model mặc định trong repository là:

```text
TrafficAIPro/models/weights/Car_YOLO26_Best.pt
```

### 2.5.5. SQLite

SQLite được sử dụng để lưu lịch sử nhận diện trong file:

```text
TrafficAIPro/database/trafficai_history.sqlite3
```

Bảng `detections` lưu các thông tin như tên ảnh, ngày nhận diện, số lượng car/bus/truck/van, tổng số phương tiện, confidence trung bình, thời gian xử lý và đường dẫn ảnh kết quả. Cách lưu trữ này phù hợp với ứng dụng desktop vì không cần triển khai database server riêng.

### 2.5.6. PyQtGraph

PyQtGraph được sử dụng cho phần biểu đồ trong giao diện Analytics. Ứng dụng có biểu đồ phân bố phương tiện và biểu đồ số lượng phương tiện theo từng lớp. Việc trực quan hóa giúp người dùng nhanh chóng nắm được loại phương tiện nào xuất hiện nhiều hơn trong lần nhận diện gần nhất.

### 2.5.7. Arduino và Serial Communication

Arduino là phần mở rộng của hệ thống, dùng để mô phỏng cảnh báo giao thông bằng LED, LCD và buzzer. Python gửi dữ liệu qua Serial theo payload `LEVEL,CAR,BUS,TRUCK,VAN,TOTAL`. Trong mã nguồn hiện tại, `ARDUINO_MOCK_MODE = True`, do đó ứng dụng có thể chạy mà không cần cắm phần cứng thật. Khi chuyển sang serial thật, người dùng cần đặt đúng cổng COM, ví dụ `COM3`.

## 2.6. Cơ chế hoạt động của các kỹ thuật xử lý ảnh

### 2.6.1. Brightness Adjustment

Brightness adjustment là kỹ thuật thay đổi độ sáng tổng thể của ảnh. Trong OpenCV, thao tác này thường được thực hiện bằng cách cộng thêm một giá trị beta vào từng pixel thông qua hàm `convertScaleAbs`. Khi ảnh quá tối, tăng brightness giúp làm rõ phương tiện và nền đường. Tuy nhiên, nếu tăng quá nhiều, ảnh có thể bị cháy sáng và làm mất chi tiết.

### 2.6.2. Contrast Adjustment

Contrast adjustment thay đổi mức chênh lệch giữa vùng sáng và vùng tối trong ảnh. Khi tăng contrast hợp lý, đường viền phương tiện, bánh xe, kính xe và phần thân xe có thể trở nên rõ hơn. Điều này giúp mô hình nhận diện có thêm đặc trưng thị giác để phân biệt phương tiện với nền. Trong hệ thống, contrast được điều chỉnh bằng hệ số alpha trong OpenCV.

### 2.6.3. Gamma Correction

Gamma correction là kỹ thuật biến đổi phi tuyến cường độ sáng của ảnh. Khác với brightness tuyến tính, gamma có thể tăng sáng vùng tối hoặc giảm sáng vùng quá sáng theo cách mềm hơn. Trong mã nguồn, gamma được thực hiện bằng bảng tra cứu 256 giá trị, sau đó áp dụng lên ảnh bằng `cv2.LUT`. Kỹ thuật này hữu ích với ảnh giao thông có ánh sáng không đều.

### 2.6.4. CLAHE Enhancement

CLAHE là viết tắt của Contrast Limited Adaptive Histogram Equalization. Kỹ thuật này chia ảnh thành các vùng nhỏ, cân bằng histogram cục bộ và giới hạn mức tăng tương phản để tránh khuếch đại nhiễu quá mức. Trong hệ thống, CLAHE được áp dụng trên kênh L của không gian màu LAB, sau đó ghép lại với các kênh màu còn lại. Cách làm này giúp tăng độ rõ của ảnh nhưng vẫn giữ màu tương đối tự nhiên.

### 2.6.5. Median Filter

Median filter là bộ lọc phi tuyến dùng để giảm nhiễu bằng cách thay giá trị pixel bằng trung vị của các pixel lân cận. Bộ lọc này đặc biệt hiệu quả với nhiễu dạng muối tiêu và ít làm mờ biên hơn so với lọc trung bình. Trong ứng dụng, người dùng có thể chọn kích thước kernel lẻ để áp dụng median blur trước khi đưa ảnh vào mô hình nhận diện.

### 2.6.6. Vai trò của xử lý ảnh trong hệ thống

Xử lý ảnh đóng vai trò chuẩn hóa và cải thiện chất lượng đầu vào cho mô hình YOLOv26. Trong điều kiện ảnh thiếu sáng, ngược sáng hoặc có tương phản thấp, việc tăng cường ảnh có thể giúp phương tiện nổi bật hơn. Tuy nhiên, xử lý ảnh không phải lúc nào cũng làm tăng độ chính xác. Nếu tham số quá mạnh, ảnh có thể bị biến dạng hoặc mất chi tiết. Vì vậy, hệ thống cung cấp các thanh điều chỉnh trực quan để người dùng quan sát ảnh trước/sau xử lý và lựa chọn cấu hình phù hợp.

[CHÈN HÌNH 2.2. KẾT QUẢ TĂNG CƯỜNG CHẤT LƯỢNG ẢNH SAU KHI ÁP DỤNG CÁC KỸ THUẬT XỬ LÝ ẢNH]

**Hình 2.2. Kết quả tăng cường chất lượng ảnh sau khi áp dụng các kỹ thuật xử lý ảnh**

## 2.7. Thiết kế giao diện hệ thống

Giao diện TrafficVision AI được tổ chức theo sidebar với ba nhóm chính: MAIN, DETECT và REPORTS. Nhóm MAIN gồm Dashboard. Nhóm DETECT gồm Image Processing, Vehicle Detection và Video Analysis. Nhóm REPORTS gồm Analytics, History và Project Information. Trong mã nguồn, các màn hình này được khởi tạo trong `TrafficAIPro/ui/main_window.py` và chuyển đổi bằng `QStackedWidget`.

### 2.7.1. Dashboard

Dashboard là màn hình tổng quan của hệ thống. Màn hình này hiển thị số lượng tổng, số lượng từng loại phương tiện, tóm tắt lần nhận diện gần nhất, thời gian xử lý, confidence trung bình, model đang hoạt động và trạng thái Arduino. Dashboard cũng có khu vực thông tin phần cứng để hiển thị chế độ Mock hoặc Connected, màu đèn giao thông và payload cuối cùng đã gửi.

[CHÈN ẢNH DASHBOARD]

**Hình 2.3. Giao diện Dashboard của hệ thống**

### 2.7.2. Image Processing

Màn hình Image Processing cho phép người dùng tải ảnh giao thông và xem song song ảnh gốc với ảnh đã xử lý. Các tham số có thể điều chỉnh gồm gamma, brightness, contrast, CLAHE và median filter. Sau khi ảnh được cập nhật, hệ thống phát tín hiệu để chuyển ảnh đã xử lý sang phần nhận diện. Thiết kế này giúp người dùng thấy được tác động của tiền xử lý trước khi quan sát kết quả YOLO.

[CHÈN ẢNH IMAGE PROCESSING]

**Hình 2.4. Giao diện Image Processing**

### 2.7.3. Vehicle Detection

Màn hình Vehicle Detection chạy YOLOv26 trên ảnh đã xử lý. Kết quả được hiển thị bằng ảnh có bounding box và các thẻ thống kê số lượng Cars, Buses, Trucks, Vans và Total Vehicles. Theo mã nguồn, confidence mặc định cho ảnh là `0.25`. Sau khi nhận diện xong, kết quả được lưu vào SQLite nếu ảnh chưa được lưu trùng theo chữ ký ảnh.

[CHÈN ẢNH VEHICLE DETECTION CÓ BOUNDING BOX]

**Hình 2.5. Giao diện Vehicle Detection với bounding box**

### 2.7.4. Video Analysis

Trong repository hiện tại, màn hình Video Analysis đã được triển khai. Màn hình này hỗ trợ mở các định dạng video như `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`; chọn tracker ByteTrack hoặc BoT-SORT; điều chỉnh confidence và IoU; bật/tắt enhancement; bật/tắt Track ID; chọn counting line ngang hoặc dọc; theo dõi frame, FPS, thời gian xử lý và confidence trung bình.

[CHÈN ẢNH VIDEO ANALYSIS]

**Hình 2.6. Giao diện Video Analysis**

### 2.7.5. Analytics

Màn hình Analytics hiển thị biểu đồ phân bố phương tiện, biểu đồ cột theo từng lớp xe và phần so sánh giữa ảnh gốc với ảnh đã tăng cường. Các chỉ số so sánh gồm brightness, contrast, số xe phát hiện và confidence trung bình. Màn hình này giúp người dùng đánh giá sơ bộ tác động của xử lý ảnh lên kết quả nhận diện.

[CHÈN ẢNH ANALYTICS]

**Hình 2.7. Giao diện Analytics**

### 2.7.6. History

Màn hình History lưu và hiển thị lịch sử nhận diện từ SQLite. Người dùng có thể tìm kiếm theo tên ảnh, sắp xếp theo mới nhất, cũ nhất, nhiều xe nhất hoặc confidence cao nhất. Khi chọn một dòng lịch sử, ứng dụng hiển thị ảnh annotated tương ứng nếu file còn tồn tại. Màn hình này cũng hỗ trợ xóa record và xuất dữ liệu ra file CSV.

[CHÈN ẢNH HISTORY]

**Hình 2.8. Giao diện History**

### 2.7.7. Project Information

Trong repository hiện tại, màn hình Project Information đã được triển khai. Màn hình này trình bày tên dự án TrafficVision AI, thông tin môn học, năm học, thành viên nhóm, công nghệ chính và sơ đồ kiến trúc dạng flow. Đây là trang phù hợp để giới thiệu nhanh sản phẩm khi báo cáo hoặc demo trước giảng viên.

[CHÈN ẢNH PROJECT INFORMATION]

**Hình 2.9. Giao diện Project Information**

## 2.8. Thiết kế hệ thống phần cứng

Phần cứng Arduino được thiết kế như một phần mở rộng, không phải trọng tâm chính của đề tài. Mục đích của phần này là mô phỏng khả năng biến kết quả nhận diện thành tín hiệu cảnh báo giao thông vật lý. Cấu hình phần cứng dự kiến gồm Arduino Uno R3, LCD 1602 I2C, ba LED xanh/vàng/đỏ và buzzer.

Dữ liệu từ Python được gửi qua Serial với cấu trúc:

```text
LEVEL,CAR,BUS,TRUCK,VAN,TOTAL
```

Trong đó `LEVEL` được xác định theo tổng số phương tiện:

**Bảng 2.2. Quy ước mức độ giao thông cho Arduino**

| Tổng số phương tiện | Mức | Tín hiệu cảnh báo |
| --- | --- | --- |
| `total < 10` | Green | Bật LED xanh |
| `total < 20` | Yellow | Bật LED vàng |
| `total >= 20` | Red | Bật LED đỏ và buzzer |

Ví dụ, nếu tổng số phương tiện phát hiện được lớn hơn hoặc bằng 20, hệ thống gửi mức `R` sang Arduino. Khi đó LED đỏ và buzzer được kích hoạt để cảnh báo đoạn đường đang đông, người tham gia giao thông nên cân nhắc chọn lộ trình khác. Trong giai đoạn hiện tại, mã nguồn Python đã hỗ trợ Arduino Mock mode và có thể chuyển sang Serial thật khi cấu hình cổng COM.

## 2.9. Kết luận chương

Chương 2 đã trình bày thiết kế giải pháp tổng thể của TrafficVision AI, bao gồm pipeline xử lý ảnh, mô hình YOLOv26, giao diện desktop, lưu trữ lịch sử, phân tích dữ liệu và phần mở rộng Arduino. Hệ thống được tổ chức theo hướng module, trong đó mỗi service đảm nhiệm một nhóm chức năng rõ ràng. Cách thiết kế này giúp ứng dụng dễ bảo trì và có khả năng mở rộng thêm tracking nâng cao, camera real-time, nhận diện biển số hoặc kết nối IoT trong tương lai.

---

# CHƯƠNG 3: KẾT QUẢ THỰC NGHIỆM

## 3.1. Dataset sử dụng

### 3.1.1. Giới thiệu UA-DETRAC

UA-DETRAC là bộ dữ liệu giao thông thường được sử dụng trong các bài toán phát hiện và theo dõi phương tiện. Bộ dữ liệu gồm nhiều cảnh đường phố với điều kiện ánh sáng, mật độ phương tiện và góc nhìn khác nhau. Trong đề tài này, dataset được định hướng sử dụng sau khi chuyển đổi sang định dạng YOLO để phù hợp với quá trình huấn luyện mô hình YOLOv26.

Trong repository hiện tại, nhóm chưa tìm thấy thư mục dataset, file `data.yaml` hoặc các file mô tả chính thức về số lượng ảnh train/validation/test. Vì vậy, phần chia tập dữ liệu cần được bổ sung sau khi nhóm đưa vào báo cáo bản chính thức các thông tin từ quá trình chuẩn bị dữ liệu.

### 3.1.2. Các lớp dữ liệu

Hệ thống tập trung nhận diện bốn lớp phương tiện chính. Trong mã nguồn, các lớp này được khai báo ở `TrafficAIPro/models/detection.py` dưới dạng `car`, `bus`, `truck`, `van`.

**Bảng 3.1. Các lớp dữ liệu nhận diện**

| STT | Tên lớp trong báo cáo | Tên lớp trong mã nguồn | Ý nghĩa |
| --- | --- | --- | --- |
| 1 | Car | `car` | Ô tô con |
| 2 | Bus | `bus` | Xe buýt |
| 3 | Truck | `truck` | Xe tải |
| 4 | Van | `van` | Xe van |

### 3.1.3. Chia tập Train / Validation / Test

Do repository hiện tại chưa có file chia tập hoặc thống kê dataset, báo cáo chưa thể ghi số lượng ảnh cụ thể cho từng tập. Cần bổ sung thông tin sau khi có thư mục dataset hoặc file cấu hình huấn luyện chính thức.

**Bảng 3.2. Chia tập dữ liệu train/validation/test**

| Tập dữ liệu | Số lượng ảnh | Ghi chú |
| --- | --- | --- |
| Train | [BỔ SUNG SỐ LƯỢNG ẢNH TRAIN/VALIDATION/TEST] | Cần lấy từ dataset sau khi chuyển đổi YOLO |
| Validation | [BỔ SUNG SỐ LƯỢNG ẢNH TRAIN/VALIDATION/TEST] | Cần lấy từ dataset sau khi chuyển đổi YOLO |
| Test | [BỔ SUNG SỐ LƯỢNG ẢNH TRAIN/VALIDATION/TEST] | Cần lấy từ dataset sau khi chuyển đổi YOLO |

## 3.2. Mô hình YOLOv26

### 3.2.1. Cấu hình huấn luyện

Repository hiện có file trọng số `Car_YOLO26_Best.pt`, tuy nhiên chưa có file cấu hình huấn luyện, file log, `args.yaml`, `results.csv` hoặc thư mục `runs/train`. Vì vậy, các tham số như số epoch, batch size, image size huấn luyện, learning rate, optimizer và augmentation cần được bổ sung từ lần huấn luyện thật.

**Bảng 3.3. Cấu hình huấn luyện mô hình**

| Tham số | Giá trị |
| --- | --- |
| Model | YOLOv26 / YOLO26 |
| Trọng số sử dụng trong ứng dụng | `TrafficAIPro/models/weights/Car_YOLO26_Best.pt` |
| Dataset | UA-DETRAC chuyển đổi sang YOLO format |
| Epoch | [BỔ SUNG EPOCH] |
| Batch size | [BỔ SUNG BATCH SIZE] |
| Image size | [BỔ SUNG IMAGE SIZE] |
| Optimizer | [BỔ SUNG OPTIMIZER] |
| Learning rate | [BỔ SUNG LEARNING RATE] |
| Thiết bị huấn luyện | [BỔ SUNG GPU/CPU SỬ DỤNG] |

### 3.2.2. Môi trường huấn luyện

Môi trường chạy ứng dụng được xác định qua `requirements.txt`, gồm PyQt6, PyQt6-Fluent-Widgets, OpenCV, Ultralytics, NumPy, Pillow, PyQtGraph và pyserial. Tuy nhiên, môi trường huấn luyện cụ thể chưa được ghi lại trong repository. Khi hoàn thiện báo cáo, nhóm cần bổ sung thông tin về GPU/CPU, phiên bản Python, phiên bản CUDA nếu có và nền tảng huấn luyện.

### 3.2.3. Quy trình huấn luyện

Quy trình huấn luyện dự kiến gồm các bước: chuyển đổi annotation UA-DETRAC sang định dạng YOLO, chia dữ liệu thành train/validation/test, cấu hình file dữ liệu, huấn luyện mô hình YOLOv26, đánh giá trên validation/test và xuất ra các file kết quả. Sau đó, trọng số tốt nhất được đưa vào thư mục `TrafficAIPro/models/weights/` để ứng dụng desktop sử dụng.

Do các file huấn luyện không có trong repository, báo cáo không trình bày chi tiết chỉ số huấn luyện ở giai đoạn này. Các thông tin này cần được bổ sung từ kết quả huấn luyện chính thức.

## 3.3. Kết quả huấn luyện

[CHÈN RESULTS.PNG]

**Hình 3.1. Biểu đồ kết quả huấn luyện `results.png`**

[CHÈN CONFUSION_MATRIX.PNG]

**Hình 3.2. Ma trận nhầm lẫn của mô hình**

[CHÈN PRECISION-RECALL CURVE]

**Hình 3.3. Precision-Recall Curve**

[CHÈN F1 CURVE]

**Hình 3.4. F1 Curve**

Các chỉ số chi tiết sẽ được bổ sung dựa trên file kết quả huấn luyện của mô hình.

Trong quá trình kiểm tra repository, nhóm nhận thấy một số giá trị metric được hiển thị cứng trong giao diện Dashboard. Tuy nhiên, vì repository không chứa file kết quả huấn luyện tương ứng, các giá trị này không được sử dụng như kết quả thực nghiệm chính thức trong báo cáo. Khi hoàn thiện bản nộp, nhóm cần lấy metric từ các file xuất ra bởi quá trình huấn luyện YOLO.

## 3.4. Kết quả nhận diện trên ảnh

Repository hiện có các ảnh annotated được lưu runtime trong thư mục:

```text
TrafficAIPro/database/detected_images/
```

Khi kiểm tra cục bộ, thư mục này có 30 ảnh kết quả đã lưu, còn cơ sở dữ liệu SQLite có 32 record lịch sử nhận diện. Các record này cho thấy chức năng lưu lịch sử và ảnh kết quả đã được ứng dụng sử dụng trong quá trình chạy thử. Tuy nhiên, để báo cáo học thuật rõ ràng hơn, nhóm nên chọn một số ảnh đại diện, chèn vào báo cáo và mô tả ngắn gọn kết quả theo từng trường hợp.

[CHÈN ẢNH KẾT QUẢ NHẬN DIỆN TRÊN ẢNH]

**Hình 3.5. Kết quả nhận diện phương tiện trên ảnh tĩnh**

Phần mô tả kết quả nên ghi rõ tên ảnh, số lượng Car, Bus, Truck, Van, tổng số phương tiện và nhận xét về các trường hợp nhận diện đúng, bỏ sót hoặc nhầm lẫn nếu có.

## 3.5. Kết quả nhận diện trên video

Repository có file video mẫu:

```text
test_video.mp4
```

Màn hình Video Analysis đã hỗ trợ mở video, chạy YOLO tracking, hiển thị Track ID, counting line, FPS, confidence trung bình và số lượng phương tiện theo từng lớp. Khi hoàn thiện báo cáo, nhóm cần chạy thử video, chụp một khung hình kết quả có bounding box và counting line để minh họa.

[CHÈN ẢNH KẾT QUẢ NHẬN DIỆN TRÊN VIDEO]

**Hình 3.6. Kết quả nhận diện và tracking phương tiện trên video**

## 3.6. Kết quả giao diện hệ thống

Qua kiểm tra mã nguồn, các màn hình chính của hệ thống đã được triển khai gồm Dashboard, Image Processing, Vehicle Detection, Video Analysis, Analytics, History và Project Information. Giao diện dùng PyQt6 kết hợp QFluentWidgets, có sidebar điều hướng, header trạng thái model, các card thống kê, bảng lịch sử và vùng hiển thị ảnh/video.

Kết quả giao diện cần được bổ sung bằng ảnh chụp màn hình trực tiếp từ ứng dụng. Các vị trí cần chèn đã được liệt kê trong Chương 2. Khi chụp màn hình, nên ưu tiên các trạng thái có dữ liệu thật: Dashboard sau khi nhận diện, Vehicle Detection có bounding box, Analytics có biểu đồ, History có record và Video Analysis đang chạy video.

## 3.7. Kết quả tích hợp Arduino

Ở giai đoạn hiện tại, hệ thống đã hỗ trợ chế độ Arduino Mock để mô phỏng dữ liệu gửi đến phần cứng. Khi phần cứng được kết nối, hệ thống có thể chuyển sang chế độ Serial thật thông qua cổng COM.

Trong mã nguồn, service Arduino xác định mức độ giao thông theo tổng số phương tiện: dưới 10 xe là Green, từ 10 đến 19 xe là Yellow, từ 20 xe trở lên là Red. Payload được gửi có dạng `LEVEL,CAR,BUS,TRUCK,VAN,TOTAL`, ví dụ `R,12,3,4,2,21`.

## 3.8. Đánh giá kết quả

**Bảng 3.4. Đánh giá ưu điểm và hạn chế**

| Nhóm đánh giá | Nội dung |
| --- | --- |
| Ưu điểm | Hệ thống có pipeline tương đối đầy đủ từ xử lý ảnh, nhận diện, thống kê, biểu đồ, lịch sử đến phần cứng mở rộng. Giao diện trực quan, có nhiều màn hình phục vụ demo và báo cáo. |
| Ưu điểm | Mã nguồn được chia module rõ ràng, gồm service xử lý ảnh, service nhận diện, repository SQLite, service Arduino và các page giao diện riêng. |
| Ưu điểm | Ứng dụng đã có model `.pt`, video mẫu, SQLite history, ảnh annotated runtime và chức năng xuất CSV. |
| Hạn chế | Repository chưa có dataset, file chia tập train/validation/test và file kết quả huấn luyện chính thức. |
| Hạn chế | Các metric huấn luyện chưa thể xác minh từ file log, do đó chưa được đưa vào báo cáo như kết quả chính thức. |
| Hạn chế | Phần Arduino hiện ở chế độ mock mặc định, cần kiểm thử thêm với phần cứng thật. |
| Nhận xét tổng quan | TrafficVision AI đã thể hiện được luồng ứng dụng xử lý ảnh số vào bài toán giao thông. Để hoàn thiện hơn, nhóm cần bổ sung minh chứng huấn luyện, ảnh chụp giao diện và kết quả kiểm thử trên nhiều bối cảnh giao thông khác nhau. |

---

# CHƯƠNG 4: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 4.1. Kết luận

Đề tài TrafficVision AI đã xây dựng được một ứng dụng desktop hỗ trợ nhận diện và thống kê phương tiện giao thông dựa trên mô hình YOLOv26. Hệ thống kết hợp các kỹ thuật xử lý ảnh truyền thống với mô hình học sâu, từ đó tạo thành một pipeline tương đối hoàn chỉnh cho bài toán nhận diện phương tiện trên ảnh và video.

Về mặt kỹ thuật, ứng dụng đã tích hợp các thư viện quan trọng như OpenCV, Ultralytics YOLO, PyQt6, QFluentWidgets, SQLite và PyQtGraph. Các chức năng chính gồm xử lý ảnh, nhận diện phương tiện, phân tích video, dashboard, analytics, history, export CSV và Arduino mock mode. Điều này cho thấy đề tài không chỉ tập trung vào mô hình mà còn chú ý đến trải nghiệm sử dụng và khả năng quản lý kết quả.

Tuy nhiên, để báo cáo trở thành bản hoàn chỉnh, nhóm cần bổ sung kết quả huấn luyện chính thức, số lượng dataset, ảnh chụp giao diện và hình minh họa kết quả nhận diện. Đây là các phần quan trọng để chứng minh hiệu quả thực nghiệm của mô hình.

## 4.2. Hạn chế

Hạn chế lớn nhất hiện tại là repository chưa chứa các file huấn luyện như `results.png`, `confusion_matrix.png`, `results.csv`, `args.yaml` hoặc file cấu hình dataset. Vì vậy, báo cáo chưa thể trình bày các chỉ số như mAP, precision, recall hoặc F1-score một cách chính thức. Ngoài ra, phần Arduino mới được cấu hình ở chế độ mock, chưa có bằng chứng kiểm thử với phần cứng thật trong repository.

Trong các cảnh giao thông đông, phương tiện bị che khuất hoặc có góc nhìn phức tạp, mô hình có thể bỏ sót hoặc nhận nhầm lớp phương tiện. Phần tracking video hiện đã có ByteTrack và BoT-SORT, nhưng vẫn cần kiểm thử thêm với nhiều video thực tế để đánh giá độ ổn định của Track ID và counting line.

## 4.3. Hướng phát triển

Trong các phiên bản tiếp theo, hệ thống có thể được cải thiện theo các hướng sau:

| Hướng phát triển | Mô tả |
| --- | --- |
| Improve detection in crowded scenes | Tăng dữ liệu và tối ưu mô hình để nhận diện tốt hơn trong cảnh đông xe, che khuất hoặc ánh sáng phức tạp |
| Add tracking | Hoàn thiện tracking, đếm xe qua line theo hướng di chuyển và tránh đếm trùng |
| Add license plate recognition | Kết hợp nhận diện biển số xe để tăng giá trị ứng dụng thực tế |
| Add real-time camera stream | Hỗ trợ camera IP, webcam hoặc RTSP để giám sát thời gian thực |
| Improve Arduino/IoT integration | Kiểm thử với Arduino thật, bổ sung IoT dashboard hoặc gửi dữ liệu lên server |
| Deploy as smart traffic monitoring system | Đóng gói hệ thống thành giải pháp giám sát giao thông thông minh có thể triển khai tại nút giao hoặc tuyến đường cụ thể |

---

# TÀI LIỆU THAM KHẢO

[1] Ultralytics, YOLO Documentation, hướng dẫn sử dụng mô hình YOLO cho detection và tracking.  
[2] OpenCV Documentation, tài liệu về xử lý ảnh, video processing và các hàm enhancement.  
[3] Rivero, M. et al., UA-DETRAC Dataset, bộ dữ liệu giao thông cho bài toán detection và tracking phương tiện.  
[4] PyQt6 Documentation, tài liệu xây dựng giao diện desktop bằng Qt cho Python.  
[5] QFluentWidgets Documentation, tài liệu component giao diện Fluent cho PyQt.  
[6] SQLite Documentation, tài liệu về cơ sở dữ liệu nhúng SQLite.  
[7] Arduino Documentation, tài liệu về Serial communication và điều khiển LED, LCD, buzzer.

---

# PHỤ LỤC

## Phụ lục A. Cấu trúc source code

```text
TrafficVision-AI/
├── main.py
├── README.md
├── requirements.txt
├── run.bat
├── test_video.mp4
├── legacy/
└── TrafficAIPro/
    ├── assets/
    │   └── backgrounds/
    ├── database/
    │   ├── history_repository.py
    │   ├── trafficai_history.sqlite3
    │   └── detected_images/
    ├── models/
    │   ├── detection.py
    │   └── weights/
    │       └── Car_YOLO26_Best.pt
    ├── pages/
    │   ├── dashboard.py
    │   ├── image_processing.py
    │   ├── detection.py
    │   ├── video_analysis.py
    │   ├── analytics.py
    │   ├── history.py
    │   └── project_information.py
    ├── services/
    │   ├── image_service.py
    │   ├── detection_service.py
    │   ├── arduino_service.py
    │   └── settings_service.py
    ├── ui/
    │   └── main_window.py
    ├── utils/
    └── widgets/
```

## Phụ lục B. Mã Arduino tham khảo

Repository hiện tại chưa có file `.ino`. Đoạn mã dưới đây là mã tham khảo để phần cứng Arduino đọc payload từ Python và điều khiển LED/buzzer. Khi dùng thực tế, nhóm cần kiểm tra lại chân kết nối, địa chỉ LCD I2C và tốc độ baud.

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int GREEN_LED = 8;
const int YELLOW_LED = 9;
const int RED_LED = 10;
const int BUZZER = 11;

void setup() {
  Serial.begin(9600);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("TrafficVision");
  lcd.setCursor(0, 1);
  lcd.print("Waiting data...");
}

void setLight(char level) {
  digitalWrite(GREEN_LED, level == 'G');
  digitalWrite(YELLOW_LED, level == 'Y');
  digitalWrite(RED_LED, level == 'R');
  digitalWrite(BUZZER, level == 'R');
}

void loop() {
  if (Serial.available()) {
    String payload = Serial.readStringUntil('\n');
    payload.trim();
    if (payload.length() == 0) return;

    char level = payload.charAt(0);
    setLight(level);

    int lastComma = payload.lastIndexOf(',');
    String total = lastComma >= 0 ? payload.substring(lastComma + 1) : "0";

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Level: ");
    lcd.print(level);
    lcd.setCursor(0, 1);
    lcd.print("Total: ");
    lcd.print(total);
  }
}
```

## Phụ lục C. Screenshots cần bổ sung

| Vị trí | Placeholder |
| --- | --- |
| Dashboard | [CHÈN ẢNH DASHBOARD] |
| Image Processing | [CHÈN ẢNH IMAGE PROCESSING] |
| Vehicle Detection | [CHÈN ẢNH VEHICLE DETECTION CÓ BOUNDING BOX] |
| Video Analysis | [CHÈN ẢNH VIDEO ANALYSIS] |
| Analytics | [CHÈN ẢNH ANALYTICS] |
| History | [CHÈN ẢNH HISTORY] |
| Project Information | [CHÈN ẢNH PROJECT INFORMATION] |
| Kết quả ảnh | [CHÈN ẢNH KẾT QUẢ NHẬN DIỆN TRÊN ẢNH] |
| Kết quả video | [CHÈN ẢNH KẾT QUẢ NHẬN DIỆN TRÊN VIDEO] |

## Phụ lục D. Training result files cần bổ sung

| Loại file | Placeholder |
| --- | --- |
| Biểu đồ training | [CHÈN RESULTS.PNG] |
| Confusion matrix | [CHÈN CONFUSION_MATRIX.PNG] |
| Precision-Recall curve | [CHÈN PRECISION-RECALL CURVE] |
| F1 curve | [CHÈN F1 CURVE] |
| Dataset split | [BỔ SUNG SỐ LƯỢNG ẢNH TRAIN/VALIDATION/TEST] |
| Cấu hình huấn luyện | [BỔ SUNG EPOCH], [BỔ SUNG BATCH SIZE], [BỔ SUNG IMAGE SIZE], [BỔ SUNG OPTIMIZER], [BỔ SUNG LEARNING RATE], [BỔ SUNG GPU/CPU SỬ DỤNG] |

## Phụ lục E. Tóm tắt thông tin kiểm tra từ repository

Thông tin đã tìm thấy trong repository:

| Nhóm thông tin | Kết quả kiểm tra |
| --- | --- |
| Tên dự án trong README | TrafficVision AI |
| Tên cửa sổ ứng dụng | TrafficAI Pro |
| Framework giao diện | PyQt6 và QFluentWidgets |
| Thư viện xử lý ảnh | OpenCV, NumPy, Pillow |
| Thư viện nhận diện | Ultralytics YOLO |
| Lớp phương tiện trong mã nguồn | `car`, `bus`, `truck`, `van` |
| Model weight | `TrafficAIPro/models/weights/Car_YOLO26_Best.pt` |
| Video mẫu | `test_video.mp4` |
| Database lịch sử | `TrafficAIPro/database/trafficai_history.sqlite3` |
| Số record SQLite khi kiểm tra | 32 record |
| Ảnh annotated runtime khi kiểm tra | 30 ảnh trong `TrafficAIPro/database/detected_images/` |
| Các màn hình đã triển khai | Dashboard, Image Processing, Vehicle Detection, Video Analysis, Analytics, History, Project Information |
| CSV export | Có trong `HistoryRepository.export_csv()` |
| Arduino service | Có, mặc định Mock mode, hỗ trợ Serial khi cấu hình cổng COM |

Thông tin chưa tìm thấy và cần bổ sung:

| Nhóm thông tin thiếu | Ghi chú |
| --- | --- |
| Dataset trong repository | Chưa thấy thư mục dataset, file `data.yaml` hoặc thống kê UA-DETRAC đã chuyển đổi |
| Chia tập train/validation/test | Cần bổ sung số lượng ảnh từng tập |
| Training logs | Chưa thấy `results.csv`, `args.yaml` hoặc thư mục `runs/train` |
| Training figures | Chưa thấy `results.png`, `confusion_matrix.png`, PR curve, F1 curve |
| Screenshots giao diện | Cần chụp và chèn vào các placeholder |
| Arduino sketch chính thức | Chưa thấy file `.ino`; phụ lục hiện chỉ có mã tham khảo |
| Kiểm thử phần cứng thật | Chưa có bằng chứng kết nối Arduino thật trong repository |
