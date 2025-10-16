# 🟨 V3: + Cacheable + Uniform Interface

## 🧩 Nguyên tắc:
**Cacheable:** Cho phép client hoặc proxy cache phản hồi để tăng hiệu suất.  
**Uniform Interface:** Giao diện thống nhất với các phương thức chuẩn HTTP (GET, POST, PUT, DELETE).

---

## 💡 Đặc điểm:
- Dùng `ETag`, `Cache-Control` để giảm tải server  
- Tuân thủ URI và HTTP status code chuẩn  
- Giao tiếp qua `/api/books` theo quy tắc REST  

---

## ⚙️ Chạy & Test:
```bash
python app.py

# Lấy danh sách
curl "http://localhost:5002/api/books"

# Thêm mới (POST)
curl -X POST -H "Content-Type: application/json" \
-d '{"title":"Flask Web Development","author":"Miguel Grinberg"}' \
"http://localhost:5002/api/books"

# Cập nhật (PUT)
curl -X PUT -H "Content-Type: application/json" \
-d '{"title":"Flask Advanced","author":"Miguel Grinberg"}' \
"http://localhost:5002/api/books/1"

# Xóa (DELETE)
curl -X DELETE "http://localhost:5002/api/books/1"
