from flask import Flask, jsonify, request, make_response
import hashlib

app = Flask(__name__)

books = [
    {"id": 1, "title": "Flask Web Development", "author": "Miguel Grinberg"},
    {"id": 2, "title": "Effective Python", "author": "Brett Slatkin"},
]

def compute_etag(data):
    return hashlib.sha1(str(data).encode()).hexdigest()

@app.route("/api/books", methods=["GET"])
def get_books():
    etag = compute_etag(books)
    if request.headers.get("If-None-Match") == etag:
        return "", 304
    resp = make_response(jsonify(books))
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "public, max-age=60"
    return resp

@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()
    new = {"id": len(books)+1, **data}
    books.append(new)
    return jsonify(new), 201

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

if __name__ == "__main__":
    app.run(port=5002, debug=True)
