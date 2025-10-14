from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from datetime import datetime

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = "dev-secret-change-me"

    # ensure instance/ exists
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{instance_path / 'library.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(100))               # 🆕 thêm thể loại
    year = db.Column(db.Integer)                    # 🆕 thêm năm xuất bản
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)

    def __repr__(self) -> str:
        return f"<Book {self.title} ({self.available_copies}/{self.total_copies})>"


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    borrower = db.Column(db.String(120), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)

    book = db.relationship("Book", backref="loans")

    def __repr__(self) -> str:
        return f"<Loan book={self.book_id} borrower={self.borrower}>"
