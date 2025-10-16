from flask import Flask, jsonify

app = Flask(__name__)

# Dữ liệu giả lập
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Design Patterns", "author": "Erich Gamma"},
]

@app.route("/books")
def get_books():
    return jsonify(books)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
