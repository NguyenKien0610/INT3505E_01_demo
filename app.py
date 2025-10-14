from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Book, Loan, create_app
from forms import BookForm, BorrowForm

app = create_app()


@app.route("/")
def index():
    books = Book.query.order_by(Book.title.asc()).all()
    recent_loans = Loan.query.order_by(Loan.borrowed_at.desc()).limit(10).all()
    return render_template("index.html", books=books, recent_loans=recent_loans)


# Books CRUD
@app.route("/books")
def list_books():
    # Lấy tham số từ query string
    search = request.args.get("q", "", type=str)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)

    # Câu truy vấn cơ bản
    query = Book.query.order_by(Book.title.asc())

    # Nếu có từ khóa tìm kiếm
    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) |
            (Book.author.ilike(f"%{search}%"))
        )

    # Phân trang
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    books = pagination.items
    total_pages = pagination.pages

    # Truyền kết quả xuống giao diện
    return render_template(
        "books.html",
        books=books,
        page=page,
        total_pages=total_pages,
        search=search
    )


@app.route("/books/new", methods=["GET", "POST"])
def create_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            total_copies=form.total_copies.data,
            available_copies=form.total_copies.data,
        )
        db.session.add(book)
        db.session.commit()
        flash("Đã thêm sách", "success")
        return redirect(url_for("list_books"))
    return render_template("book_form.html", form=form, mode="create")


@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        delta = form.total_copies.data - book.total_copies
        book.title = form.title.data
        book.author = form.author.data
        book.total_copies = form.total_copies.data
        book.available_copies = max(0, book.available_copies + delta)
        db.session.commit()
        flash("Đã cập nhật sách", "success")
        return redirect(url_for("list_books"))
    else:
     if request.method == "POST":
        print("Form errors:", form.errors)
    return render_template("book_form.html", form=form, mode="edit")


@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if Loan.query.filter_by(book_id=book.id, returned_at=None).count() > 0:
        flash("Không thể xoá: sách đang được mượn", "danger")
        return redirect(url_for("list_books"))
    db.session.delete(book)
    db.session.commit()
    flash("Đã xoá sách", "success")
    return redirect(url_for("list_books"))


# Borrow / Return
@app.route("/loans", methods=["GET", "POST"])
def loans():
    form = BorrowForm()
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        if not book:
            flash("Không tìm thấy sách", "danger")
        elif book.available_copies <= 0:
            flash("Hết sách để mượn", "warning")
        else:
            loan = Loan(book_id=book.id, borrower=form.borrower.data)
            book.available_copies -= 1
            db.session.add(loan)
            db.session.commit()
            flash("Mượn sách thành công", "success")
        return redirect(url_for("loans"))
    elif request.method == "POST":
        print("Form errors:", form.errors)

    active_loans = Loan.query.filter_by(returned_at=None).order_by(Loan.borrowed_at.desc()).all()
    return render_template("loans.html", form=form, active_loans=active_loans)


@app.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.returned_at is None:
        loan.returned_at = datetime.utcnow()
        book = Book.query.get(loan.book_id)
        book.available_copies = min(book.total_copies, book.available_copies + 1)
        db.session.commit()
        flash("Đã trả sách", "success")
    else:
        flash("Phiếu mượn đã được trả trước đó", "info")
    return redirect(url_for("loans"))


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/api/books")
def api_books():
    search = request.args.get("q", "", type=str)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)

    query = Book.query.order_by(Book.title.asc())
    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) |
            (Book.author.ilike(f"%{search}%"))
        )

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return {
        "page": pagination.page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
        "results": [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "genre": b.genre,
                "year": b.year
            } for b in pagination.items
        ]
    }


