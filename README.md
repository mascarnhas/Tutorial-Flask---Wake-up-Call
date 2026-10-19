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

## Regras de funcionamento

- **Status selecionáveis:** `A fazer`, `Fazendo` e `Concluída`.
- **Atraso automático:** uma tarefa não concluída cujo prazo já passou é exibida como `Atrasada`. Esse estado é calculado pela aplicação, não selecionado manualmente.
- **Identificação visual:** cada status possui uma cor própria: cinza para tarefas a fazer, amarelo para tarefas em andamento, verde para concluídas e vermelho para atrasadas.
- **Prazos:** a aplicação destaca tarefas que vencem hoje, amanhã ou que já venceram.
- **Exclusão segura:** a exclusão de tarefas e contatos utiliza requisições POST. Contatos vinculados a tarefas não podem ser excluídos.
- **Responsáveis:** cada tarefa é vinculada a um contato cadastrado.

## Testes e validações

Durante a validação do protótipo, foram verificados:

- Acesso às páginas de contatos, tarefas e dashboard.
- Cadastro, edição e exclusão de contatos e tarefas.
- Validação de campos obrigatórios e dados inválidos.
- Associação entre tarefas e contatos.
- Cálculo e apresentação de tarefas atrasadas.
- Proteção contra exclusão de contatos vinculados a tarefas.
- Respostas adequadas para operações de exclusão inválidas.
- Sintaxe do arquivo Python e consistência das dependências.

Os testes funcionais foram executados em uma cópia temporária do projeto para evitar alterações no banco de dados original.

## Colaboração e controle de versão

- A branch `main` representa a versão principal do repositório.
- A branch `dev` é utilizada para integrar e validar as funcionalidades antes da entrega.
- As alterações devem ser registradas em commits pequenos, com mensagens descritivas.
- Antes da integração final, o código e os requisitos da atividade devem ser revisados.
- Alterações feitas por integrantes diferentes devem ser integradas e verificadas para evitar regressões.

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

Projeto colaborativo desenvolvido para praticar desenvolvimento web, persistência de dados, organização de funcionalidades e uso do Git em equipe, realizado como parte da disciplina Fundamentos de Sistemas de Informações.
Este projeto colaborativo foi desenvolvido com o objetivo de proporcionar aos participantes a oportunidade de praticar e consolidar conhecimentos relacionados ao desenvolvimento web, à persistência de dados e à organização de funcionalidades, além de estimular o uso do Git em equipe como ferramenta essencial para o controle de versões e a integração de trabalhos. A iniciativa, realizada em grupo, busca não apenas exercitar aspectos técnicos, mas também promover a experiência de trabalho colaborativo e a vivência de metodologias de desenvolvimento. Este trabalho integra as atividades da disciplina Fundamentos de Sistemas de Informações, contribuindo para a formação prática e teórica dos estudantes na área de tecnologia da informação.
