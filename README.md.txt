# 🗂️ Sistema de Cadastro de Usuários

Projeto desenvolvido com o objetivo de praticar e consolidar conhecimentos em desenvolvimento web com Python, passando por diferentes etapas de evolução: desde um CRUD simples com armazenamento em JSON até um sistema completo com banco de dados, autenticação segura e controle de acesso.

Mais do que um projeto técnico, esse sistema representa minha jornada de aprendizado — cada funcionalidade foi implementada com intenção, buscando simular o que encontraria em um ambiente profissional real.

---

## 🚀 Funcionalidades

- *Autenticação completa* — login, logout e registro de novos usuários
- *Níveis de acesso* — perfil admin (acesso total) e visualizador (somente leitura)
- *Bloqueio por tentativas* — conta bloqueada após 5 erros consecutivos, com contagem regressiva
- *CRUD de usuários* — cadastrar, listar, editar e deletar
- *Validação de dados* — email duplicado, campos obrigatórios e formato de idade
- *Dados protegidos* — perfil pessoal da desenvolvedora não pode ser editado ou deletado
- *Variáveis de ambiente* — informações sensíveis protegidas via .env
- *Interface responsiva* — dark mode com tema roxo

---

## 🛠️ Tecnologias utilizadas

- *Python* — linguagem principal
- *Flask* — framework web
- *Flask-SQLAlchemy* — ORM para banco de dados
- *SQLite* — banco de dados relacional
- *Werkzeug* — criptografia de senhas
- *Python-dotenv* — gerenciamento de variáveis de ambiente
- *HTML & CSS* — interface do usuário

---

## 🔐 Perfis de acesso para teste

| Perfil | Usuário | Senha |
|--------|---------|-------|
| Administrador | admin | 1234 |
| Visualizador | Crie sua conta! | — |

---

## ⚙️ Como executar localmente

1. Clone o repositório:
```bash
git clone https://github.com/silvarodnanda-rgb/crud-usuarios.git

2. Instale as dependências:
pip install flask flask-sqlalchemy werkzeug python-dotenv

3. Crie um arquivo .env na raiz do projeto:
SECRET_KEY=sua_chave_secreta
SENHA_FERNANDA=sua_senha
MEU_EMAIL=seu@email.com

4. Execute o projeto:
python main.py
Acesse no navegador: http://127.0.0.1:5000

## 📈 Evolução do projeto

Este projeto passou por diversas melhorias ao longo do desenvolvimento:
v1 — CRUD básico com armazenamento em arquivo JSON
v2 — Migração para banco de dados SQLite com Flask-SQLAlchemy
v3 — Autenticação com criptografia de senha (Werkzeug)
v4 — Níveis de acesso e bloqueio por tentativas de login
v5 — Registro de usuários, proteção de dados e variáveis de ambiente

## 👩‍💻 Sobre a desenvolvedora

Estudante de TI com foco em desenvolvimento web, buscando minha primeira oportunidade de estágio. Apaixonada por aprender e transformar conhecimento em projetos reais.
