from flask import Flask, jsonify, request

app = Flask(__name__)

# Dữ liệu giả lập (mock data)
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

orders = [
    {"id": 101, "user_id": 1, "total": 59.99},
    {"id": 102, "user_id": 2, "total": 24.50},
]

# ----------------------------
# ✅ 1. Consistency: dùng danh từ số nhiều (plural nouns)
# ✅ 2. Clarity: rõ ràng, mỗi endpoint chỉ làm một nhiệm vụ
# ✅ 3. Extensibility: dễ thêm version / module sau này
# ----------------------------

# GET /api/v1/users
@app.route("/api/v1/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# GET /api/v1/users/<id>
@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# GET /api/v1/orders
@app.route("/api/v1/orders", methods=["GET"])
def get_orders():
    return jsonify(orders), 200

# POST /api/v1/users
@app.route("/api/v1/users", methods=["POST"])
def create_user():
    new_user = request.get_json()
    new_user["id"] = len(users) + 1
    users.append(new_user)
    return jsonify(new_user), 201

# ----------------------------
# Ví dụ API poorly designed (để case study)
# ----------------------------
@app.route("/getAllUserInfo", methods=["GET"])
def bad_api_example():
    """❌ Ví dụ sai:
    - Không dùng danh từ số nhiều
    - Dính camelCase
    - Không có versioning
    """
    return jsonify({"message": "This is a bad API example"}), 200


if __name__ == "__main__":
    app.run(port=5002, debug=True)
