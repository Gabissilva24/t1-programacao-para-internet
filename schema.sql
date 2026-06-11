--DROP DATABASE IF EXISTS t1_programacao;

CREATE DATABASE IF NOT EXISTS t1_programacao
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE t1_programacao;

-- DROP TABLE IF EXISTS funcoes;

CREATE TABLE IF NOT EXISTS funcoes(
    id_funcao BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(20) NOT NULL UNIQUE,
    status ENUM ('Ativo', 'Inativo') DEFAULT 'Ativo',
    descricao VARCHAR(255),
    permissoes BOOLEAN DEFAULT 0,
    gerenciar_usuarios BOOLEAN DEFAULT 0,
    gerenciar_funcoes BOOLEAN DEFAULT 0,
    gerenciar_filmes BOOLEAN DEFAULT 0,

    -- log
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- DROP TABLE IF EXISTS usuarios;

CREATE TABLE IF NOT EXISTS usuarios(
    id_usuario BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(50) NOT NULL,
    cpf CHAR(14) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    status ENUM ('Ativo', 'Inativo') DEFAULT 'Ativo',

    funcao_id BIGINT UNSIGNED NOT NULL,

    -- logs
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    -- Cria o relacionamento entre tabelas
    CONSTRAINT fk_usuario_funcao
    FOREIGN KEY (funcao_id) REFERENCES funcoes (id_funcao)
);


-- DROP TABLE IF EXISTS generos;

CREATE TABLE IF NOT EXISTS generos (
    id_genero BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,

    -- logs
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO generos (nome, descricao) VALUES
('Comédia', 'Filmes e séries focados em humor'),
('Aventura', 'Muita adrenalina e exploração'),
('Suspense', 'Histórias de tensão e mistério'),
('Animação', 'Desenhos para todas as idades'),
('Fantasia', 'Mundos imaginários, magia'),
('Romance', 'Histórias de amor, relacionamentos e emoções');

-- DROP TABLE IF EXISTS filmes;

CREATE TABLE IF NOT EXISTS filmes (
    id_filme BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    diretor VARCHAR(150),
    ano SMALLINT UNSIGNED,
    genero_id BIGINT UNSIGNED,
    poster VARCHAR(255) NULL,    

    -- logs
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

     -- Cria o relacionamento entre tabelas
    CONSTRAINT fk_filme_genero FOREIGN KEY (genero_id) REFERENCES generos(id_genero) 
        ON UPDATE CASCADE,

    INDEX idx_titulo (titulo),
    INDEX idx_ano (ano)
);

INSERT INTO filmes (titulo, diretor, ano, genero_id, poster) VALUES
('O Auto da Compadecida', 'Guel Arraes', 2000, (SELECT id_genero FROM generos WHERE nome = 'Comédia'), 'o_auto_da_compadecida.jpg'),
('A Múmia', 'Stephen Sommers', 1999, (SELECT id_genero FROM generos WHERE nome = 'Aventura'), 'a_mumia.jpg'),
('O Sexto Sentido', 'M. Night Shyamalan', 1999, (SELECT id_genero FROM generos WHERE nome = 'Suspense'), 'o_sexto_sentido.jpg'),
('Olhos Famintos 2', 'Victor Salva', 2003, (SELECT id_genero FROM generos WHERE nome = 'Terror'), 'olhos_famintos2.jpg'),
('Os Sem-Floresta', 'Tim Johnson', 2006, (SELECT id_genero FROM generos WHERE nome = 'Animação'), 'os_sem_floresta.jpg');

-- DROP TABLE IF EXISTS series;

CREATE TABLE IF NOT EXISTS series (
    id_serie BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    temporadas INT UNSIGNED NOT NULL,
    plataforma VARCHAR(150),
    poster VARCHAR(255) NULL,

    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_titulo_series (titulo)
);

-- Dados iniciais de séries
INSERT INTO series (titulo, temporadas, plataforma, poster) VALUES
('Peaky Blinders', 6, 'Netflix', 'peaky_blinders.jpg'),
('Smallville', 10, 'Prime Video', 'smallville.jpg'),
('Gossip Girl', 6, 'Netflix', 'gossip_girl.jpg'),
('Supernatural', 15, 'HBO Max', 'supernatural.jpg'),
('Teen Wolf', 6, 'Netflix', 'teen_wolf.jpg');