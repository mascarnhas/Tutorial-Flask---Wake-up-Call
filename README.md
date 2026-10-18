# Wake-up Call — Gerenciador de Tarefas

Aplicação web de gerenciamento de tarefas desenvolvida em Python com Flask e SQLite, como projeto acadêmico da disciplina de Fundamentos de Sistemas de Informação.

## Funcionalidades

- **Gerenciamento de contatos:** cadastrar, listar e excluir contatos.
- **Gerenciamento de tarefas:** cadastrar, listar, editar e excluir tarefas.
- **Responsáveis:** associar cada tarefa a um contato cadastrado.
- **Prazos:** definir uma data limite para cada tarefa.
- **Prioridades:** classificar tarefas como baixa, média ou alta.
- **Status:** acompanhar tarefas a fazer, em andamento ou concluídas.
- **Identificação de atrasos:** destacar automaticamente tarefas com prazo vencido que ainda não foram concluídas.
- **Dashboard:** visualizar a quantidade de tarefas por status.

## Tecnologias

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2
- HTML e CSS
- Bootstrap 5.3.0

## Estrutura do projeto

```text
Tutorial-Flask---Wake-up-Call/
├── app.py
├── requirements.txt
├── README.md
└── templates/
    ├── base.html
    ├── contatos.html
    ├── tarefas.html
    ├── _form_tarefa.html
    ├── _macros.html
    ├── editar_tarefa.html
    └── dashboard.html
```

## Instalação e execução

### 1. Pré-requisitos

- Python 3 instalado.
- Git instalado.
- Conexão com a internet para carregar os arquivos do Bootstrap via CDN.

### 2. Clonar o repositório

```bash
git clone https://github.com/mascarnhas/Tutorial-Flask---Wake-up-Call.git
cd Tutorial-Flask---Wake-up-Call
```

### 3. Criar e ativar o ambiente virtual

No Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação

```bash
python app.py
```

Abra no navegador o endereço local informado pelo Flask, normalmente:

http://127.0.0.1:5000

Na inicialização, a aplicação utiliza `db.create_all()` para criar as tabelas que ainda não existirem no banco SQLite. Esse mecanismo não substitui automaticamente tabelas existentes quando o modelo de dados muda.

## Organização do código

O arquivo `app.py` concentra os modelos de dados, as rotas e a lógica de negócio. Os arquivos da pasta `templates/` definem as páginas renderizadas pelo Flask, reutilizando a estrutura visual e os componentes compartilhados.

O Bootstrap 5.3.0 é carregado por CDN, enquanto o SQLite é utilizado para persistir os dados da aplicação.

## Contexto acadêmico

Projeto colaborativo desenvolvido para praticar desenvolvimento web, persistência de dados, organização de funcionalidades e uso do Git em equipe.
