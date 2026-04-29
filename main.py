import json
from flask import Flask, render_template, request, redirect, flash, session

app = Flask(__name__)
app.secret_key = "123456"

usuarios = []

import os 

def salvar():
    caminho= os.path.abspath("usuarios.json")
    print("Salvando em:", caminho)

    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo)   

def carregar():
    global usuarios
    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)
    except:
        usuarios = []            

def cadastrar():
    nome = input("Digite o Nome: ")
    email = input("Digite o email: ")
    idade = input("Digite a idade: ")

    usuario = {
        "nome": nome,
        "email": email,
        "idade": idade

    }

    usuarios.append(usuario)
    salvar()
    print("Usuário cadastrado com sucesso! \n")


def listar():
    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado. \n")
    else:
        print("\n Lista de usuários: ")
        for i, usuario in enumerate(usuarios):
            print(f"{i} - {usuario['nome']} | {usuario['email']} | {usuario['idade']}")
        print()

def editar():
    listar()
    if len(usuarios) == 0:
        return

    indice = int(input("Digite o número do usuário que deseja editar: ")) 
    if indice < len(usuarios):
        nome =  input("Novo nome: ")
        email = input("Novo email: ")
        idade = input("Nova idade: ")

        usuarios[indice] = {
            "nome": nome,
            "email": email,
            "idade": idade

        }

        salvar()

        print("Usuário atualizado com sucesso! ")
    else:
        print("Índice inválido! \n ")    

def deletar():
    listar()
    if len(usuarios) == 0:
        return
    indice = int(input("Digite o número do usuário que deseja deletar: "))
    if indice < len(usuarios):
        usuarios.pop(indice)
        salvar()
        print("Usuário removido com sucesso! \n ")
    else:
        print("Índice inválido! \n ")    

def menu():
    while True:
        print("=== MENU ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuário")
        print("3 - Editar usuário")
        print("4 - Deletar usuário")
        print("5 - Sair")

        opcao = input("Escolha uma opção:")

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            editar()
        elif opcao == "4":
            deletar()
        elif opcao == "5":
            print("Encerrando sistema...")
            break       
        else:
            print("Opção inválida! \n")

carregar()
# menu()                

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "1234":
            session["logado"] = True

            return redirect("/")
        flash("Usuário ou senha inválidos", "erro")
        return redirect("/login")
    
    return render_template("login.html")
        
    flash("Usuário ou senha inválidos", "erro")
    return redirect("/login")

    return render_template("login.html")



@app.route("/")
def home():
    if not session.get("logado"):
        return redirect("/login")

    return render_template("index.html")

@app.route("/usuarios")
def usuarios_page():
    if not session.get("logado"):
        return redirect ("/login")
    
    carregar()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/cadastrar", methods=["POST"])
def cadastrar_web():
    carregar()

    nome = request.form["nome"]
    email = request.form["email"]
    idade = request.form["idade"]

    erro = None

    #validações
    if not nome or len(nome) < 3:
        erro = "Nome inválido (mínimo 3 letras)"
    if "@" not in email or "." not in email:
        erro = "Email inválido"
    if not idade.isdigit():
        erro = "Idade deve ser número" 
    
    if erro:
        return render_template("index.html", usuarios=usuarios, erro=erro)

    usuarios.append({
        "nome": nome,
        "email": email,
        "idade": idade
    })

    salvar()

    flash("Usuário cadastrado com sucesso!", "cadastro")
    return redirect("/")

@app.route("/editar/<int:indice>")
def editar_usuario(indice):
    carregar()
    usuario = usuarios[indice]
    return render_template("editar.html", usuario=usuario, indice=indice)

@app.route("/atualizar/<int:indice>", methods=["POST"])
def atualizar_usuarios(indice):
    carregar()

    usuarios[indice] = {
        "nome": request.form["nome"],
        "email": request.form["email"],
        "idade": request.form["idade"]
    }

    salvar()

    flash("Usuário atualizado com sucesso!", "editar")
    return redirect("/usuarios")

@app.route("/deletar/<int:indice>")
def deletar_web(indice):
    carregar()

    if indice < len(usuarios):
        usuarios.pop(indice)
        salvar()

    flash("Usuário deletado com sucesso!", "deletar")
    return redirect("/usuarios")    

@app.route("/logout")
def logout():
    session.pop("logado", None)
    flash("Logout realizado com sucesso!", "editar")
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
