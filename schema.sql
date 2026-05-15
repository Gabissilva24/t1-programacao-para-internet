-- DROP DATABASE IF EXISTS t1_programacao;

CREATE DATABASE IF NOT EXISTS t1_programacao
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE t1_programacao;

-- DROP TABLE IF EXISTS funcoes;

CREATE TABLE IF NOT EXISTS funcoes(
    id_funcao BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_funcao VARCHAR(20) NOT NULL UNIQUE,
    status ENUM ('Ativo', 'Inativo') DEFAULT 'Ativo',
    descricao VARCHAR(255),
    permissoes BOOLEAN DEFAULT 0,
    gerenciar_usuarios BOOLEAN DEFAULT 0,
    gerenciar_funcoes BOOLEAN DEFAULT 0,
    gerenciar_filmes BOOLEAN DEFAULT 0,

    -- log
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENTE_TIMESTAMP,
        ON UPDATE CURRENTE_TIMESTAMP
)

-- DROP TABLE IF EXISTS clientes;

CREATE TABLE IF NOT EXISTS usuarios(
    id_usuario BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    tipo_perfil,
    senha VARCHAR(255) NOT NULL
    status ENUM ('Ativo', 'Inativo') DEFAULT 'Ativo',

    funcao_id BIGINT UNSIGNED NOT NULL

    -- logs
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENTE_TIMESTAMP
        ON UPDATE CURRENTE_TIMESTAMP,

    -- Cria o relacionamento entre tabelas
    CONSTRAINT fk_usuario_funcao
    FOREIGN KEY (funcao_id) REFERENCES funcoes (id_funcao)
)

