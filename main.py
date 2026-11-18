from banco.database import criar_tabelas
from interface.menu import iniciar


def main():
    try:
        criar_tabelas()
        iniciar()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()