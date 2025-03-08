from flask import Flask, render_template, request, redirect, url_for

from crud import createUpdateDelete
from crud import read

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        telefone = request.form.get('tel')
        tipoUsuario = request.form.get('tipoUsuario')

        print(email, senha, nome, telefone, tipoUsuario)

        createUpdateDelete(
            "INSERT INTO usuario (email, senha, nome, telefone, tipo) VALUES (%s,%s,%s,%s,%s)",
            (email, senha, nome, telefone, tipoUsuario),
            "INSERT"
        )

    return render_template('cadastro.html')