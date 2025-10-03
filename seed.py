from models import create_app, db, Book

app = create_app()

with app.app_context():
    if Book.query.count() == 0:
        samples = [
            ("Lập trình C++ cơ bản", "Nguyễn Văn A", 5),
            ("Cấu trúc dữ liệu & Giải thuật", "Nguyễn Văn B", 3),
            ("Mạng máy tính", "Kurose & Ross", 4),
        ]
        for title, author, qty in samples:
            db.session.add(Book(title=title, author=author, total_copies=qty, available_copies=qty))
        db.session.commit()
        print("Đã thêm dữ liệu mẫu")
    else:
        print("DB đã có dữ liệu")
