# Kết quả Test - Week 10: Security & Monitoring

## ✅ Tất cả các tính năng hoạt động chính xác!

---

## 1. Rate Limiting ✅

**Cấu hình:** 5 requests/phút

**Kết quả test:**
- Request 1-5: ✅ Thành công (200 OK)
- Request 6-8: ❌ Bị chặn (429 Too Many Requests)

**Log từ server:**
```
2025-11-27 14:18:39,652 - INFO - GET /hello 200
2025-11-27 14:18:39,886 - INFO - GET /hello 200
2025-11-27 14:18:40,116 - INFO - GET /hello 200
2025-11-27 14:18:40,335 - INFO - GET /hello 200
2025-11-27 14:18:40,552 - INFO - GET /hello 429  ← Bắt đầu bị chặn
2025-11-27 14:18:40,769 - INFO - GET /hello 429
2025-11-27 14:18:40,986 - INFO - GET /hello 429
2025-11-27 14:18:41,205 - INFO - GET /hello 429
```

**Kết luận:** Rate limiting hoạt động chính xác theo cấu hình.

---

## 2. Monitoring (Prometheus Metrics) ✅

**Endpoint:** http://127.0.0.1:3000/metrics

**Metrics thu thập được:**

### Request Counter
```
http_request_total{endpoint="/hello",method="GET",status_code="200"} 5.0
http_request_total{endpoint="/hello",method="GET",status_code="429"} 4.0
```

### Request Latency (Histogram)
```
http_request_latency_seconds_count{endpoint="/hello"} 9.0
http_request_latency_seconds_sum{endpoint="/hello"} 0.012279
```

**Phân tích:**
- Tổng 9 requests đã được ghi nhận
- 5 requests thành công (200)
- 4 requests bị chặn (429)
- Latency trung bình: ~1.36ms (rất nhanh!)

**Kết luận:** Monitoring hoạt động tốt, metrics chính xác.

---

## 3. Logging ✅

**File log:** `app.log`

**Nội dung log:**
```
2025-11-27 14:18:29,022 - INFO - GET /hello 200
2025-11-27 14:18:39,652 - INFO - GET /hello 200
2025-11-27 14:18:39,886 - INFO - GET /hello 200
2025-11-27 14:18:40,116 - INFO - GET /hello 200
2025-11-27 14:18:40,335 - INFO - GET /hello 200
2025-11-27 14:18:40,552 - INFO - GET /hello 429
2025-11-27 14:18:40,769 - INFO - GET /hello 429
2025-11-27 14:18:40,986 - INFO - GET /hello 429
2025-11-27 14:18:41,205 - INFO - GET /hello 429
2025-11-27 14:18:54,638 - INFO - GET /metrics 200
```

**Tính năng:**
- ✅ Ghi log vào file `app.log`
- ✅ Hiển thị log trên console
- ✅ Format: timestamp - level - message
- ✅ Ghi nhận cả request thành công và bị chặn

**Kết luận:** Logging hoạt động đầy đủ.

---

## Cách chạy test

### 1. Khởi động server
```bash
cd Week10
uvicorn main:app --reload --port 3000
```

### 2. Test thủ công

**Test rate limiting:**
```bash
for ($i=1; $i -le 8; $i++) { 
    Write-Host "Request $i"; 
    curl http://127.0.0.1:3000/hello; 
    Start-Sleep -Milliseconds 200 
}
```

**Xem metrics:**
```bash
curl http://127.0.0.1:3000/metrics
```

**Xem log:**
```bash
Get-Content app.log -Tail 15
```

---

## Kiến thức đạt được

### 1. Security
- ✅ Rate Limiting: Bảo vệ API khỏi abuse/DDoS
- ✅ Giới hạn 5 requests/phút cho mỗi IP
- ✅ Trả về HTTP 429 khi vượt giới hạn

### 2. Monitoring
- ✅ Thu thập metrics với Prometheus
- ✅ Đếm số lượng requests theo endpoint, method, status code
- ✅ Đo latency của từng request (histogram)
- ✅ Metrics có thể tích hợp với Grafana để visualize

### 3. Logging
- ✅ Ghi log structured với timestamp
- ✅ Log vào cả file và console
- ✅ Theo dõi tất cả requests (audit trail)
- ✅ Hỗ trợ debugging và troubleshooting

---

## Mở rộng

### Tích hợp Prometheus + Grafana

1. **Cài đặt Prometheus:**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['localhost:3000']
```

2. **Chạy Prometheus:**
```bash
prometheus --config.file=prometheus.yml
```

3. **Truy cập:**
- Prometheus UI: http://localhost:9090
- Query metrics: `http_request_total`

4. **Tích hợp Grafana:**
- Add Prometheus data source
- Tạo dashboard với các panels:
  - Request rate (requests/second)
  - Error rate (429 errors)
  - Latency percentiles (p50, p95, p99)
  - Request distribution by endpoint

---

## Tổng kết

✅ **Rate Limiting:** Hoạt động chính xác  
✅ **Monitoring:** Metrics đầy đủ và chính xác  
✅ **Logging:** Ghi log đầy đủ vào file và console  

Code demo đã thực hiện đầy đủ các yêu cầu của bài học Week 10!
