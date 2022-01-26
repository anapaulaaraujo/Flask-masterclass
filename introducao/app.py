from flask import Flask, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

#criando uma rota
@app.route("/")
def index():
    #retornar um link
    return "<a href='/posts'>Posts</a>"

@app.route("/redirect")
def redirect2():
    return redirect(url_for("response"))
    #o url_for ele redireciona o usuario dado o nome da rota e nao um caminho
    #entao se outra pessoa mudar o caminho a aplicacao nao quebra

@app.route("/response")
def response():
    return render_template("response.html")

@app.route("/posts")
@app.route("/posts/<int:id>")
def posts(id):
    titulo = request.args.get("titulo")

    data = dict(
        path=request.path,
        referrer=request.referrer,
        content_type=request.content_type,
        method=request.method,
        titulo=titulo,
        id=id if id else 0
    )
    
    return data


if __name__ == '__main__':
    app.run(debug=True) #para nao precisar sempre reiniciar o servidor