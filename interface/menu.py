import sqlite3

from banco.tarefas import (
    adicionar_tarefa,
    listar_tarefas,
    concluir_tarefa,
    buscar_tarefa,
    atualizar_tarefa,
    buscar_detalhes,
    excluir_tarefa,
)
from banco.projetos import listar_projetos, buscar_projeto
from interface.entrada import pedir_texto, pedir_prioridade, pedir_prazo, pedir_inteiro
from interface.menu_projetos import submenu_projetos


def mostrar_menu():
    print("\n=== GERENCIADOR DE TAREFAS ===\n")
    print("1. Nova tarefa")
    print("2. Listar tarefas")
    print("3. Ver detalhes da tarefa")
    print("4. Editar tarefa")
    print("5. Concluir tarefa")
    print("6. Excluir tarefa")
    print("7. Gerenciar projetos")
    print("0. Sair\n")


def escolher_projeto():
    projetos = listar_projetos()

    if not projetos:
        return None

    print("\nProjetos disponíveis:")
    for id_, nome in projetos:
        print(f"  {id_} - {nome}")

    while True:
        valor = input("Id do projeto (Enter para nenhum): ").strip()

        if not valor:
            return None

        try:
            id_projeto = int(valor)
        except ValueError:
            print("Digite um número válido.")
            continue

        if buscar_projeto(id_projeto) is not None:
            return id_projeto

        print("Nenhum projeto com esse id.")


def nova_tarefa():
    titulo = pedir_texto("Título da tarefa: ")
    descricao = pedir_texto("Descrição (Enter para pular): ", obrigatorio=False)
    prioridade = pedir_prioridade()
    prazo = pedir_prazo()
    projeto_id = escolher_projeto()

    id_criado = adicionar_tarefa(titulo, descricao, prioridade, prazo, projeto_id)
    print(f"Tarefa criada com o id {id_criado}.")


def listar():
    print("\nMostrar:")
    print("1. Todas")
    print("2. Pendentes")
    print("3. Concluídas")
    print("4. De um projeto")
    opcao = input("Escolha: ").strip()

    status = None
    projeto_id = None

    if opcao == "1":
        pass
    elif opcao == "2":
        status = "pendente"
    elif opcao == "3":
        status = "concluida"
    elif opcao == "4":
        projeto_id = escolher_projeto()
        if projeto_id is None:
            print("Nenhum projeto selecionado.")
            return
    else:
        print("Opção inválida.")
        return

    tarefas = listar_tarefas(status, projeto_id)

    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return

    print(f"\n{'ID':<5}{'Status':<12}{'Prioridade':<12}{'Prazo':<13}{'Projeto':<12}Título")

    for id_, status_tarefa, prioridade, prazo, projeto, titulo in tarefas:
        print(
            f"{id_:<5}{status_tarefa:<12}{prioridade:<12}"
            f"{prazo or '-':<13}{projeto or '-':<12}{titulo}"
        )


def ver_detalhes():
    id_tarefa = pedir_inteiro("Id da tarefa: ")
    tarefa = buscar_detalhes(id_tarefa)

    if tarefa is None:
        print("Nenhuma tarefa com esse id.")
        return

    id_, titulo, descricao, status, prioridade, prazo, criada_em, projeto = tarefa

    print(f"\nTarefa #{id_}")
    print(f"Título:     {titulo}")
    print(f"Descrição:  {descricao or '(sem descrição)'}")
    print(f"Status:     {status}")
    print(f"Prioridade: {prioridade}")
    print(f"Prazo:      {prazo or '-'}")
    print(f"Projeto:    {projeto or '-'}")
    print(f"Criada em:  {criada_em}")


def editar():
    id_tarefa = pedir_inteiro("Id da tarefa a editar: ")
    tarefa = buscar_tarefa(id_tarefa)

    if tarefa is None:
        print("Nenhuma tarefa com esse id.")
        return

    _, titulo_atual, descricao_atual, prioridade_atual, prazo_atual = tarefa

    print("Enter mantém o valor atual.")
    titulo = pedir_texto(f"Título [{titulo_atual}]: ", atual=titulo_atual)
    descricao = pedir_texto(
        f"Descrição [{descricao_atual or 'sem descrição'}]: ",
        obrigatorio=False,
        atual=descricao_atual,
    )
    prioridade = pedir_prioridade(prioridade_atual)
    prazo = pedir_prazo(prazo_atual)

    atualizar_tarefa(id_tarefa, titulo, descricao, prioridade, prazo)
    print("Tarefa atualizada.")


def concluir():
    id_tarefa = pedir_inteiro("Id da tarefa a concluir: ")

    if concluir_tarefa(id_tarefa):
        print("Tarefa concluída.")
    else:
        print("Nenhuma tarefa com esse id.")


def excluir():
    id_tarefa = pedir_inteiro("Id da tarefa a excluir: ")
    tarefa = buscar_tarefa(id_tarefa)

    if tarefa is None:
        print("Nenhuma tarefa com esse id.")
        return

    titulo = tarefa[1]
    resposta = input(f"Excluir a tarefa '{titulo}'? (s/n): ").strip().lower()

    if resposta != "s":
        print("Operação cancelada.")
        return

    excluir_tarefa(id_tarefa)
    print("Tarefa excluída.")


ACOES = {
    "1": nova_tarefa,
    "2": listar,
    "3": ver_detalhes,
    "4": editar,
    "5": concluir,
    "6": excluir,
    "7": submenu_projetos,
}


def iniciar():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Até mais!")
            break

        acao = ACOES.get(opcao)

        if acao is None:
            print("Opção inválida.")
            continue

        try:
            acao()
        except sqlite3.Error as erro:
            print(f"Erro no banco de dados: {erro}")