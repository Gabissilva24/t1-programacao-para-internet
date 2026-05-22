DROP DATABASE IF EXISTS t1_programacao;

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
    email VARCHAR(255) NOT NULL UNIQUE,
    tipo_perfil VARCHAR(50),
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

-- DROP TABLE IF EXISTS filmes;

CREATE TABLE IF NOT EXISTS filmes (
    id_filme BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    diretor VARCHAR(150),
    ano SMALLINT UNSIGNED,
    genero_id BIGINT UNSIGNED,
    status ENUM('Ativo','Inativo') DEFAULT 'Ativo',

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

-- DROP TABLE IF EXISTS series;

CREATE TABLE IF NOT EXISTS series (
    id_serie BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    temporadas INT UNSIGNED DEFAULT 0,
    plataforma VARCHAR(150),
    status ENUM('Ativo','Inativo') DEFAULT 'Ativo',

    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_titulo_series (titulo)
);