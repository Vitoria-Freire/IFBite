from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL #para inserir usuarios no banco
import MySQLdb.cursors
import re

from crud import createUpdateDelete
from crud import read

app = Flask(__name__)

########### Rotas ################

# cadastro de usuarios 
@app.route ('/login', methods = ['GET', 'POST'])
def cadastro():
    if request.method == 'POST' and 'password' and 'email' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor





# verifica se o usuario já está cadastrado
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'password' and 'email' in request.form:
        email = request.form['email']
        password = request.form['password']
    cursor = mys
#nao ta terminado

    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/painel')
def painel():
    return render_template('painel.html')

@app.route('/pagamento')
def pagamento():
    return render_template('pagamento.html')

@app.route('/restaurante')
def restaurante():
    return render_template('restaurante.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carinho.html')

