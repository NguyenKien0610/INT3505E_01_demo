# Week 9: API Versioning và Lifecycle Management

## 📚 Nội dung bài học

### Kiến thức đạt được:
- ✅ Các chiến lược versioning: URL, header, query parameter
- ✅ Cách xử lý breaking changes và deprecation
- ✅ Lifecycle management cho API

### Kỹ năng thực hành:
- ✅ Triển khai versioning cho API (v1 → v2)
- ✅ Lập kế hoạch nâng cấp API (migration plan)
- ✅ Viết thông báo deprecation cho developers

## 🎯 Case Study: Payment API

Demo này mô phỏng việc nâng cấp một Payment API từ v1 sang v2 với các breaking changes:

### Breaking Changes từ V1 → V2:

| Feature | V1 (Deprecated) | V2 (Current) |
|---------|----------------|--------------|
| Amount validation | Không validate | Phải > 0 |
| Payment method | Không có (default: card) | Required field |
| Datetime format | ISO string | Datetime object |
| Idempotency | Không hỗ trợ | Có idempotency_key |
| Metadata | Không hỗ trợ | Có metadata field |

## 🚀 Cài đặt và Chạy

### 1. Cài đặt dependencies:
```bash
cd Week9
pip install -r requirements.txt
```

**Lưu ý:** Nếu bạn có nhiều Python installations và gặp lỗi `ModuleNotFoundError`, hãy dùng:
```bash
python -m pip install -r requirements.txt
```

### 2. Chạy server:
```bash
python app.py
```

**Nếu gặp lỗi `ModuleNotFoundError: No module named 'fastapi'`:**
```bash
# Tìm đường dẫn Python đã cài fastapi
where python

# Chạy với đường dẫn cụ thể (ví dụ):
C:\Users\Admin\AppData\Local\Programs\Python\Python313\python.exe app.py
```

Hoặc dùng uvicorn:
```bash
uvicorn app:app --reload
```

Server sẽ chạy tại: http://localhost:8000

### 3. Xem API Documentation:
Mở trình duyệt: http://localhost:8000/docs

## 🧪 Test API

### Cách 1: Sử dụng script test tự động
```bash
python test_api.py
```

### Cách 2: Test thủ công với curl

#### Test V1 (Deprecated):
```bash
# Tạo payment V1
curl -X POST http://localhost:8000/api/v1/payments \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 100, \"currency\": \"USD\", \"customer_id\": \"C001\"}"

# Get payment V1
curl http://localhost:8000/api/v1/payments/PAY_1001
```

#### Test V2 (Current):
```bash
# Tạo payment V2
curl -X POST http://localhost:8000/api/v2/payments \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 250.75, \"currency\": \"USD\", \"customer_id\": \"C002\", \"payment_method\": \"card\", \"metadata\": {\"order_id\": \"ORD123\"}}"

# Get payment V2
curl http://localhost:8000/api/v2/payments/PAY_1002

# List payments
curl http://localhost:8000/api/v2/payments?customer_id=C002
```

#### Test Idempotency:
```bash
# Gửi 2 lần với cùng idempotency_key
curl -X POST http://localhost:8000/api/v2/payments \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 99.99, \"currency\": \"USD\", \"customer_id\": \"C003\", \"payment_method\": \"e_wallet\", \"idempotency_key\": \"UNIQUE_KEY_123\"}"
```

#### Test Header Versioning:
```bash
# V1 qua header
curl -X POST http://localhost:8000/api/payments \
  -H "X-API-Version: 1" \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 150, \"customer_id\": \"C004\"}"

# V2 qua header
curl -X POST http://localhost:8000/api/payments \
  -H "X-API-Version: 2" \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 150, \"customer_id\": \"C004\"}"
```

#### Test Query Parameter Versioning:
```bash
# V1 qua query param
curl "http://localhost:8000/api/payments/PAY_1001/details?version=1"

# V2 qua query param
curl "http://localhost:8000/api/payments/PAY_1001/details?version=2"
```

### Cách 3: Test với Swagger UI
1. Mở http://localhost:8000/docs
2. Thử các endpoints trực tiếp trên giao diện

### Cách 4: Test với Postman
1. Import file `Week9_API_Versioning.postman_collection.json`
2. Đọc hướng dẫn chi tiết: **[POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)**
3. Chạy 23 test cases tự động

