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
            ORDER BY id_usuario ASC
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
        cpf = request.form.get('cpf', '').strip()
        email = request.form.get('email', '').strip()
        status = request.form.get('status', 'Ativo').strip()
        senha = request.form.get('senha', '').strip()
        confirmar_senha = request.form.get('confirmar_senha', '').strip()
        funcao_id = request.form.get('funcao', '').strip()
        
        # VALIDACAO NO BACK-END: Verifica se os campos obrigatorios foram preenchidos
        if not nome:
            flash(f'Erro! O campo nome é obrigatório.', 'danger')
            
        if cpf:
            if len(cpf) != 14:
                flash('CPF inválido. Digite no formato 000.000.000-00.', 'danger')
                return redirect(url_for('inserir_usuario'))
            if cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
                flash('CPF inválido. Digite no formato 000.000.000-00.', 'danger')
                return redirect(url_for('inserir_usuario'))
        else:
            flash('O campo CPF é obrigatório.', 'danger')
            return redirect(url_for('inserir_usuario'))
        
        if not email:
            flash('O campo e-mail é obrigatório.', 'danger')
            return redirect(url_for('inserir_usuario'))
        
        if not funcao_id:
            flash('Selecione uma função.', 'danger')
            return redirect(url_for('inserir_usuario'))

        if senha:
            if senha != confirmar_senha:
                flash('As senhas não conferem.', 'danger')
                return render_template('usuarios/inserir_usuario.html', lista_funcoes=lista_funcoes, form=request.form)
            if len(senha) < 8:
                flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
                return redirect(url_for('inserir_usuario'))
        else:
            flash('O campo senha é obrigatório.', 'danger')
            return redirect(url_for('inserir_usuario'))

        
        sql = '''SELECT COUNT(*) AS qtde FROM usuarios
                WHERE email = %s OR cpf = %s
                    '''
        existente = execute_one(sql, (email, cpf))
        if existente and existente['qtde'] > 0:
            flash(f'E-mail ou CPF já cadastrados', 'danger')
            return render_template('usuarios/inserir_usuario.html',
                           lista_funcoes=lista_funcoes,
                           form=request.form)  # ← mantém os dados preenchidos
        
        senha_hash = generate_password_hash(senha)

        try:
            sql = '''INSERT INTO usuarios (nome_usuario, cpf, email, status, senha, funcao_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
            '''
            dados = (nome, cpf, email, status, senha_hash, funcao_id)
            execute_query(sql, dados)
            flash(f'Usuário {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))
        except Exception as e:
            print(f'Erro ao criar Usúario {e}')
            flash(f'Erro ao criar Usúario {e}', 'danger')
            return render_template('usuarios/inserir_usuario.html',
                           lista_funcoes=lista_funcoes,
                           form=request.form)
        
    sql = 'SELECT id_funcao, nome FROM funcoes'
    lista_funcoes = execute_query(sql, fetch=True)
    return render_template('usuarios/inserir_usuario.html', lista_funcoes=lista_funcoes)

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):

    if request.method == 'POST':
        nome           = request.form.get('nome', '').strip()
        cpf            = request.form.get('cpf', '').strip()
        email          = request.form.get('email', '').strip()
        funcao_id      = request.form.get('funcao', '').strip()
        status         = request.form.get('status', '').strip()
        senha          = request.form.get('senha', '').strip()
        confirmar_senha = request.form.get('confirmar_senha', '').strip()

        # VALIDAÇÕES
        if not nome:
            flash('O campo nome é obrigatório.', 'danger')
            return redirect(url_for('editar_usuario', id=id))

        if not email:
            flash('O campo e-mail é obrigatório.', 'danger')
            return redirect(url_for('editar_usuario', id=id))

        if not funcao_id:
            flash('Selecione uma função.', 'danger')
            return redirect(url_for('editar_usuario', id=id))

        if cpf:
            if len(cpf) != 14:
                flash('CPF inválido. Digite no formato 000.000.000-00.', 'danger')
                return redirect(url_for('editar_usuario', id=id))
            if cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
                flash('CPF inválido. Digite no formato 000.000.000-00.', 'danger')
                return redirect(url_for('editar_usuario', id=id))
        else:
            flash('O campo CPF é obrigatório.', 'danger')
            return redirect(url_for('editar_usuario', id=id))

        # Verifica se e-mail ou CPF já pertencem a OUTRO usuário
        existente = execute_one(
            'SELECT id_usuario FROM usuarios WHERE (email = %s OR cpf = %s) AND id_usuario <> %s',
            (email, cpf, id)
        )
        if existente:
            flash('E-mail ou CPF já cadastrados em outro usuário.', 'danger')
            return redirect(url_for('editar_usuario', id=id))

        # Senha é opcional na edição — só valida se foi preenchida
        if senha:
            if senha != confirmar_senha:
                flash('As senhas não conferem.', 'danger')
                return redirect(url_for('editar_usuario', id=id))
            if len(senha) < 8:
                flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
                return redirect(url_for('editar_usuario', id=id))

        try:
            if senha:
                # Atualiza com nova senha
                sql = '''UPDATE usuarios SET
                            nome_usuario = %s,
                            cpf          = %s,
                            email        = %s,
                            funcao_id    = %s,
                            status       = %s,
                            senha        = %s
                         WHERE id_usuario = %s'''
                dados = (nome, cpf, email, funcao_id, status, generate_password_hash(senha), id)
            else:
                # Atualiza sem alterar a senha
                sql = '''UPDATE usuarios SET
                            nome_usuario = %s,
                            cpf          = %s,
                            email        = %s,
                            funcao_id    = %s,
                            status       = %s
                         WHERE id_usuario = %s'''
                dados = (nome, cpf, email, funcao_id, status, id)

            execute_query(sql, dados)
            flash(f'Usuário {nome} atualizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            flash(f'Erro ao editar usuário: {e}', 'danger')
            return redirect(url_for('editar_usuario', id=id))

    # GET — busca os dados atuais do usuário para preencher o formulário
    item = execute_one('SELECT * FROM usuarios WHERE id_usuario = %s', (id,))
    if not item:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('listar_usuarios'))

    lista_funcoes = execute_query('SELECT id_funcao, nome FROM funcoes', fetch=True)
    return render_template('usuarios/editar_usuario.html', item=item, lista_funcoes=lista_funcoes)


