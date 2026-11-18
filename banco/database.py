import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "banco_de_dados.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS projetos (
    id   INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tarefas (
    id         INTEGER PRIMARY KEY,
    titulo     TEXT NOT NULL,
    descricao  TEXT,
    prioridade TEXT NOT NULL DEFAULT 'media'
               CHECK (prioridade IN ('baixa', 'media', 'alta')),
    status     TEXT NOT NULL DEFAULT 'pendente'
               CHECK (status IN ('pendente', 'concluida')),
    prazo      TEXT,
    criada_em  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    projeto_id INTEGER,
    FOREIGN KEY (projeto_id) REFERENCES projetos (id) ON DELETE CASCADE
);
"""


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas():
    with conectar() as conn:
        conn.executescript(SCHEMA)