from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from crud import createUpdateDelete
from crud import read

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorador

app = Flask(__name__)
app.secret_key = "chave_super_secreta" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = read("SELECT * FROM usuario WHERE email = %s",
                       (email, ))
        
        print(usuario)
        
        if usuario[0]['senha'] == senha:
            session['usuario'] = usuario[0]['id']
            return render_template('sucesso.html', mensagem = f"Seja bem vindo {usuario[0]['nome']}!", url = "/home")
        else:
            return render_template('erro.html', mensagem = f"Parece que Ocorreu um Erro, Tente Novamente!", url = "/login")
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None) 
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome').title()
        telefone = request.form.get('tel')
        tipoUsuario = request.form.get('tipoUsuario')
        
        if createUpdateDelete(
            "INSERT INTO usuario (email, senha, nome, telefone, tipo) VALUES (%s,%s,%s,%s,%s)",
            (email, senha, nome, telefone, tipoUsuario),
            "INSERT"):

            if tipoUsuario == 'res':
                id = read(
                "SELECT id FROM usuario WHERE nome = %s",
                (nome, ))

                return redirect(url_for('cadastroRestaurante', id = int(id[0]['id'])))
    
            return render_template('sucesso.html', mensagem = "Você foi Cadastrado com Sucesso!", url = "/login")
        
        else:
            return render_template('erro.html', mensagem = "Ocorreu um erro no seu Cadastro, Tente Novamente!", url = "/cadastro")

    return render_template('cadastro.html')

@app.route('/cadastroRestaurante<int:id>', methods=['GET', 'POST'])
def cadastroRestaurante(id):
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('tel')
        cnpj = request.form.get('cnpj')
        localidade = request.form.get('localidade')

        if createUpdateDelete(
            "INSERT INTO restaurante (nome, telefone, cnpj, localidade) VALUES (%s,%s,%s,%s)",
            (nome, telefone, cnpj, localidade),
            "INSERT"):

            idRestaurante = read(
                "SELECT id FROM restaurante WHERE nome = %s",
                (nome, ))
            
            createUpdateDelete(
                "UPDATE usuario SET idRestaurante = %s WHERE id = %s",
                (int(idRestaurante[0]['id']), id),
                "UPDATE")
    
            return render_template('sucesso.html', mensagem = "Você Cadastrou se Restaurante com Sucesso!", url = "/login")
        
        else:
            return render_template('erro.html', mensagem = "Ocorreu um erro no Cadastro, Tente Novamente!", url = "/cadastroRestaurante")

    return render_template('cadastroRestaurante.html')

@app.route('/home')
@login_requerido
def home():
    id = session.get('usuario')
    usuario = read("SELECT tipo, nome FROM usuario WHERE id = %s",
                       (id, ))
    
    return render_template('home.html', usuario = usuario)

@app.route('/perfil', methods=['GET', 'POST'])
@login_requerido
def perfil():
    id = session.get('usuario')
    usuario = read("SELECT * FROM usuario WHERE id = %s",
                       (id, ))
    
    enderecos = read("SELECT * FROM localidade WHERE idUsuario = %s",
                       (id, ))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            senha = request.form.get('senha')
            nome = request.form.get('nome').title()
            telefone = request.form.get('tel')
            if createUpdateDelete(
                        "UPDATE usuario SET email = %s, senha = %s, nome = %s, telefone = %s WHERE id = %s",
                        (email, senha, nome, telefone, id),
                        "UPDATE"):
                return render_template('sucesso.html', mensagem = f"Seus Dados Foram Alterados Com Sucesso!", url = "/login")
            else:
                return render_template('erro.html', mensagem = f"Parece que Ocorreu um Erro, Tente Novamente!", url = "/perfil")
            
        except:
            endereco = request.form.get('endereco')
            if createUpdateDelete(
                        "INSERT INTO localidade (idUsuario, localidade) VALUES (%s, %s)",
                        (id, endereco),
                        "INSERT"):
                return render_template('sucesso.html', mensagem = f"Localidade Adicionada Com Sucesso!", url = "/perfil")
            else:
                return render_template('erro.html', mensagem = f"Parece que Ocorreu um Erro, Tente Novamente!", url = "/perfil")

    return render_template('perfil.html', usuario = usuario, enderecos = enderecos)