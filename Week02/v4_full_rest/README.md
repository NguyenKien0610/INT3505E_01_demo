# 🟥 V4: Full REST Architecture (All 6 Constraints)

## 🧩 Nguyên tắc:
Bao gồm toàn bộ 6 ràng buộc REST:
1. Client–Server  
2. Stateless  
3. Cacheable  
4. Uniform Interface  
5. Layered System  
6. Code-on-Demand  

---

## 💡 Đặc điểm:
- Có logging middleware (Layered System)  
- Có endpoint `/api/health` để giám sát hệ thống  
- Có HATEOAS links trong JSON trả về  
- Có cache header và ETag  
- Có hỗ trợ dynamic client script (Code-on-Demand)

---

## ⚙️ Chạy & Test:
```bash
python app.py

# Lấy danh sách
curl "http://localhost:5003/api/books"

# Thêm mới
curl -X POST -H "Content-Type: application/json" \
-d '{"title":"AI Toàn Tập","author":"Lê Hải Nam"}' \
"http://localhost:5003/api/books"

# Xem chi tiết
curl "http://localhost:5003/api/books/1"

# Xóa sách
curl -X DELETE "http://localhost:5003/api/books/1"

# Kiểm tra trạng thái hệ thống
curl "http://localhost:5003/api/health"