@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
def usuarios_excluir(id):
    try:
        execute_query('DELETE FROM usuarios WHERE id_usuario = %s', (id,))
        flash('Usuário excluído com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao excluir usuário: {e}', 'danger')
    return redirect(url_for('listar_usuarios'))

# --- ENTIDADE: FILMES ---
@app.route('/filmes/listar')
def listar_filmes():
    sql = '''
        SELECT
            f.id_filme,
            f.titulo,
            f.diretor,
            f.ano,
            f.poster,
            g.nome AS genero
        FROM filmes AS f
        LEFT JOIN generos AS g ON f.genero_id = g.id_genero
        ORDER BY f.titulo ASC
    '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('filmes/listar_filmes.html', lista=lista_dados)

@app.route('/filmes/inserir', methods=['GET', 'POST'])
def inserir_filme():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        diretor = request.form.get('diretor', '').strip()
        ano = request.form.get('ano', '').strip()
        genero_id = request.form.get('genero', '').strip()
        poster = request.form.get('poster', '').strip()
        
        # Validacao de campo obrigatorio antes do redirecionamento
        if not titulo:
            flash(f'Erro! O título é obrigatório.', 'danger')
            return redirect(url_for('inserir_filme'))
        
        try:
            sql = '''INSERT INTO filmes (titulo, diretor, ano, genero_id, poster)
                     VALUES (%s, %s, %s, %s, %s)'''
            execute_query(sql, (titulo, diretor or None, ano or None, genero_id or None, poster or None))
            flash(f'Filme {titulo} cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_filmes'))
        except Exception as e:
            print(f'Erro ao inserir filme: {e}')
            flash('Erro ao salvar filme. Tente novamente.', 'danger')
            return redirect(url_for('inserir_filme'))

    lista_generos = execute_query('SELECT id_genero, nome FROM generos', fetch=True)
    return render_template('filmes/inserir_filme.html', lista_generos=lista_generos)

@app.route('/filmes/editar/<int:id>', methods=['GET', 'POST'])
def editar_filme(id):

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        diretor = request.form.get('diretor', '').strip()
        ano = request.form.get('ano', '').strip()
        genero_id = request.form.get('genero_id', '').strip()
        poster = request.form.get('poster', '').strip()

        if not titulo:
            flash('O título é obrigatório.', 'danger')
            return redirect(url_for('editar_filme', id=id))

        try:
            sql = '''UPDATE filmes SET
                        titulo    = %s,
                        diretor   = %s,
                        ano       = %s,
                        genero_id = %s,
                        poster    = %s
                     WHERE id_filme = %s'''
            dados = (titulo, diretor or None, ano or None, genero_id or None, poster or None, id)
            execute_query(sql, dados)
            flash(f'Filme {titulo} atualizado com sucesso!', 'success')
            return redirect(url_for('listar_filmes'))
        except Exception as e:
            print(f'Erro ao editar filme: {e}')
            flash('Erro ao editar filme. Tente novamente.', 'danger')
            return redirect(url_for('editar_filme', id=id))

    # GET — busca os dados atuais
    item = execute_one('SELECT * FROM filmes WHERE id_filme = %s', (id,))
    if not item:
        flash('Filme não encontrado.', 'danger')
        return redirect(url_for('listar_filmes'))

    lista_generos = execute_query('SELECT id_genero, nome FROM generos', fetch=True)
    return render_template('filmes/editar_filme.html', item=item, lista_generos=lista_generos)


@app.route('/filmes/excluir/<int:id>', methods=['POST'])
def excluir_filme(id):
    try:
        execute_query('DELETE FROM filmes WHERE id_filme = %s', (id,))
        flash('Filme excluído com sucesso.', 'success')
    except Exception as e:
        print(f'Erro ao excluir filme: {e}')
        flash('Erro ao excluir filme. Tente novamente.', 'danger')
    return redirect(url_for('listar_filmes'))

# --- ENTIDADE: SERIES ---
@app.route('/series/listar')
def listar_series():
    sql = '''
        SELECT id_serie, titulo, temporadas, plataforma, poster
        FROM series
        ORDER BY titulo ASC
    '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('series/listar_series.html', lista=lista_dados)

