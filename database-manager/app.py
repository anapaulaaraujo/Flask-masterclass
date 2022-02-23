from flask import Flask, render_template, redirect, request, url_for, flash
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#suprir o erro que nao tinha banco de dados associado
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
#warning sobre track modifications
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'secret'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin): #herdando da classe pai db.model e UserMixin
   
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False) #igual ao VarChar (84) do MySQL
    email = db.Column(db.String(84), nullable=False, unique=True, index=True) #pq index=True?
    password = db.Column(db.String(255), nullable=False)
    #para relacionar com a tabela de profile
    profile = db.relationship('Profile', backref='user', uselist=False) #uselist=False significa que um usuario so pertence a um perfil

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

@app.route("/")
def index():
    users = User.query.all() #Igual ao Select * from users;
    return render_template("users.html", users=users)

@app.route("/user/<int:id>")
@login_required
def unique(id):
    #get da no mesmo que filter_by, mas é melhor para pegar id
    user = User.query.get(id)
    return render_template("user.html", user=user)


@app.route("/user/delete/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User()
        user.name = request.form["name"]
        user.email = request.form["email"]
        user.password = generate_password_hash(request.form["password"])

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("index"))
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()


        if not user:
            flash("Credencias Inválidas")
            return redirect(url_for("login"))

        if not check_password_hash(user.password, password):
            flash("Credencias Inválidas")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("index"))


    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)