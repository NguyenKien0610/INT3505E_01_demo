from flask import Flask, jsonify, request, make_response, url_for
import hashlib, time

app = Flask(__name__)

books = [
    {"id": 1, "title": "Deep Learning with Python", "author": "François Chollet"},
    {"id": 2, "title": "AI Toàn Tập", "author": "Lê Hải Nam"},
]

def compute_etag(data):
    return hashlib.sha1(str(data).encode()).hexdigest()

@app.before_request
def log_request():
    print(f"[{time.strftime('%H:%M:%S')}] {request.method} {request.path}")

@app.route("/api/books", methods=["GET"])
def get_books():
    etag = compute_etag(books)
    if request.headers.get("If-None-Match") == etag:
        return "", 304
    resp = make_response(jsonify({
        "data": books,
        "links": {
            "self": url_for("get_books"),
            "add": url_for("add_book")
        }
    }))
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "public, max-age=120"
    return resp

@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()
    new = {"id": len(books)+1, **data}
    books.append(new)
    resp = make_response(jsonify(new), 201)
    resp.headers["Location"] = url_for("get_book", book_id=new["id"])
    return resp

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    for b in books:
        if b["id"] == book_id:
            b["links"] = {"self": url_for("get_book", book_id=book_id)}
            return jsonify(b)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    for b in books:
        if b["id"] == book_id:
            b.update(data)
            return jsonify(b)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return "", 204

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "time": time.strftime("%H:%M:%S")})

if __name__ == "__main__":
    app.run(port=5003, debug=True)