@app.route('/series/inserir', methods=['GET', 'POST'])
def inserir_serie():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        temporadas = request.form.get('temporadas', '').strip()
        plataforma = request.form.get('plataforma', '').strip()
        poster = request.form.get('poster', '').strip()

        if not titulo:
            flash(f'Erro! O título é obrigatório.', 'danger')
            return redirect(url_for('inserir_serie'))
        
        if not temporadas:
            flash('O número de temporadas é obrigatório.', 'danger')
            return redirect(url_for('inserir_serie'))
        
        try:
            sql = '''INSERT INTO series (titulo, temporadas, plataforma, poster)
                     VALUES (%s, %s, %s, %s)'''
            execute_query(sql, (titulo, temporadas, plataforma or None, poster or None))
            flash(f'Série {titulo} cadastrada com sucesso!', 'success')
            return redirect(url_for('listar_series'))
        except Exception as e:
            print(f'Erro ao inserir série: {e}')
            flash('Erro ao salvar série. Tente novamente.', 'danger')
            return redirect(url_for('inserir_serie'))

    return render_template('series/inserir_serie.html')

@app.route('/series/editar/<int:id>', methods=['GET', 'POST'])
def editar_serie(id):

    if request.method == 'POST':
        titulo     = request.form.get('titulo', '').strip()
        temporadas = request.form.get('temporadas', '0').strip()
        plataforma = request.form.get('plataforma', '').strip()
        poster     = request.form.get('poster', '').strip()

        if not titulo:
            flash('O título é obrigatório.', 'danger')
            return redirect(url_for('editar_serie', id=id))

        try:
            sql = '''UPDATE series SET
                        titulo     = %s,
                        temporadas = %s,
                        plataforma = %s,
                        poster     = %s
                     WHERE id_serie = %s'''
            execute_query(sql, (titulo, temporadas, plataforma or None, poster or None, id))
            flash(f'Série {titulo} atualizada com sucesso!', 'success')
            return redirect(url_for('listar_series'))
        except Exception as e:
            print(f'Erro ao editar série: {e}')
            flash('Erro ao editar série. Tente novamente.', 'danger')
            return redirect(url_for('editar_serie', id=id))

    item = execute_one('SELECT * FROM series WHERE id_serie = %s', (id,))
    if not item:
        flash('Série não encontrada.', 'danger')
        return redirect(url_for('listar_series'))

    return render_template('series/editar_serie.html', item=item)


@app.route('/series/excluir/<int:id>', methods=['POST'])
def excluir_serie(id):
    try:
        execute_query('DELETE FROM series WHERE id_serie = %s', (id,))
        flash('Série excluída com sucesso.', 'success')
    except Exception as e:
        print(f'Erro ao excluir série: {e}')
        flash('Erro ao excluir série. Tente novamente.', 'danger')
    return redirect(url_for('listar_series'))


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
        ORDER BY id_genero ASC
    '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('generos/listar_generos.html', dados=lista_dados)

@app.route('/generos/inserir', methods=['GET', 'POST'])
def inserir_genero():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()

        if not nome:
            flash(f'Erro! O nome do gênero é obrigatório.', 'danger')
            return redirect(url_for('inserir_genero'))
        
        existente = execute_one('SELECT COUNT(*) AS qtde FROM generos WHERE nome = %s', (nome,))
        if existente and existente['qtde'] > 0:
            flash(f'Já existe um gênero com o nome {nome}.', 'danger')
            return redirect(url_for('inserir_genero'))
        
        try:
            sql = 'INSERT INTO generos (nome, descricao) VALUES (%s, %s)'
            execute_query(sql, (nome, descricao))
            flash(f'Gênero {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_generos'))
        except Exception as e:
            print(f'Erro ao inserir gênero: {e}')
            flash('Erro ao salvar gênero. Tente novamente.', 'danger')
            return redirect(url_for('inserir_genero'))

    return render_template('generos/inserir_genero.html')

