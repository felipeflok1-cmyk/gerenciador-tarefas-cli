import sqlite3

from banco.projetos import (
    adicionar_projeto,
    listar_projetos,
    buscar_projeto,
    contar_tarefas,
    excluir_projeto,
)
from interface.entrada import pedir_texto, pedir_inteiro


def novo_projeto():
    nome = pedir_texto("Nome do projeto: ")

    try:
        id_criado = adicionar_projeto(nome)
    except sqlite3.IntegrityError:
        print("Já existe um projeto com esse nome.")
        return

    print(f"Projeto criado com o id {id_criado}.")


def mostrar_projetos():
    projetos = listar_projetos()

    if not projetos:
        print("Nenhum projeto cadastrado.")
        return

    print(f"\n{'ID':<5}Nome")
    for id_, nome in projetos:
        print(f"{id_:<5}{nome}")


def excluir():
    id_projeto = pedir_inteiro("Id do projeto a excluir: ")
    projeto = buscar_projeto(id_projeto)

    if projeto is None:
        print("Nenhum projeto com esse id.")
        return

    nome = projeto[1]
    quantidade = contar_tarefas(id_projeto)

    resposta = input(
        f"O projeto '{nome}' tem {quantidade} tarefa(s). Excluir tudo? (s/n): "
    ).strip().lower()

    if resposta != "s":
        print("Operação cancelada.")
        return

    excluir_projeto(id_projeto)
    print("Projeto excluído.")


def submenu_projetos():
    while True:
        print("\n--- PROJETOS ---\n")
        print("1. Novo projeto")
        print("2. Listar projetos")
        print("3. Excluir projeto")
        print("0. Voltar\n")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            novo_projeto()
        elif opcao == "2":
            mostrar_projetos()
        elif opcao == "3":
            excluir()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")