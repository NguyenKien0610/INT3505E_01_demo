from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class BookForm(FlaskForm):
    title = StringField("Tên sách", validators=[DataRequired()])
    author = StringField("Tác giả", validators=[DataRequired()])
    total_copies = IntegerField("Số lượng", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Lưu")


class BorrowForm(FlaskForm):
    book_id = IntegerField("ID sách", validators=[DataRequired(), NumberRange(min=1)])
    borrower = StringField("Người mượn", validators=[DataRequired()])
    submit = SubmitField("Mượn")