@app.route('/generos/editar/<int:id>', methods=['GET', 'POST'])
def editar_genero(id):

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()

        if not nome:
            flash('O nome do gênero é obrigatório.', 'danger')
            return redirect(url_for('editar_genero', id=id))

        existente = execute_one(
            'SELECT COUNT(*) AS qtde FROM generos WHERE nome = %s AND id_genero <> %s',
            (nome, id)
        )
        if existente and existente['qtde'] > 0:
            flash(f'Já existe um gênero com o nome {nome}.', 'danger')
            return redirect(url_for('editar_genero', id=id))

        try:
            sql = '''UPDATE generos SET nome = %s, descricao = %s
                     WHERE id_genero = %s'''
            execute_query(sql, (nome, descricao, id))
            flash(f'Gênero {nome} atualizado com sucesso!', 'success')
            return redirect(url_for('listar_generos'))
        except Exception as e:
            print(f'Erro ao editar gênero: {e}')
            flash('Erro ao editar gênero. Tente novamente.', 'danger')
            return redirect(url_for('editar_genero', id=id))

    # GET — busca os dados atuais
    item = execute_one('SELECT * FROM generos WHERE id_genero = %s', (id,))
    if not item:
        flash('Gênero não encontrado.', 'danger')
        return redirect(url_for('listar_generos'))

    return render_template('generos/editar_genero.html', item=item)

@app.route('/generos/excluir/<int:id>', methods=['POST'])
def excluir_genero(id):
    try:
        execute_query('DELETE FROM generos WHERE id_genero = %s', (id,))
        flash('Gênero excluído com sucesso.', 'success')
    except Exception as e:
        print(f'Erro ao excluir gênero: {e}')
        flash('Erro ao excluir gênero. Tente novamente.', 'danger')
    return redirect(url_for('listar_generos'))


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
        ORDER BY id_funcao ASC;

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

@app.route('/funcoes/editar/<int:id>', methods=['GET', 'POST'])
def editar_funcao(id):

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        status = request.form.get('status', '').strip()
        descricao = request.form.get('descricao', '').strip()
        gerenciar_usuarios = 1 if request.form.get('gerenciar_usuarios') else 0
        gerenciar_funcoes = 1 if request.form.get('gerenciar_funcoes') else 0
        gerenciar_filmes = 1 if request.form.get('gerenciar_filmes') else 0

        if not nome:
            flash('O campo nome é obrigatório.', 'danger')
            return redirect(url_for('editar_funcao', id=id))

        existente = execute_one(
            'SELECT COUNT(*) AS qtde FROM funcoes WHERE nome = %s AND id_funcao <> %s',
            (nome, id)
        )
        if existente and existente['qtde'] > 0:
            flash(f'Já existe uma função com o nome {nome}.', 'danger')
            return redirect(url_for('editar_funcao', id=id))

        try:
            sql = '''UPDATE funcoes SET
                        nome               = %s,
                        status             = %s,
                        descricao          = %s,
                        gerenciar_usuarios = %s,
                        gerenciar_funcoes  = %s,
                        gerenciar_filmes   = %s
                     WHERE id_funcao = %s'''
            dados = (nome, status, descricao, gerenciar_usuarios, gerenciar_funcoes, gerenciar_filmes, id)
            execute_query(sql, dados)
            flash(f'Função {nome} atualizada com sucesso!', 'success')
            return redirect(url_for('listar_funcoes'))
        except Exception as e:
            print(f'Erro ao editar função: {e}')
            flash('Erro ao editar função. Tente novamente.', 'danger')
            return redirect(url_for('editar_funcao', id=id))

    # GET — busca os dados atuais
    item = execute_one('SELECT * FROM funcoes WHERE id_funcao = %s', (id,))
    if not item:
        flash('Função não encontrada.', 'danger')
        return redirect(url_for('listar_funcoes'))

    return render_template('funcoes/editar_funcao.html', item=item)


@app.route('/funcoes/excluir/<int:id>', methods=['POST'])
def excluir_funcao(id):
    try:
        execute_query('DELETE FROM funcoes WHERE id_funcao = %s', (id,))
        flash('Função excluída com sucesso.', 'success')
    except Exception as e:
        print(f'Erro ao excluir função: {e}')
        flash('Erro ao excluir função. Verifique se não há usuários vinculados a ela.', 'danger')
    return redirect(url_for('listar_funcoes'))


if __name__ == '__main__': # Verifica se esse arquivo esta sendo executado diretamente
    # Inicia o servidor em modo Debug para facilitar o desenvolvimento e correcao de erros
    app.run(debug=True)