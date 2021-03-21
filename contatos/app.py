from flask import Flask
from flask import render_template, request, url_for, redirect, flash

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contatos.sqlite3"
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = "None"
app.secret_key = "None"
csrf = CSRFProtect()


class Contatos(db.Model):
    __tablename__ = "contatos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))

    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class FormContato(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    telefone = StringField('Telefone')


db.create_all()

@app.route("/")
def index():
    form = FormContato()
    contatos = Contatos.query.all()
    return render_template("index.html", form=form, contatos=contatos)

@app.route("/adicionar", methods=["POST"])
def addcontato():
    if request.method == "POST":
        addcontato = Contatos(request.form["nome"], request.form["telefone"])

        db.session.add(addcontato)
        db.session.commit()

        flash("Contato ADICIONADO!")
    
    return redirect(url_for("index"))

@app.route("/deletar/<int:id>", methods=["POST"])
def delcontato(id):
    if request.method == "POST":
        delcontato = Contatos.query.filter_by(id=id).first()

        db.session.delete(delcontato)
        db.session.commit()

        flash(f'Contato {delcontato.nome} REMOVIDO!')
    
    return redirect(url_for("index"))

@app.route("/atualizar/<int:id>")
def upcontato(id):
    form = FormContato()
    contato = Contatos.query.filter_by(id=id)

    return render_template("update.html", form=form, contato=contato)

@app.route("/atualizar/<int:id>", methods=["POST"])
def uptelefone(id):
    contato = Contatos.query.filter_by(id=id)

    novo = request.form["novotelefone"]
    update = Contatos.query.filter_by(id=id).update(dict(telefone=novo))

    db.session.commit()

    flash(f'Contato ATUALIZADO!')

    return redirect(url_for("index"))