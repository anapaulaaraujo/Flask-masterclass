from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField
from wtforms.validators import Length, Email, DataRequired
from app.models import Book


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[
        Email()
    ])
    password = PasswordField("Senha", validators=[
        Length(3, 8, " O campo deve ter entre 3 a 8 caracteres")
    ])
    remember = BooleanField("Permanecer Conectado")
    submit = SubmitField("Logar")

class RegisterForm(FlaskForm):
    name = StringField("Nome Completo", validators=[
        DataRequired("O campo é obrigatório")
    ])
    email = EmailField("Email", validators=[
        Email()
    ])
    password = PasswordField("Senha", validators=[
        Length(3, 8, " O campo deve ter entre 3 a 8 caracteres")
    ])
    submit = SubmitField("Cadastrar")

class BookForm(FlaskForm):
    name = StringField("Nome do livro", validators=[
        DataRequired("O campo é obrigatório")
    ])
    submit = SubmitField("Salvar")

class UserBookForm(FlaskForm):
    book = SelectField("Livro", coerce=int)
    submit = SubmitField("Salvar")

    #ele vai ser chamado antes de qualquer verificação 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book.choices = [
            (book.id, book.name) for book in Book.query.all()
        ]