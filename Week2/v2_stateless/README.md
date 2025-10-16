# 🟩 V2: Client–Server + Stateless

## 🧩 Nguyên tắc:
**Stateless:** Mỗi request là độc lập, server không lưu session state.  
Tất cả thông tin cần thiết phải được gửi kèm trong request.

---

## 💡 Đặc điểm:
- Không lưu trạng thái người dùng  
- Dễ mở rộng và phân tán  
- Dễ debug và test API độc lập  

---

## ⚙️ Chạy & Test:
```bash
# Chạy server Flask
python app.py

# Lấy tất cả sách
curl "http://localhost:5001/books"

# Lọc theo tác giả (query param)
curl "http://localhost:5001/books?author=Robert"
