from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
CORS(app)  # Cho phép Swagger UI (chạy khác port) gọi được API này
app.config["JWT_SECRET_KEY"] = "secret-key-demo"
jwt = JWTManager(app)

# Cơ sở dữ liệu mẫu
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999},
    {"id": 3, "title": "Refactoring", "author": "Martin Fowler", "year": 1999}
]

# -------------------------------
# Đăng nhập để lấy JWT Token
# -------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == "admin" and password == "123":
        token = create_access_token(identity=username)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Sai thông tin đăng nhập"}), 401

# -------------------------------
# Lấy danh sách tất cả sách
# -------------------------------
@app.route('/api/books', methods=['GET'])
def get_books():
    author = request.args.get('author')
    limit = int(request.args.get('limit', 10))
    books = BOOKS
    if author:
        books = [b for b in books if author.lower() in b['author'].lower()]
    return jsonify(books[:limit])

# -------------------------------
# Lấy thông tin sách theo ID
# -------------------------------
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    for book in BOOKS:
        if book['id'] == id:
            return jsonify(book)
    return jsonify({"message": "Không tìm thấy"}), 404

# -------------------------------
# Thêm sách mới (Yêu cầu JWT)
# -------------------------------
@app.route('/api/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.json
    new_book = {
        "id": len(BOOKS) + 1,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"]
    }
    BOOKS.append(new_book)
    return jsonify(new_book), 201

# -------------------------------
# Cập nhật thông tin sách (Yêu cầu JWT)
# -------------------------------
@app.route('/api/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    data = request.json
    for book in BOOKS:
        if book['id'] == id:
            book.update(data)
            return jsonify(book)
    return jsonify({"message": "Không tìm thấy"}), 404

# -------------------------------
# Xóa sách (Yêu cầu JWT)
# -------------------------------
@app.route('/api/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    global BOOKS
    BOOKS = [b for b in BOOKS if b['id'] != id]
    return '', 204

# -------------------------------
# Chạy server
# -------------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)
