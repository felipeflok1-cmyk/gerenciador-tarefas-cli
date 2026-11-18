# Gerenciador de Tarefas (CLI)

Aplicação de linha de comando para organizar tarefas em projetos, feita em
Python com SQLite. Projeto de estudo focado em modelagem de dados, organização
de código em camadas e tratamento de erros.

## Funcionalidades

- Criar tarefas com título, descrição, prioridade (baixa, média, alta) e prazo
- Listar tarefas, com filtro por status (pendentes ou concluídas) e por projeto
- Ver os detalhes completos de uma tarefa
- Editar e concluir tarefas
- Excluir tarefas, com confirmação
- Criar, listar e excluir projetos
- Ao excluir um projeto, as tarefas dele são excluídas junto (com confirmação
  que informa quantas tarefas serão apagadas)
- Tarefas podem existir sem projeto
- Os dados ficam salvos entre execuções

## Tecnologias

- Python 3.8+
- SQLite (módulo `sqlite3` da biblioteca padrão, sem dependências externas)

## Como executar

```bash
cd CLI
python3 main.py
```

O arquivo do banco (`banco/banco_de_dados.db`) é criado automaticamente na
primeira execução.

## Exemplo de uso

```
=== GERENCIADOR DE TAREFAS ===

1. Nova tarefa
2. Listar tarefas
3. Ver detalhes da tarefa
4. Editar tarefa
5. Concluir tarefa
6. Excluir tarefa
7. Gerenciar projetos
0. Sair

Escolha uma opção: 1
Título da tarefa: Estudar SQLite
Descrição (Enter para pular): Revisar chaves estrangeiras
Prioridade (baixa/media/alta) [media]: alta
Prazo (dd/mm/aaaa, Enter para pular): 20/11/2026
Tarefa criada com o id 1.
```

## Estrutura do projeto

```
CLI/
├── main.py                  # ponto de entrada
├── requirements.txt
├── banco/
│   ├── database.py          # conexão e criação das tabelas
│   ├── projetos.py          # consultas SQL de projetos
│   └── tarefas.py           # consultas SQL de tarefas
└── interface/
    ├── entrada.py           # leitura e validação do que o usuário digita
    ├── menu.py              # menu principal e ações de tarefas
    └── menu_projetos.py     # submenu de projetos
```

O código é dividido em camadas: o pacote `interface` cuida apenas da conversa
com o usuário e nunca escreve SQL; o pacote `banco` cuida apenas do acesso aos
dados e nunca usa `input()` ou `print()`.

## Modelo de dados

**projetos**: `id`, `nome` (obrigatório e único)

**tarefas**: `id`, `titulo` (obrigatório), `descricao`, `prioridade`
(`baixa`, `media` ou `alta`), `status` (`pendente` ou `concluida`), `prazo`,
`criada_em`, `projeto_id` (opcional, chave estrangeira para `projetos`)

Decisões de modelagem:

- Prioridade e status são restritos por `CHECK`, então o próprio banco recusa
  valores inválidos.
- A chave estrangeira usa `ON DELETE CASCADE`. O SQLite mantém chaves
  estrangeiras desligadas por padrão, por isso `PRAGMA foreign_keys = ON` é
  executado em toda conexão.
- Datas são guardadas como texto no formato `AAAA-MM-DD`. O usuário digita
  `dd/mm/aaaa` e o programa converte.
- Todas as consultas usam parâmetros (`?`), o que evita SQL injection, inclusive
  nos filtros dinâmicos.

## Limitações conhecidas

- Os filtros por status e por projeto não podem ser combinados pela interface
  (o banco já suporta).
- Na edição, não é possível limpar a descrição ou o prazo, nem trocar o projeto
  de uma tarefa.
- A data de criação é exibida em UTC.

## Ideias para evolução

- Testes automatizados com `pytest`
- Expor o mesmo banco por uma API (FastAPI)
- Exportação para CSV
- Subtarefas e tarefas recorrentes