from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, datetime

app = Flask(__name__)
CORS(app)
DB_FILE = "library.db"

# ----------------- Tiện ích -----------------
def _conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows

def count_db(query, args=()):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(query, args)
    n = cur.fetchone()[0]
    conn.close()
    return n

# ----------------- OFFSET PAGINATION -----------------
@app.route("/books_offset", methods=["GET"])
def books_offset():
    """Phân trang kiểu offset — có thể bị lỗi nếu dữ liệu thay đổi"""
    limit = request.args.get("limit", 5, type=int)
    offset = request.args.get("offset", 0, type=int)
    total = count_db("SELECT COUNT(*) FROM Book")

    rows = query_db("SELECT * FROM Book ORDER BY id DESC LIMIT ? OFFSET ?", [limit, offset])
    books = [dict(r) for r in rows]

    print(f"[OFFSET] offset={offset}, ids={[b['id'] for b in books]}")
    return jsonify({
        "mode": "offset",
        "limit": limit,
        "offset": offset,
        "total": total,
        "count": len(books),
        "data": books
    })

# ----------------- CURSOR PAGINATION -----------------
@app.route("/books_cursor", methods=["GET"])
def books_cursor():
    """Phân trang kiểu cursor — ổn định hơn khi dữ liệu thay đổi"""
    last_id = request.args.get("last_id", type=int)
    limit = request.args.get("limit", 5, type=int)

    query = "SELECT * FROM Book"
    params = []
    if last_id:
        query += " WHERE id < ?"
        params.append(last_id)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    rows = query_db(query, params)
    books = [dict(r) for r in rows]
    next_cursor = books[-1]["id"] if books else None

    print(f"[CURSOR] last_id={last_id}, ids={[b['id'] for b in books]}")
    return jsonify({
        "mode": "cursor",
        "limit": limit,
        "next_cursor": next_cursor,
        "count": len(books),
        "data": books
    })

# ----------------- Resource Tree: Member → Loans -----------------
@app.route("/members/<int:member_id>/loans", methods=["GET"])
def get_member_loans(member_id):
    limit = request.args.get("limit", 5, type=int)
    offset = request.args.get("offset", 0, type=int)

    total = count_db("SELECT COUNT(*) FROM Loan WHERE member_id = ?", [member_id])
    rows = query_db(
        "SELECT * FROM Loan WHERE member_id = ? ORDER BY id DESC LIMIT ? OFFSET ?",
        [member_id, limit, offset]
    )
    loans = [dict(r) for r in rows]
    return jsonify({
        "member_id": member_id,
        "limit": limit,
        "offset": offset,
        "total": total,
        "count": len(loans),
        "data": loans
    })

# ----------------- Mô phỏng thêm sách mới -----------------
@app.route("/simulate_add_book", methods=["POST"])
def simulate_add_book():
    conn = _conn()
    c = conn.cursor()
    c.execute("INSERT INTO Book (title, author, status) VALUES (?, ?, ?)",
              (f"NEW BOOK {datetime.datetime.now().strftime('%H:%M:%S')}",
               "Dynamic Author", "available"))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book added successfully"}), 201

# ----------------- Khởi tạo dữ liệu -----------------
def init_db():
    conn = _conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Book (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    category TEXT,
                    status TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Member (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Loan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    member_id INTEGER,
                    borrow_date TEXT,
                    return_date TEXT,
                    status TEXT,
                    FOREIGN KEY (book_id) REFERENCES Book(id),
                    FOREIGN KEY (member_id) REFERENCES Member(id)
                )''')
    conn.commit()
    conn.close()

def seed_data():
    conn = _conn()
    c = conn.cursor()
    c.execute("DELETE FROM Loan")
    c.execute("DELETE FROM Member")
    c.execute("DELETE FROM Book")

    # Thêm Book
    c.executemany("""
    INSERT INTO Book (title, author, category, status)
    VALUES (?, ?, ?, ?)
""", [
    ('Dế Mèn Phiêu Lưu Ký', 'Tô Hoài', 'Thiếu nhi', 'available'),
    ('O Chuột', 'Tô Hoài', 'Văn học', 'borrowed'),
    ('Harry Potter', 'J.K. Rowling', 'Fantasy', 'available'),
    ('1984', 'George Orwell', 'Dystopian', 'available'),
    ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'available'),
    ('Les Misérables', 'Victor Hugo', 'Classic', 'available'),
    ('The Little Prince', 'Antoine de Saint-Exupéry', 'Children', 'available')
])

    # Thêm Member
    c.executemany("""
        INSERT INTO Member (name, email) VALUES (?, ?)
    """, [
        ('Nguyễn Văn A', 'vana@example.com'),
        ('Trần Thị B', 'thib@example.com')
    ])

    # Thêm Loan
    c.executemany("""
        INSERT INTO Loan (book_id, member_id, borrow_date, status)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, '2025-10-01', 'returned'),
        (2, 1, '2025-10-05', 'borrowed'),
        (3, 2, '2025-10-10', 'borrowed')
    ])

    conn.commit()
    conn.close()

# ----------------- Run -----------------
if __name__ == "__main__":
    init_db()
    seed_data()
    app.run(debug=True)
