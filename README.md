# INT3505E_01_demo – Flask Library


Chức năng:
- Quản lý sách (thêm/sửa/xoá, theo dõi tồn kho)
- Mượn/Trả sách (giảm/tăng tồn kho; không cho xoá sách đang mượn)


## Chạy nhanh
```bash
pip install -r requirements.txt
python seed.py
flask --app app run --debug