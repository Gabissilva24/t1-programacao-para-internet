from flask import Flask, render_template, request, redirect, url_for, flash
from db import iniciar_bd, execute_query, execute_one
from werkzeug.security import generate_password_hash


app = Flask(__name__)
# A secret_key é necessária para utilizar o sistema de mensagens flash
app.secret_key = 'cinecatalogo_t1_ppi_secret_key'

iniciar_bd() # inicia o banco de dados


# --- DADOS SIMULADOS (HARDCODED) ---
# Listas que simulam o banco de dados
usuarios = [
    {"id": 1, "nome": "Admin", "email": "admin@cine.com", "tipo": "Administrador"},
    {"id": 2, "nome": "Gabriele Soares", "email": "gabriele@cine.com", "tipo": "Editora"},
    {"id": 3, "nome": "Bruno Oliveira", "email": "bruno@cine.com", "tipo": "Editor"},
    {"id": 4, "nome": "Ana Costa", "email": "ana@cine.com", "tipo": "Visualizador"},
    {"id": 5, "nome": "Carlos Lima", "email": "carlos@cine.com", "tipo": "Administrador"}
]

filmes = [
    {"id": 1, "titulo": "O Auto da Compadecida", "diretor": "Guel Arraes", "ano": 2000, "genero": "Comédia", "poster": "o_auto_da_compadecida.jpg"},
    {"id": 2, "titulo": "A Múmia", "diretor": "Stephen Sommers", "ano": 1999, "genero": "Aventura", "poster": "a_mumia.jpg"},
    {"id": 3, "titulo": "O Sexto Sentido", "diretor": "M. Night Shyamalan", "ano": 1999, "genero": "Suspense", "poster": "o_sexto_sentido.jpg"},
    {"id": 4, "titulo": "Olhos Famintos 2", "diretor": "Victor Salva", "ano": 2003, "genero": "Terror", "poster": "olhos_famintos2.jpg"},
    {"id": 5, "titulo": "Os Sem-Floresta", "diretor": "Tim Johnson", "ano": 2006, "genero": "Animação", "poster": "os_sem_floresta.jpg"}
]

series = [
    {"id": 1, "titulo": "Peaky Blinders", "temporadas": 6, "plataforma": "Netflix", "poster": "peaky_blinders.jpg"},
    {"id": 2, "titulo": "Smallville", "temporadas": 10, "plataforma": "Prime Video", "poster": "smallville.jpg"},
    {"id": 3, "titulo": "Gossip Girl", "temporadas": 6, "plataforma": "Netflix", "poster": "gossip_girl.jpg"},
    {"id": 4, "titulo": "Supernatural", "temporadas": 15, "plataforma": "HBO Max", "poster": "supernatural.jpg"},
    {"id": 5, "titulo": "Teen Wolf", "temporadas": 6, "plataforma": "Netflix", "poster": "teen_wolf.jpg"}
]

generos = [
    {"id": 1, "nome": "Comédia", "descricao": "Filmes e séries focados em humor (Ex: O Auto da Compadecida)"},
    {"id": 2, "nome": "Terror", "descricao": "Para quem gosta de sustos e suspense (Ex: Olhos Famintos)"},
    {"id": 3, "nome": "Ação/Aventura", "descricao": "Muita adrenalina e exploração (Ex: A Múmia)"},
    {"id": 4, "nome": "Drama", "descricao": "Histórias intensas e emocionantes (Ex: Peaky Blinders)"},
    {"id": 5, "nome": "Animação", "descricao": "Desenhos para todas as idades (Ex: Os Sem-Floresta)"}
]

funcoes = [
    {"id": 1, "nome": "Administrador", "status": "ativo", "descricao": "Acesso total ao sistema"},
    {"id": 2, "nome": "Editor", "status": "ativo", "descricao": "Pode gerenciar conteúdo"},
    {"id": 3, "nome": "Visualizador", "status": "inativo", "descricao": "Apenas visualiza"}
]


