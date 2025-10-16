# 🌐 Buổi 3: Nguyên tắc Thiết kế API (RESTful Best Practices)

## 🎯 Mục tiêu học tập
- Hiểu và áp dụng 3 nguyên tắc chính:
  1. **Consistency** – Nhất quán trong naming & cấu trúc API  
  2. **Clarity** – Dễ hiểu, rõ ràng về chức năng của từng endpoint  
  3. **Extensibility** – Dễ mở rộng, hỗ trợ versioning  

- Áp dụng **naming convention**:  
  - Dùng danh từ số nhiều (plural nouns)  
  - Viết thường (`lowercase`) và dùng gạch nối (`-`)  
  - Có version trong URL (`/api/v1/...`)

---

## 🧩 Cấu trúc thư mục
Week3/
│
├── app.py # Flask API demo chuẩn RESTful
└── README.md # Hướng dẫn và case study

---

## 🚀 Cách chạy
1. Mở terminal tại thư mục `Week3`
2. Kích hoạt môi trường ảo (nếu có):  
   ```bash
   .venv\Scripts\activate
3. Chạy Flask app:

python app.py


4. Mở trình duyệt hoặc Postman tại:

http://127.0.0.1:5002/api/v1/users

5. Các Endpoint Chính

| Mục đích                 | Method | Endpoint             | Ghi chú                                           |
| ------------------------ | ------ | -------------------- | ------------------------------------------------- |
| Lấy danh sách người dùng | GET    | `/api/v1/users`      | Trả về toàn bộ users                              |
| Lấy chi tiết người dùng  | GET    | `/api/v1/users/<id>` | Ví dụ: `/api/v1/users/1`                          |
| Tạo người dùng mới       | POST   | `/api/v1/users`      | Gửi JSON body `{ "name": "...", "email": "..." }` |
| Lấy danh sách đơn hàng   | GET    | `/api/v1/orders`     | Đơn hàng demo có sẵn                              |
| API “xấu” để học         | GET    | `/getAllUserInfo`    | Ví dụ về thiết kế sai                             |

## Case Study: Phân tích API thiết kế kém
❌ API: /getAllUserInfo

Vấn đề:
-Dùng động từ “get” trong endpoint → không RESTful
-Dạng camelCase → không nhất quán
-Thiếu version /api/v1
-Không rõ resource chính là gì

Cách cải thiện:
✅ Nên viết lại: 
GET /api/v1/users