## 📋 Các Chiến lược Versioning

### 1. URL Path Versioning (✅ Recommended)
```
/api/v1/payments
/api/v2/payments
```
**Ưu điểm:**
- Rõ ràng, dễ hiểu
- Dễ cache và route
- Dễ deprecate từng version

**Nhược điểm:**
- URL dài hơn
- Phải maintain nhiều endpoints

### 2. Header Versioning
```
POST /api/payments
Header: X-API-Version: 2
```
**Ưu điểm:**
- URL clean
- Linh hoạt

**Nhược điểm:**
- Khó test với browser
- Khó cache
- Dễ quên set header

### 3. Query Parameter Versioning
```
/api/payments?version=2
```
**Ưu điểm:**
- Dễ test
- URL-based

**Nhược điểm:**
- Có thể conflict với query params khác
- Không semantic

## 📅 Deprecation Timeline

### Ví dụ trong demo:

| Ngày | Sự kiện |
|------|---------|
| 01/06/2025 | V1 được đánh dấu deprecated (có warnings) |
| 01/10/2025 | V1 chuyển sang read-only mode |
| 31/12/2025 | V1 bị loại bỏ hoàn toàn |

## 📢 Deprecation Notice

Xem thông báo deprecation đầy đủ:
```bash
curl http://localhost:8000/api/deprecation-notice
```

Thông tin bao gồm:
- Timeline chi tiết
- Breaking changes
- Migration guide
- Support contact

## 🔄 Migration Guide

### Bước 1: Đọc deprecation notice
```bash
curl http://localhost:8000/api/deprecation-notice
```

### Bước 2: Update code
```python
# V1 (Old)
{
    "amount": 100,
    "currency": "USD",
    "customer_id": "C001"
}

# V2 (New)
{
    "amount": 100,
    "currency": "USD",
    "customer_id": "C001",
    "payment_method": "card",  # ← Required
    "idempotency_key": "unique_key"  # ← Recommended
}
```

### Bước 3: Test với V2
```bash
# Test V2 endpoints
curl -X POST http://localhost:8000/api/v2/payments ...
```

### Bước 4: Deploy và monitor
- Deploy code mới
- Monitor logs
- Đảm bảo không còn calls đến V1

## 🎓 Bài tập thực hành

### Bài 1: Thêm V3
Thêm version 3 với feature mới:
- Hỗ trợ recurring payments
- Webhook notifications
- Refund support

### Bài 2: Implement Sunset Header
Thêm header `Sunset` cho V1:
```
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
```

### Bài 3: Version Negotiation
Implement content negotiation:
```
Accept: application/vnd.payment.v2+json
```

### Bài 4: Backward Compatibility Layer
Tạo adapter để V1 requests tự động convert sang V2.

## 📚 Tài liệu tham khảo

- [REST API Versioning Best Practices](https://restfulapi.net/versioning/)
- [Semantic Versioning](https://semver.org/)
- [API Deprecation Guidelines](https://www.rfc-editor.org/rfc/rfc8594.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 💡 Best Practices

1. **Luôn version API từ đầu** - Ngay cả v1
2. **Document breaking changes rõ ràng**
3. **Cho thời gian migration đủ dài** (3-6 tháng)
4. **Communicate sớm và thường xuyên**
5. **Maintain backward compatibility khi có thể**
6. **Use semantic versioning**
7. **Monitor usage của old versions**
8. **Provide migration tools/scripts**

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'fastapi':
```bash
# Kiểm tra Python nào đang được dùng
where python

# Cài đặt với Python cụ thể
python -m pip install -r requirements.txt

# Hoặc dùng đường dẫn đầy đủ
C:\Users\Admin\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```

### Server không start:
```bash
# Check port 8000 có bị chiếm không
netstat -ano | findstr :8000

# Thử port khác
uvicorn app:app --port 8001
```

### Import errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Test script lỗi:
```bash
# Đảm bảo server đang chạy
curl http://localhost:8000/

# Check Python version (cần >= 3.9)
python --version
```

## 📞 Liên hệ

Nếu có câu hỏi về demo này, hãy tạo issue hoặc liên hệ instructor.

---

**Happy Coding! 🚀**
