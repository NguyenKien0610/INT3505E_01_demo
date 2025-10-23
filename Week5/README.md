# 🏛️ Buổi 5: Data Modeling và Resource Design

## 🎯 Mục tiêu buổi học
Trong buổi này, sinh viên cần hiểu và thực hành các nội dung sau:
- Thiết kế **data model** phù hợp với domain (Library Management System)
- Thiết kế **resource tree** RESTful
- So sánh và minh họa hai chiến lược **pagination**: `offset-based` và `cursor-based`

---

## 🧩 1. Cấu trúc dữ liệu (Data Modeling)
Hệ thống mô phỏng gồm 3 thực thể chính:

| Bảng | Mô tả | Các cột chính |
|------|--------|----------------|
| **Book** | Sách trong thư viện | `id`, `title`, `author`, `status` |
| **Member** | Thành viên mượn sách | `id`, `name`, `email` |
| **Loan** | Phiếu mượn sách | `id`, `book_id`, `member_id`, `borrow_date`, `status` |

Mối quan hệ:  
- `Loan` **tham chiếu** đến `Book` và `Member`  
- Một `Member` có thể có nhiều `Loan`

---

## 🌐 2. Resource Tree Design (RESTful)
Thiết kế URL RESTful thể hiện mối quan hệ dữ liệu:

| Endpoint | Mô tả |
|-----------|--------|
| `/books_offset` | Danh sách sách (offset pagination) |
| `/books_cursor` | Danh sách sách (cursor pagination) |
| `/members/{id}/loans` | Danh sách phiếu mượn của thành viên |
| `/simulate_add_book` | Thêm sách mới (mô phỏng dữ liệu động) |

---

## ⚙️ 3. Phân trang (Pagination Strategies)

### 🧱 Offset-based Pagination
- Dễ triển khai, dùng `limit` và `offset`.
- Dễ **trượt dữ liệu** khi có bản ghi mới được thêm vào.
- Ví dụ:
  ```
  GET /books_offset?limit=5&offset=0
  → Thêm sách mới
  GET /books_offset?limit=5&offset=5
  → Dữ liệu bị lệch
  ```

### 🧭 Cursor-based Pagination
- Sử dụng `id` hoặc `timestamp` làm con trỏ.
- Ổn định, không bị trượt khi thêm dữ liệu mới.
- Ví dụ:
  ```
  GET /books_cursor?limit=5
  GET /books_cursor?limit=5&last_id=<next_cursor>
  ```

---

## 🚀 4. Cách chạy demo

1. **Khởi động server**
   ```bash
   python app.py
   ```

2. **Mở Swagger UI** (hoặc dùng Postman)

3. **Thực hiện các bước sau để chứng minh lỗi offset:**
   1. Gọi: `GET /books_offset?limit=3&offset=0`
   2. Gọi: `POST /simulate_add_book`
   3. Gọi lại: `GET /books_offset?limit=3&offset=3`
   → Thấy ID sách bị lệch hoặc lặp

4. **So sánh với cursor:**
   1. `GET /books_cursor?limit=3`
   2. `GET /books_cursor?limit=3&last_id=<next_cursor>`
   → Dữ liệu vẫn ổn định

5. **Demo resource tree:**
   ```
   GET /members/1/loans
   ```

---

## 🧠 5. Kết luận
| Chiến lược | Ưu điểm | Nhược điểm |
|-------------|----------|------------|
| Offset-based | Dễ hiểu, dễ triển khai | Không ổn định khi dữ liệu động |
| Cursor-based | Ổn định, hiệu suất tốt | Phức tạp hơn khi triển khai |

**=> Trong thực tế, các hệ thống lớn như Facebook, Twitter, Spotify đều dùng Cursor-based pagination.**

