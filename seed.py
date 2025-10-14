from models import create_app, db, Book

app = create_app()

with app.app_context():
    print("🧹 Đang xoá dữ liệu cũ trong bảng Book...")
    Book.query.delete()
    db.session.commit()

    samples = [
        # Lập trình cơ bản
        ("Lập trình C++ cơ bản", "Nguyễn Văn A", "Lập trình", 2018, 5),
        ("Giải thuật và lập trình", "Lê Minh Hoàng", "Thuật toán", 2020, 6),
        ("Nhập môn Python", "Nguyễn Hồng Đức", "Lập trình", 2021, 4),
        ("Python nâng cao", "Trần Anh Tuấn", "Lập trình", 2022, 3),
        ("Java từ cơ bản đến nâng cao", "Phạm Quang Huy", "Lập trình", 2020, 4),

        # Web & Backend
        ("Flask Web Development", "Miguel Grinberg", "Web Backend", 2018, 5),
        ("Django for APIs", "William S. Vincent", "Web Backend", 2020, 3),
        ("Thiết kế RESTful API", "Nguyễn Thị Lan", "Kiến trúc phần mềm", 2023, 4),
        ("Node.js cơ bản", "Trần Văn Long", "Web Backend", 2019, 5),
        ("Kiến trúc hướng dịch vụ - SOA", "Nguyễn Đức Khoa", "Kiến trúc phần mềm", 2022, 3),

        # Mạng & hệ thống
        ("Mạng máy tính", "Kurose & Ross", "Mạng máy tính", 2021, 4),
        ("Hệ điều hành", "Abraham Silberschatz", "Hệ thống", 2019, 3),
        ("Kiến trúc máy tính", "David Patterson", "Hệ thống", 2020, 3),
        ("Bảo mật mạng máy tính", "Nguyễn Mạnh Hùng", "Mạng máy tính", 2022, 2),

        # Cơ sở dữ liệu
        ("Cơ sở dữ liệu MySQL", "Trần Văn Phúc", "Cơ sở dữ liệu", 2018, 4),
        ("PostgreSQL nâng cao", "Phạm Minh Tuấn", "Cơ sở dữ liệu", 2020, 3),
        ("Quản trị hệ quản trị cơ sở dữ liệu", "Nguyễn Thanh Huyền", "Cơ sở dữ liệu", 2023, 4),

        # Trí tuệ nhân tạo & Khoa học dữ liệu
        ("Machine Learning cơ bản", "Andrew Ng", "Trí tuệ nhân tạo", 2017, 5),
        ("Deep Learning with Python", "François Chollet", "Trí tuệ nhân tạo", 2018, 3),
        ("AI toàn tập", "Lê Hải Nam", "Trí tuệ nhân tạo", 2023, 4),
        ("Phân tích dữ liệu với Pandas", "Wes McKinney", "Khoa học dữ liệu", 2021, 3),
        ("Thống kê ứng dụng cho khoa học dữ liệu", "Nguyễn Hoàng", "Khoa học dữ liệu", 2020, 4),
    ]

    for title, author, genre, year, qty in samples:
        db.session.add(
            Book(
                title=title,
                author=author,
                genre=genre,
                year=year,
                total_copies=qty,
                available_copies=qty
            )
        )

    db.session.commit()
    print(f"✅ Đã thêm {len(samples)} sách mẫu mới vào cơ sở dữ liệu!")
