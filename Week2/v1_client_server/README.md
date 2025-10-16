# 🟦 V1: Client–Server

## 🧩 Nguyên tắc:
**Client–Server:** Tách biệt vai trò giữa Client và Server.  
- Client xử lý giao diện (UI) và tương tác người dùng  
- Server xử lý logic nghiệp vụ và dữ liệu  
- Giao tiếp qua HTTP request–response  

---

## 💡 Đặc điểm:
- Tách biệt lớp giao diện và xử lý dữ liệu  
- Thay đổi Client không ảnh hưởng Server  
- Dễ mở rộng và bảo trì  

---

## ⚙️ Chạy & Test:
```bash
# Chạy server Flask
python app.py

# Gửi request kiểm tra
curl "http://localhost:5000/books"
