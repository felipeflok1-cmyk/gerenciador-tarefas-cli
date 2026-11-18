from banco.database import conectar


def adicionar_tarefa(titulo, descricao=None, prioridade="media", prazo=None, projeto_id=None):
    with conectar() as conn:
        cursor = conn.execute(
            "INSERT INTO tarefas (titulo, descricao, prioridade, prazo, projeto_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (titulo, descricao, prioridade, prazo, projeto_id),
        )
        return cursor.lastrowid


def listar_tarefas(status=None, projeto_id=None):
    sql = """
        SELECT t.id, t.status, t.prioridade, t.prazo, p.nome, t.titulo
        FROM tarefas t
        LEFT JOIN projetos p ON p.id = t.projeto_id
    """
    condicoes = []
    parametros = []

    if status is not None:
        condicoes.append("t.status = ?")
        parametros.append(status)

    if projeto_id is not None:
        condicoes.append("t.projeto_id = ?")
        parametros.append(projeto_id)

    if condicoes:
        sql += " WHERE " + " AND ".join(condicoes)

    sql += " ORDER BY t.id"

    with conectar() as conn:
        return conn.execute(sql, parametros).fetchall()


def concluir_tarefa(id_tarefa):
    with conectar() as conn:
        cursor = conn.execute(
            "UPDATE tarefas SET status = 'concluida' WHERE id = ?",
            (id_tarefa,),
        )
        return cursor.rowcount > 0


def buscar_tarefa(id_tarefa):
    with conectar() as conn:
        return conn.execute(
            "SELECT id, titulo, descricao, prioridade, prazo FROM tarefas WHERE id = ?",
            (id_tarefa,),
        ).fetchone()


def atualizar_tarefa(id_tarefa, titulo, descricao, prioridade, prazo):
    with conectar() as conn:
        cursor = conn.execute(
            "UPDATE tarefas "
            "SET titulo = ?, descricao = ?, prioridade = ?, prazo = ? "
            "WHERE id = ?",
            (titulo, descricao, prioridade, prazo, id_tarefa),
        )
        return cursor.rowcount > 0


def buscar_detalhes(id_tarefa):
    with conectar() as conn:
        return conn.execute(
            """
            SELECT t.id, t.titulo, t.descricao, t.status, t.prioridade,
                   t.prazo, t.criada_em, p.nome
            FROM tarefas t
            LEFT JOIN projetos p ON p.id = t.projeto_id
            WHERE t.id = ?
            """,
            (id_tarefa,),
        ).fetchone()


def excluir_tarefa(id_tarefa):
    with conectar() as conn:
        cursor = conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
        return cursor.rowcount > 0