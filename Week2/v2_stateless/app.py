from flask import Flask, jsonify, request

app = Flask(__name__)

# Danh sách dữ liệu mẫu (in-memory, không có session)
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Fluent Python", "author": "Luciano Ramalho"},
    {"id": 3, "title": "Learning SQL", "author": "Alan Beaulieu"},
]

@app.route("/books")
def get_books():
    author = request.args.get("author")
    if author:
        result = [b for b in books if author.lower() in b["author"].lower()]
    else:
        result = books
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
