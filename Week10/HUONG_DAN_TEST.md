# Hướng dẫn Test - Week 10: Security & Monitoring

## Tổng quan
Code demo này bao gồm 3 tính năng chính:
1. **Logging** - Ghi log vào file và console
2. **Monitoring** - Thu thập metrics với Prometheus
3. **Rate Limiting** - Giới hạn số request (5 request/phút)

---

## Bước 1: Khởi động server

```bash
uvicorn main:app --reload --port 3000
```

Server sẽ chạy tại: http://localhost:3000

---

## Bước 2: Test Rate Limiting

### Test 2.1: Gửi request bình thường
Mở terminal mới và chạy:

```bash
curl http://localhost:3000/hello
```

**Kết quả mong đợi:**
```json
{"message":"Hello Service Operation with Python!"}
```

### Test 2.2: Test giới hạn rate limit (5 request/phút)
Chạy lệnh này 6 lần liên tiếp:

```bash
curl http://localhost:3000/hello
curl http://localhost:3000/hello
curl http://localhost:3000/hello
curl http://localhost:3000/hello
curl http://localhost:3000/hello
curl http://localhost:3000/hello
```

**Kết quả mong đợi:**
- 5 request đầu: Thành công
- Request thứ 6: Bị chặn với lỗi `429 Too Many Requests`

```json
{"error":"Rate limit exceeded: 5 per 1 minute"}
```

### Test 2.3: Dùng PowerShell (Windows)
```powershell
for ($i=1; $i -le 6; $i++) {
    Write-Host "Request $i"
    Invoke-WebRequest -Uri http://localhost:3000/hello
}
```

---

## Bước 3: Test Logging

### Test 3.1: Kiểm tra log trong console
Khi bạn gửi request, terminal chạy server sẽ hiển thị log:

```
2024-11-27 10:30:15 - INFO - GET /hello 200
```

### Test 3.2: Kiểm tra log file
Mở file `app.log` trong folder Week10:

```bash
type app.log
```

**Kết quả mong đợi:** File chứa tất cả các request đã gửi:
```
2024-11-27 10:30:15 - INFO - GET /hello 200
2024-11-27 10:30:16 - INFO - GET /hello 200
2024-11-27 10:30:17 - INFO - GET /hello 429
```

---

## Bước 4: Test Monitoring (Prometheus Metrics)

### Test 4.1: Xem metrics
Truy cập endpoint metrics:

```bash
curl http://localhost:3000/metrics
```

Hoặc mở trình duyệt: http://localhost:3000/metrics

**Kết quả mong đợi:** Hiển thị metrics theo format Prometheus:

```
# HELP http_request_total Total HTTP requests
# TYPE http_request_total counter
http_request_total{endpoint="/hello",method="GET",status_code="200"} 5.0
http_request_total{endpoint="/hello",method="GET",status_code="429"} 1.0

# HELP http_request_latency_seconds Latency of HTTP requests
# TYPE http_request_latency_seconds histogram
http_request_latency_seconds_bucket{endpoint="/hello",le="0.005"} 3.0
http_request_latency_seconds_bucket{endpoint="/hello",le="0.01"} 5.0
http_request_latency_seconds_sum{endpoint="/hello"} 0.025
http_request_latency_seconds_count{endpoint="/hello"} 6.0
```

### Test 4.2: Phân tích metrics
- `http_request_total`: Đếm tổng số request theo method, endpoint, status code
- `http_request_latency_seconds`: Đo thời gian xử lý request (histogram)

---

## Bước 5: Test tổng hợp

### Script test tự động (PowerShell)

```powershell
# Test 1: Gửi 10 request và quan sát rate limit
Write-Host "=== Test Rate Limiting ===" -ForegroundColor Green
for ($i=1; $i -le 10; $i++) {
    Write-Host "Request $i" -NoNewline
    try {
        $response = Invoke-WebRequest -Uri http://localhost:3000/hello -ErrorAction Stop
        Write-Host " - OK (200)" -ForegroundColor Green
    } catch {
        Write-Host " - BLOCKED (429)" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 500
}

# Test 2: Kiểm tra metrics
Write-Host "`n=== Checking Metrics ===" -ForegroundColor Green
Invoke-WebRequest -Uri http://localhost:3000/metrics | Select-Object -ExpandProperty Content

# Test 3: Kiểm tra log file
Write-Host "`n=== Checking Logs ===" -ForegroundColor Green
Get-Content app.log -Tail 10
```

### Script test (Bash/Linux/Mac)

```bash
#!/bin/bash
echo "=== Test Rate Limiting ==="
for i in {1..10}; do
    echo -n "Request $i: "
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/hello
    sleep 0.5
done

echo -e "\n=== Checking Metrics ==="
curl -s http://localhost:3000/metrics | grep http_request

echo -e "\n=== Checking Logs ==="
tail -10 app.log
```

---

## Giải thích Code

### 1. Rate Limiting (`main.py`)
```python
app.state.limiter = Limiter(key_func=get_remote_address)
@app.get("/hello")
@app.state.limiter.limit("5/minute")  # Giới hạn 5 request/phút
```

### 2. Logging (`logging_config.py`)
```python
file_handler = logging.FileHandler("app.log")  # Ghi vào file
console_handler = logging.StreamHandler()      # Hiển thị console
```

### 3. Monitoring (`monitoring.py`)
```python
REQUEST_COUNT = Counter(...)      # Đếm số request
REQUEST_LATENCY = Histogram(...)  # Đo latency
```

---

## Kết quả mong đợi

✅ **Rate Limiting hoạt động:** Request thứ 6 trở đi bị chặn trong 1 phút  
✅ **Logging hoạt động:** Log xuất hiện trong console và file `app.log`  
✅ **Monitoring hoạt động:** Metrics hiển thị đầy đủ tại `/metrics`

---

## Troubleshooting

### Lỗi: Module not found
```bash
pip install fastapi uvicorn slowapi prometheus-client
```

### Lỗi: Port 3000 đã được sử dụng
```bash
uvicorn main:app --reload --port 8000
```

### Không thấy file app.log
- Kiểm tra bạn đang ở đúng folder Week10
- Gửi ít nhất 1 request để tạo file log

---

## Mở rộng

### Tích hợp Prometheus Server
1. Cài đặt Prometheus
2. Cấu hình `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['localhost:3000']
```
3. Truy cập Prometheus UI: http://localhost:9090

### Tích hợp Grafana
1. Kết nối Grafana với Prometheus
2. Tạo dashboard hiển thị metrics
3. Thiết lập alerts khi có quá nhiều 429 errors
