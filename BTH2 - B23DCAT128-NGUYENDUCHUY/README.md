# Bài Thực Hành 2 - Môn IoT và Ứng dụng
**Sinh viên:** Nguyễn Đức Huy  
**Mã SV:** B23DCAT128  

## Mô tả hệ thống
Đây là bài thực hành thu thập và xử lý dữ liệu cảm biến (Nhiệt độ, độ ẩm, ánh sáng). 
Luồng hoạt động của hệ thống:
1. Thiết bị ESP32 (mô phỏng trên Wokwi) đọc dữ liệu và gửi lên MQTT Broker.
2. Code Python nhận dữ liệu từ MQTT và lưu thô vào InfluxDB (Measurement: `sensor_data`).
3. Code Python tiền xử lý sẽ đọc dữ liệu thô, lọc nhiễu (outlier) bằng thuật toán IQR, tính trung bình trượt và lưu sang bảng sạch (Measurement: `sensor_processed`).
4. Hiển thị và so sánh dữ liệu theo thời gian thực trên Dashboard Grafana.

## Yêu cầu môi trường (Thư viện cần cài đặt)
Mở terminal/CMD và chạy lệnh sau để cài các thư viện cần thiết:
`pip install paho-mqtt influxdb-client pandas numpy`

## Hướng dẫn chạy thử nghiệm (Demo)
* **Bước 1:** Bật chạy mô phỏng mạch ESP32 trên Wokwi.
* **Bước 2:** Chạy lệnh `python nhan_du_lieu.py` để bắt đầu hứng dữ liệu đẩy vào InfluxDB.
bơm 60 phút dữ liệu có lẫn các điểm đột biến (nhiệt độ vọt lên 80 độ C).
* **Bước 3:** Chạy lệnh `python tien_xu_ly.py` để hệ thống làm mượt dữ liệu và loại bỏ các điểm đột biến.
* **Bước 4:** Bật Grafana, load lại Dashboard để xem thành quả ở ô biểu đồ `temp_rolling_mean`.