from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

book_in_users = db.Table("books_users",
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), nullable=False)
)

class User(db.Model, UserMixin): #herdando da classe pai db.model e UserMixin
   
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False) #igual ao VarChar (84) do MySQL
    email = db.Column(db.String(84), nullable=False, unique=True, index=True) #pq index=True?
    password = db.Column(db.String(255), nullable=False)
    #para relacionar com a tabela de profile
    profile = db.relationship('Profile', backref='user', uselist=False) #uselist=False significa que um usuario so pertence a um perfil
    books = db.relationship("Book", secondary=book_in_users, lazy=True, backref='users')

    #criando uma representacao para esse objeto, para toda vez que ele for instanciado
    #ele nao vir com user e endereço de memoria e sim o nome do user 
    def __str__(self):
        return self.name

class Profile(db.Model, UserMixin): #herdando da classe pai db.model
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Unicode(124), nullable=False) #igual ao VarChar (84) do MySQL
    #criando chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __str__(self):
        return self.name

class Book(db.Model, UserMixin): #herdando da classe pai db.model
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), nullable=False) #igual ao VarChar (84) do MySQL
    #criando chave estrangeira


    def __str__(self):
        return self.name