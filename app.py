from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'cine_catalogo_ppi_secret_key'


# DADOS SIMULADOS
usuarios = [
    {"id": 1, "nome": "Admin", "email": "admin@cine.com", "tipo": "Administrador"},
    {"id": 2, "nome": "Gabriele Soares", "email": "gabriele@cine.com", "tipo": "Editora"},
    {"id": 3, "nome": "Bruno Oliveira", "email": "bruno@cine.com", "tipo": "Editor"},
    {"id": 4, "nome": "Ana Costa", "email": "ana@cine.com", "tipo": "Visualizador"},
    {"id": 5, "nome": "Carlos Lima", "email": "carlos@cine.com", "tipo": "Administrador"},
]

filmes = [
    {"id": 1, "titulo": "O Auto da Compadecida", "diretor": "Guel Arraes", "ano": 2000, "genero": "Comédia"},
    {"id": 2, "titulo": "A Múmia", "diretor": "Stephen Sommers", "ano": 1999, "genero": "Aventura"},
    {"id": 3, "titulo": "O Sexto Sentido", "diretor": "M. Night Shyamalan", "ano": 1999, "genero": "Suspense"},
    {"id": 4, "titulo": "Olhos Famintos 2", "diretor": "Victor Salva", "ano": 2003, "genero": "Terror"},
    {"id": 5, "titulo": "Os Sem-Floresta", "diretor": "Tim Johnson", "ano": 2006, "genero": "Animação"},
]

series = [
    {"id": 1, "titulo": "Peaky Blinders", "temporadas": 6, "plataforma": "Netflix"},
    {"id": 2, "titulo": "Smallville", "temporadas": 10, "plataforma": "Prime Video"},
    {"id": 3, "titulo": "Gossip Girl", "temporadas": 6, "plataforma": "Netflix"},
    {"id": 4, "titulo": "Supernatural", "temporadas": 15, "plataforma": "HBO Max"},
    {"id": 5, "titulo": "Teen Wolf", "temporadas": 6, "plataforma": "Netflix"},
]

generos = [
    {"id": 1, "nome": "Comédia", "descricao": "Filmes e séries focados em humor (Ex: O Auto da Compadecida)"},
    {"id": 2, "nome": "Terror", "descricao": "Para quem gosta de sustos e suspense (Ex: Olhos Famintos)"},
    {"id": 3, "nome": "Ação/Aventura", "descricao": "Muita adrenalina e exploração (Ex: A Múmia)"},
    {"id": 4, "nome": "Drama", "descricao": "Histórias intensas e emocionantes (Ex: Peaky Blinders)"},
    {"id": 5, "nome": "Animação", "descricao": "Desenhos para todas as idades (Ex: Os Sem-Floresta)"},
]


# ROTAS PUBLICAS
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('listar_usuarios'))
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        flash(f'Cadastro realizado com sucesso! Faça login', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
        return redirect(url_for('login'))


# ROTAS PROTEGIDAS

# USUARIOS
@app.route('/usuarios/listar')
def listar_usuarios():
    return render_template('usuarios/listar_usuarios.html', lista=usuarios)

@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash(f'Erro! O campo nome é obrigatório.', 'danger')
        else:
            flash(f'Usuário {nome} cadastrado!', 'success')
            return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/inserir_usuario.html')


# FILMES
@app.route('/filmes/listar')
def listar_filmes():
    return render_template('filmes/listar_filmes.html', lista=filmes)

@app.route('/filmes/inserir', methods=['GET', 'POST'])
def inserir_filme():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        if not titulo:
            flash(f'Erro! O título é obrigatório.', 'danger')
        else:
            flash(f'Filme {titulo} adicionado!', 'success')
            return redirect(url_for('listar_filmes'))
    return render_template('filmes/inserir_filmes.html')


# SERIES
@app.route('/series/listar')
def listar_series():
    return render_template('series/listar_series.html', lista=series)

@app.route('/series/inserir', methods=['GET', 'POST'])
def inserir_series():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        if not titulo:
            flash(f'Erro! O título é obrigatório.', 'danger')
        else:
            flash(f'Série {titulo} adicionada!', 'success')
            return redirect(url_for('listar_series'))
    return render_template('series/inserir_series.html')


# GENEROS
@app.route('/generos/listar')
def listar_generos():
    return render_template('generos/listar_generos.html', lista=generos)

@app.route('/generos/inserir', methods=['GET', 'POST'])
def inserir_genero():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash(f'Erro! O nome do gênero é obrigatório.', 'danger')
        else:
            flash(f'Gênero {nome} criado!', 'success')
            return redirect(url_for('listar_generos'))
    return render_template('generos/inserir_generos.html')


# SOBRE EQUIPE
@app.route('/equipe')
def equipe():
    return render_template('sobre_equipe.html')


if __name__ == '__main__':
    app.run(debug=True)