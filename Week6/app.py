from flask import Flask, jsonify, request
import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# --- Load config ---
load_dotenv()
ACCESS_SECRET = os.getenv("ACCESS_SECRET", "access_secret_123")
REFRESH_SECRET = os.getenv("REFRESH_SECRET", "refresh_secret_123")

app = Flask(__name__)
CORS(app)

# --- Mock database ---
users = {
    "user1": {"password": "123", "role": "user", "scopes": ["read:books"]},
    "admin": {"password": "123", "role": "admin", "scopes": ["read:books", "write:books", "delete:books"]}
}

revoked_tokens = set()  # Mô phỏng token bị thu hồi

# --- Helper: Tạo JWT ---
def create_token(username, secret, exp_minutes, extra_data=None):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_minutes)
    }
    if extra_data:
        payload.update(extra_data)
    return jwt.encode(payload, secret, algorithm="HS256")

# --- Decorator xác thực ---
def token_required(required_scope=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", None)
            if not auth or not auth.startswith("Bearer "):
                return jsonify({"message": "Thiếu token"}), 401
            token = auth.split(" ")[1]
            if token in revoked_tokens:
                return jsonify({"message": "Token đã bị thu hồi"}), 403
            try:
                payload = jwt.decode(token, ACCESS_SECRET, algorithms=["HS256"])
                username = payload["sub"]
                user = users.get(username)
                if not user:
                    return jsonify({"message": "User không tồn tại"}), 401
                if required_scope and required_scope not in user["scopes"]:
                    return jsonify({"message": "Không có quyền truy cập"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token đã hết hạn"}), 403
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token không hợp lệ"}), 403
            return f(username, *args, **kwargs)
        return wrapper
    return decorator

# --- Đăng nhập ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"message": "Sai tên đăng nhập hoặc mật khẩu"}), 401

    access_token = create_token(username, ACCESS_SECRET, 1, {"role": user["role"], "scopes": user["scopes"]})
    refresh_token = create_token(username, REFRESH_SECRET, 5)
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    })

# --- Refresh token ---
@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.json
    refresh_token = data.get("refresh_token")
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
        username = payload["sub"]
        user = users.get(username)
        if not user:
            return jsonify({"message": "User không tồn tại"}), 401
        new_access = create_token(username, ACCESS_SECRET, 1, {"role": user["role"], "scopes": user["scopes"]})
        return jsonify({"access_token": new_access})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token đã hết hạn"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Refresh token không hợp lệ"}), 403

# --- API: lấy sách ---
@app.route("/books/<int:book_id>", methods=["GET"])
@token_required("read:books")
def get_book(username, book_id):
    return jsonify({"book_id": book_id, "title": "Clean Architecture", "by": username})

# --- API: thêm sách ---
@app.route("/books", methods=["POST"])
@token_required("write:books")
def add_book(username):
    return jsonify({"message": f"Sách mới được thêm bởi {username}"})

# --- API: xóa sách ---
@app.route("/books/<int:book_id>", methods=["DELETE"])
@token_required("delete:books")
def delete_book(username, book_id):
    return jsonify({"message": f"Sách {book_id} đã bị xóa bởi admin {username}"})

# --- Thu hồi token ---
@app.route("/logout", methods=["POST"])
def logout():
    token = request.json.get("token")
    if not token:
        return jsonify({"message": "Không có token để thu hồi"}), 400
    revoked_tokens.add(token)
    return jsonify({"message": "Token đã bị thu hồi thành công"})

# --- Phát hiện replay attack ---
@app.route("/secure-action", methods=["POST"])
def secure_action():
    auth = request.headers.get("Authorization", None)
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"message": "Thiếu token"}), 401
    token = auth.split(" ")[1]
    if token in revoked_tokens:
        return jsonify({"message": "Replay attack bị phát hiện!"}), 403
    return jsonify({"message": "Hành động an toàn được thực hiện!"})

# --- Swagger UI ---
SWAGGER_URL = "/docs"
API_URL = "/openapi.yaml"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "JWT Auth Demo"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def index():
    return jsonify({"message": "JWT Authentication Demo 🚀"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
