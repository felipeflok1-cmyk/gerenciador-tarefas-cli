from datetime import datetime

PRIORIDADES = ("baixa", "media", "alta")


def pedir_texto(mensagem, obrigatorio=True, atual=None):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        if atual is not None:
            return atual          # Enter = manter o valor atual
        if not obrigatorio:
            return None
        print("Este campo é obrigatório.")


def pedir_prioridade(atual="media"):
    while True:
        valor = input(f"Prioridade (baixa/media/alta) [{atual}]: ").strip().lower()
        valor = valor.replace("é", "e")
        if not valor:
            return atual
        if valor in PRIORIDADES:
            return valor
        print("Prioridade inválida. Use baixa, media ou alta.")


def pedir_prazo(atual=None):
    while True:
        valor = input(f"Prazo dd/mm/aaaa [{atual or 'sem prazo'}]: ").strip()
        if not valor:
            return atual
        try:
            data = datetime.strptime(valor, "%d/%m/%Y")
            return data.strftime("%Y-%m-%d")
        except ValueError:
            print("Data inválida. Exemplo: 20/11/2026")


def pedir_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número válido.")