# --- ROTAS PUBLICAS (Acessiveis sem login) ---
@app.route('/')
def index():
    # Pagina inicial (vitrine do negocio)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se o metodo for POST, simula o processamento do login e redireciona para a area restrita (listar_usuarios)
    if request.method == 'POST':
        return redirect(url_for('listar_usuarios'))
    # Se apenas acessar a pagina (GET), mostra o formulario de login
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # Processa o formulario de novo usuario e utiliza flash para feedback visual (redireciona para pagina de login)
    if request.method == 'POST':
        flash(f'Cadastro realizado com sucesso! Faça login', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
        # Encerra a sessao e retorna a pagina de login
        return redirect(url_for('login'))


# --- ROTAS PROTEGIDAS (ENTIDADES DO SISTEMA) ---

# --- ENTIDADE: USUARIOS ---
@app.route('/usuarios/listar')
def listar_usuarios():
    sql = '''
            SELECT
                id_usuario,
                u.nome_usuario AS nome,
                email,
                f.nome AS funcao,
                u.status
            FROM usuarios AS u
            INNER JOIN funcoes AS f ON u.funcao_id = f.id_funcao
            ORDER BY id_usuario DESC
        '''
    lista_dados = execute_query(sql, fetch=True)
    # Renderiza (abre) a lista de usuarios passando a lista hardcoded 'usuarios' para o Jinja2
    return render_template('usuarios/listar_usuarios.html', dados=lista_dados)

@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():

    sql = 'SELECT id_funcao, nome FROM funcoes'
    lista_funcoes = execute_query(sql, fetch=True)

    if request.method == 'POST': # O request e um objeto do Flask que representa tudo que veio da requisicao do usuario.
        nome = request.form.get('nome', '').strip() # pega o valor digitado no campo nome
        email = request.form.get('email', '').strip()
        tipo_perfil = request.form.get('tipo_perfil', '').strip()
        status = request.form.get('status', 'Ativo').strip()
        
        # VALIDACAO NO BACK-END: Verifica se os campos obrigatorios foram preenchidos
        if not nome:
            flash(f'Erro! O campo nome é obrigatório.', 'danger')

        if senha != confirmar_senha:
            flash(f'As senhas não conferem.', 'danger')
            return redirect(url_for('inserir_usuario'))

        else:
            flash(f'Usuário {nome} cadastrado!', 'success')
            return redirect(url_for('listar_usuarios'))
        
    sql = '''SELECT nome (*) AS qtde FROM usuarios
            WHERE email = %s OR cpf = %s
                '''
    existente = execute_one(sql, (email, cpf))
    if existente:
        flash(f'E-mail ou CPF já cadastrados', 'danger')

    senha_hash = generate_password_hash(senha)

        try:
            sql = '''INSERT INTO funcoes (nome_usuario, email, tipo_perfil, senha, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            dados = (nome, email, tipo_perfil, senha, status)
            execute_query(sql, dados)
            flash(f'A função <b> {nome} </b> inserida com sucesso!', 'success')
            return redirect(url_for('listar_funcoes'))

        except Exception as e:
            flash(f'Erro ao salvar {e}', 'danger')
            return redirect(url_for('inserir_funcoes'))

    # nesse sql tem email e senha, verificar se no usuario tem realmente esses campos. Verificar qual nome está no campo senha no formulario de inserir_usuario, fica no name=

    return render_template('usuarios/inserir_usuario.html', lista_funcoes=lista_funcoes)


# --- ENTIDADE: FILMES ---
@app.route('/filmes/listar')
def listar_filmes():
    return render_template('filmes/listar_filmes.html', lista=filmes)

@app.route('/filmes/inserir', methods=['GET', 'POST'])
def inserir_filme():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        # Validacao de campo obrigatorio antes do redirecionamento
        if not titulo:
            flash(f'Erro! O título é obrigatório.', 'danger')
        else:
            flash(f'Filme {titulo} adicionado!', 'success')
            return redirect(url_for('listar_filmes'))
    return render_template('filmes/inserir_filme.html')


# --- ENTIDADE: SERIES ---
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
    return render_template('series/inserir_serie.html')


# --- ENTIDADE: GENEROS ---
@app.route('/generos/listar')
def listar_generos():
    sql = '''
        SELECT
            id_genero,
            nome,
            descricao,
            criado_em,
            alterado_em
        FROM generos
        ORDER BY id_genero DESC
    '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('generos/listar_generos.html', dados=lista_dados)

@app.route('/generos/inserir', methods=['GET', 'POST'])
def inserir_genero():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash(f'Erro! O nome do gênero é obrigatório.', 'danger')
        else:
            flash(f'Gênero {nome} criado!', 'success')
            return redirect(url_for('listar_generos'))
    return render_template('generos/inserir_genero.html')


# SOBRE EQUIPE
@app.route('/equipe')
def equipe():
    return render_template('sobre_equipe.html')

# --- ENTIDADE: FUNCOES ---
@app.route('/funcoes/listar')
def listar_funcoes():
    sql = '''
           SELECT 
            id_funcao,
            nome,
            status,
            descricao,
            permissoes,
            gerenciar_usuarios,
            gerenciar_funcoes,
            gerenciar_filmes,
            criado_em,
            alterado_em
        FROM funcoes
        ORDER BY id_funcao DESC;

        '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('funcoes/listar_funcoes.html', dados=lista_dados)

@app.route('/funcoes/inserir', methods=['GET', 'POST'])
def inserir_funcao():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        status = request.form.get('status', 'Ativo').strip()
        descricao = request.form.get('descricao', '').strip()
        gerenciar_usuarios = 1 if request.form.get('gerenciar_usuarios', '') else 0
        gerenciar_funcoes = 1 if request.form.get('gerenciar_funcoes', '') else 0
        gerenciar_filmes = 1 if request.form.get('gerenciar_filmes', '') else 0

        if not nome:
            flash('O campo <b>NOME</b> é obrigatório.', 'danger')
            return redirect(url_for('listar_funcoes'))
        # else:
        #     flash(f'Função {nome} cadastrada!', 'success')
        #     return redirect(url_for('listar_funcoes'))
        # else:
        #     # VALIDACAO: nome duplicado
        #     sql_verificar = 'SELECT id_funcao FROM funcoes WHERE nome = %s'
        #     existente = execute_query(sql_verificar, params=(nome,), fetch=True)
        #     if existente:
        #         flash(f'Erro! Já existe uma função com o nome <b>{nome}</b>.', 'danger')
        #     else:
        #         # INSERT no banco
        #         sql = '''
        #             INSERT INTO funcoes (nome, status, descricao, gerenciar_usuarios, gerenciar_funcoes, gerenciar_filmes)
        #             VALUES (%s, %s, %s, %s, %s, %s)
        #         '''
        #         dados = (nome, status, descricao, gerenciar_usuarios, gerenciar_funcoes, gerenciar_filmes)
        #         execute_query(sql, dados)
        #         flash(f'Função {nome} cadastrada!', 'success')
        #         return redirect(url_for('inserir_funcoes'))
        
        try:
            sql = '''INSERT INTO funcoes (nome, status, descricao, gerenciar_usuarios, gerenciar_funcoes, gerenciar_filmes)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            dados = (nome, status, descricao, gerenciar_usuarios, gerenciar_funcoes, gerenciar_filmes)
            execute_query(sql, dados)
            flash(f'A função <b> {nome} </b> inserida com sucesso!', 'success')
            return redirect(url_for('listar_funcoes'))

        except Exception as e:
            flash(f'Erro ao salvar {e}', 'danger')
            return redirect(url_for('inserir_funcoes'))
        
    # Entra aqui somente se for GET
    return render_template('funcoes/inserir_funcao.html')


if __name__ == '__main__': # Verifica se esse arquivo esta sendo executado diretamente
    # Inicia o servidor em modo Debug para facilitar o desenvolvimento e correcao de erros
    app.run(debug=True)