# 📘 Buổi 4: API Specification & OpenAPI (Swagger)

## 🎯 Mục tiêu học tập
- Hiểu vai trò của **OpenAPI (Swagger)** trong việc tài liệu hóa API.  
- Viết và trình bày file **OpenAPI YAML** với các phần chính: `paths`, `components`, `schemas`, `parameters`.  
- Hiểu khái niệm **Stateless API** và cách áp dụng **JWT Authentication**.  
- Sử dụng Swagger UI để hiển thị và test tài liệu API.

---

## 🧩 Kiến thức trọng tâm

### 🔹 1. Stateless API
- Mỗi request là **độc lập**, không lưu trạng thái người dùng (session).  
- Thông tin xác thực được gửi kèm trong **JWT token** ở mỗi request.  
- Ưu điểm: dễ mở rộng (scalable), bảo mật, hoạt động tốt trên nhiều server.

### 🔹 2. JWT (JSON Web Token)
- Dạng token chứa thông tin người dùng, mã hóa bằng `JWT_SECRET_KEY`.  
- Server không lưu token — chỉ **xác minh chữ ký token** khi request đến.  
- Token được gửi trong Header:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```

### 🔹 3. OpenAPI (Swagger)
- Dạng file YAML mô tả toàn bộ API: endpoints, method, request body, response, authentication.  
- Giúp tự động tạo tài liệu và hỗ trợ test trực tiếp trên giao diện Swagger UI.

---

## 🚀 Cách chạy demo

### 1️⃣ Cài đặt môi trường
```bash
pip install flask flask-cors flask-jwt-extended
```

### 2️⃣ Chạy server Flask
```bash
python server.py
```
Server chạy tại:  
👉 `http://localhost:5000`

### 3️⃣ Mở Swagger UI
Truy cập: [https://editor.swagger.io](https://editor.swagger.io)

- Dán nội dung file `test.yaml` vào ô bên trái.  
- Swagger tự động render tài liệu và cho phép test các API.

---

## 🔐 Demo JWT Authentication

### Bước 1: Lấy token
**POST** `/api/login`
```json
{
  "username": "admin",
  "password": "123"
}
```
→ Nhận được token dạng:
```json
{ "token": "eyJhbGciOiJIUzI1NiIs..." }
```

### Bước 2: Authorize trong Swagger
- Nhấn nút **Authorize (🔒)**.  
- Dán token vào khung:  
  ```
  Bearer eyJhbGciOiJIUzI1NiIs...
  ```

### Bước 3: Gọi các API yêu cầu token
- `POST /api/books` – Thêm sách mới  
- `PUT /api/books/{id}` – Cập nhật thông tin  
- `DELETE /api/books/{id}` – Xóa sách  

Nếu không có token → Swagger sẽ trả về lỗi `401 Unauthorized`.

---

## 📘 Cấu trúc dự án

```
Week4/
│
├── server.py      # Flask REST API (có JWT)
├── test.yaml      # OpenAPI Specification (Swagger)
└── README.md      # Tài liệu hướng dẫn
```

---

## 🧠 Ghi chú
| Thành phần | Mô tả |
|-------------|--------|
| **Stateless** | API không lưu session, mỗi request tự mang token |
| **JWT** | Token xác thực người dùng, gửi qua header |
| **Swagger annotation** | `security: - BearerAuth: []` để đánh dấu endpoint cần token |
| **Swagger UI** | Cho phép hiển thị và test API trực tiếp từ file YAML |
| **CORS** | Cho phép Swagger (chạy ở port khác) truy cập server Flask |

---

## ✅ Kết quả đạt được
- [x] Hiểu cấu trúc OpenAPI YAML  
- [x] Viết tài liệu cho 5 endpoint CRUD  
- [x] Thêm JWT Authentication (Stateless API)  
- [x] Hiển thị tài liệu qua Swagger UI  
- [x] Annotation yêu cầu token đúng chuẩn OpenAPI  

