from banco.database import conectar


def adicionar_projeto(nome):
    with conectar() as conn:
        cursor = conn.execute("INSERT INTO projetos (nome) VALUES (?)", (nome,))
        return cursor.lastrowid


def listar_projetos():
    with conectar() as conn:
        return conn.execute("SELECT id, nome FROM projetos ORDER BY nome").fetchall()


def buscar_projeto(id_projeto):
    with conectar() as conn:
        return conn.execute(
            "SELECT id, nome FROM projetos WHERE id = ?",
            (id_projeto,),
        ).fetchone()


def contar_tarefas(id_projeto):
    with conectar() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM tarefas WHERE projeto_id = ?",
            (id_projeto,),
        ).fetchone()[0]


def excluir_projeto(id_projeto):
    with conectar() as conn:
        cursor = conn.execute("DELETE FROM projetos WHERE id = ?", (id_projeto,))
        return cursor.rowcount > 0