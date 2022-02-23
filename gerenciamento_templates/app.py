from flask import Flask, render_template, flash
from datetime import datetime
from filtros import format_date


app = Flask(__name__, 
template_folder="temas",
static_folder="public")
app.config["SECRET_KEY"] = "secret"

app.jinja_env.filters["formatdate"] = format_date

@app.route("/templates")
def templates():

    flash("Usuario criado com sucesso")

    user_page = True

    return render_template("index.html", user_page=user_page)

@app.route("/users/1")
def users():

    users = [{
        "name":"Marcus Pereira",
        "age": 99 ,
        "email": "oi@spacedevs.com.br",
        "active": True,
        "since": datetime.utcnow()
    }, 
    {
        "name":"amanda silva",
        "age": 28 ,
        "email": "amanda@spacedevs.com.br",
        "active": False,
         "since": datetime.utcnow()
    }]
    
    flash(message="Users routes", category="warning")
    return render_template("users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)