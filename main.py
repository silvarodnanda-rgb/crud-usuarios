import os
import time
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
db = SQLAlchemy(app)

class Administrador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="visualizador")
    protegido = db.Column(db.Boolean, default=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    linkedin = db.Column(db.String(200), nullable=True)
    github = db.Column(db.String(200), nullable=True)
    protegido = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

    # Admin demo para testes
    if not Administrador.query.filter_by(usuario="admin").first():
        senha_hash = generate_password_hash("1234")
        admin = Administrador(usuario="admin", senha=senha_hash, role="admin")
        db.session.add(admin)
        db.session.commit()

    # Login pessoal
    if not Administrador.query.filter_by(usuario="fernanda").first():
        senha_hash = generate_password_hash(os.getenv("SENHA_FERNANDA"))
        eu = Administrador(usuario="fernanda", senha=senha_hash, role="admin", protegido=True)
        db.session.add(eu)
        db.session.commit()

    # Dados pessoais protegidos na lista
    if not Usuario.query.filter_by(email=os.getenv("MEU_EMAIL")).first():
        eu_usuario = Usuario(
            nome="Fernanda Rodrigues",
            email=os.getenv("MEU_EMAIL"),
            idade=22,
            linkedin="https://www.linkedin.com/in/nanda-rodrigu3s/",
            github="https://github.com/silvarodnanda-rgb",
            protegido=True
        )
        db.session.add(eu_usuario)
        db.session.commit()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Verifica bloqueio
        bloqueado_ate = session.get("bloqueado_ate")
        if bloqueado_ate:
            if time.time() < bloqueado_ate:
                segundos = int(bloqueado_ate - time.time())
                flash(f"Conta bloqueada! Tente novamente em {segundos} segundo(s).", "erro")
                return redirect("/login")
            else:
                session.pop("bloqueado_ate", None)
                session.pop("tentativas", None)

        usuario = request.form["usuario"]
        senha = request.form["senha"]
        admin = Administrador.query.filter_by(usuario=usuario).first()

        if admin and check_password_hash(admin.senha, senha):
            session["logado"] = True
            session["role"] = admin.role
            session.pop("tentativas", None)
            return redirect("/")

        # Conta tentativas
        tentativas = session.get("tentativas", 0) + 1
        session["tentativas"] = tentativas
        restam = 5 - tentativas

        if tentativas >= 5:
            session["bloqueado_ate"] = time.time() + 10
            flash("Conta bloqueada por 10 segundos!", "erro")
        else:
            unidade = "tentativa" if restam == 1 else "tentativas"
            flash(f"Usuário ou senha inválidos. Restam {restam} {unidade}.", "erro")

        return redirect("/login")

    return render_template("login.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if len(usuario) < 3:
            flash("Usuário deve ter no mínimo 3 caracteres!", "erro")
            return redirect("/registro")

        if len(senha) < 4:
            flash("Senha deve ter no mínimo 4 caracteres!", "erro")
            return redirect("/registro")

        if Administrador.query.filter_by(usuario=usuario).first():
            flash("Usuário já existe!", "erro")
            return redirect("/registro")

        senha_hash = generate_password_hash(senha)
        novo = Administrador(usuario=usuario, senha=senha_hash, role="visualizador")
        db.session.add(novo)
        db.session.commit()

        flash("Conta criada com sucesso! Faça login.", "cadastro")
        return redirect("/login")

    return render_template("registro.html")


@app.route("/")
def home():
    if not session.get("logado"):
        return redirect("/login")
    return render_template("index.html")


@app.route("/usuarios")
def usuarios_page():
    if not session.get("logado"):
        return redirect("/login")
    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/cadastrar", methods=["POST"])
def cadastrar_web():
    nome = request.form["nome"]
    email = request.form["email"]
    idade = request.form["idade"]

    erro = None

    if not nome or len(nome) < 3:
        erro = "Nome inválido (mínimo 3 letras)"
    elif "@" not in email or "." not in email:
        erro = "Email inválido"
    elif not idade.isdigit():
        erro = "Idade deve ser número"
    elif Usuario.query.filter_by(email=email).first():
        erro = "Email já cadastrado!"

    if erro:
        return render_template("index.html", erro=erro)

    novo_usuario = Usuario(nome=nome, email=email, idade=int(idade))
    db.session.add(novo_usuario)
    db.session.commit()

    flash("Usuário cadastrado com sucesso!", "cadastro")
    return redirect("/")


@app.route("/editar/<int:id>")
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("editar.html", usuario=usuario)


@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar_usuarios(id):
    if session.get("role") != "admin":
        flash("Acesso negado!", "erro")
        return redirect("/usuarios")

    usuario = Usuario.query.get_or_404(id)

    if usuario.protegido:
        flash("Este usuário não pode ser editado!", "erro")
        return redirect("/usuarios")

    usuario.nome = request.form["nome"]
    usuario.email = request.form["email"]
    usuario.idade = int(request.form["idade"])
    db.session.commit()

    flash("Usuário atualizado com sucesso!", "editar")
    return redirect("/usuarios")


@app.route("/deletar/<int:id>")
def deletar_web(id):
    if session.get("role") != "admin":
        flash("Acesso negado!", "erro")
        return redirect("/usuarios")

    usuario = Usuario.query.get_or_404(id)

    if usuario.protegido:
        flash("Este usuário não pode ser deletado!", "erro")
        return redirect("/usuarios")

    db.session.delete(usuario)
    db.session.commit()

    flash("Usuário deletado com sucesso!", "deletar")
    return redirect("/usuarios")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "editar")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)