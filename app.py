
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError


# ==========================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ==========================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-projeto-todo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==========================================
# PROTEÇÃO DE CHAVES ESTRANGEIRAS SQLITE
# ==========================================
with app.app_context():

    @event.listens_for(db.engine, 'connect')
    def ativar_chaves_estrangeiras(dbapi_connection, connection_record):
        if dbapi_connection.__class__.__module__.startswith('sqlite3'):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute('PRAGMA foreign_keys=ON')
            finally:
                cursor.close()


# ==========================================
# MODELO DE CONTATO
# ==========================================
class Contato(db.Model):
    __tablename__ = 'contatos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)

    # Não permite excluir contatos automaticamente
    # quando existem tarefas vinculadas.
    tarefas = db.relationship('Tarefa', backref='responsavel', lazy=True)

    def __repr__(self):
        return f'<Contato {self.nome}>'


# ==========================================
# MODELO TAREFA
# ==========================================
class Tarefa(db.Model):
    __tablename__ = 'tarefas'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    prazo = db.Column(db.Date, nullable=False)
    prioridade = db.Column(
        db.String(20), nullable=False, default='Média'
    )
    status = db.Column(
        db.String(20), nullable=False, default='A fazer'
    )

    contato_id = db.Column(
        db.Integer,
        db.ForeignKey('contatos.id', ondelete='RESTRICT'),
        nullable=False
    )

    @property
    def status_exibicao(self):
        # Uma tarefa vencida e não concluída aparece como atrasada.
        # O status armazenado no banco permanece inalterado.
        if (
            self.prazo
            and self.prazo < date.today()
            and self.status != 'Concluída'
        ):
            return 'Atrasada'

        return self.status

    def __repr__(self):
        return f'<Tarefa {self.descricao}>'


# ==========================================
# ROTA INICIAL
# ==========================================
@app.route('/')
def home():
    return redirect(url_for('tarefas'))

# ==========================================
# CONTATOS: CRIAR E LISTAR
# ==========================================
@app.route('/contatos', methods=['GET', 'POST'])
def contatos():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        if not nome:
            flash('O campo Nome é obrigatório!', 'danger')
            return redirect(url_for('contatos'))

        try:
            novo_contato = Contato(
                nome=nome,
                email=email if email else None,
                telefone=telefone if telefone else None
            )

            db.session.add(novo_contato)
            db.session.commit()

            flash('Contato cadastrado com sucesso!', 'success')

        except Exception:
            db.session.rollback()
            app.logger.exception('Erro ao cadastrar contato')
            flash(
                'Erro ao salvar o contato no banco de dados.',
                'danger'
            )

        # PRG: redireciona após o envio do formulário.
        return redirect(url_for('contatos'))

    lista_contatos = Contato.query.all()

    return render_template(
        'contatos.html',
        contatos=lista_contatos
    )


# ==========================================
# CONTATOS: EXCLUSÃO PROTEGIDA
# ==========================================
@app.route('/contatos/<int:id>/excluir', methods=['POST'])
def excluir_contato(id):
    contato = db.session.get(Contato, id)

    if contato is None:
        flash('Contato não encontrado.', 'warning')
        return redirect(url_for('contatos'))

    # Não permite excluir contatos com tarefas vinculadas.
    if contato.tarefas:
        flash(
            'Não é possível excluir este contato porque existem tarefas vinculadas a ele.',
            'danger'
        )
        return redirect(url_for('contatos'))

    try:
        db.session.delete(contato)
        db.session.commit()
        flash('Contato excluído com sucesso!', 'success')

    except IntegrityError:
        db.session.rollback()
        app.logger.exception(
            'O banco impediu a exclusão do contato %s por integridade referencial.',
            id
        )
        flash(
            'Não foi possível excluir o contato porque há registros vinculados.',
            'danger'
        )

    return redirect(url_for('contatos'))


# ==========================================
# TAREFAS: CRIAR E LISTAR
# ==========================================
@app.route('/tarefas', methods=['GET', 'POST'])
def tarefas():
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        prazo_texto = request.form.get('prazo', '').strip()
        prioridade = request.form.get('prioridade', '').strip()
        status = request.form.get('status', '').strip()
        contato_texto = request.form.get('contato_id', '').strip()

        # Valida a descrição.
        if not descricao:
            flash('A descrição da tarefa é obrigatória.', 'danger')
            return redirect(url_for('tarefas'))

        if len(descricao) > 255:
            flash('A descrição deve ter no máximo 255 caracteres.', 'danger')
            return redirect(url_for('tarefas'))

        # Converte a data.
        try:
            prazo = date.fromisoformat(prazo_texto)
        except ValueError:
            flash('Informe um prazo válido.', 'danger')
            return redirect(url_for('tarefas'))

        # Valida prioridade e status.
        prioridades_validas = {'Baixa', 'Média', 'Alta'}
        status_validos = {'A fazer', 'Fazendo', 'Concluída'}

        if prioridade not in prioridades_validas:
            flash('Selecione uma prioridade válida.', 'danger')
            return redirect(url_for('tarefas'))

        if status not in status_validos:
            flash('Selecione um status válido.', 'danger')
            return redirect(url_for('tarefas'))

        # Converte e verifica o contato responsável.
        try:
            contato_id = int(contato_texto)
        except ValueError:
            flash('Selecione um contato responsável válido.', 'danger')
            return redirect(url_for('tarefas'))

        contato = db.session.get(Contato, contato_id)

        if contato is None:
            flash('O contato selecionado não existe.', 'danger')
            return redirect(url_for('tarefas'))

        # Cria e salva a tarefa.
        try:
            nova_tarefa = Tarefa(
                descricao=descricao,
                prazo=prazo,
                prioridade=prioridade,
                status=status,
                contato_id=contato.id
            )

            db.session.add(nova_tarefa)
            db.session.commit()

            flash('Tarefa cadastrada com sucesso!', 'success')

        except IntegrityError:
            db.session.rollback()
            app.logger.exception('Erro de integridade ao cadastrar tarefa')
            flash(
                'Não foi possível salvar a tarefa. Confira os dados e tente novamente.',
                'danger'
            )

        # PRG: redireciona após o envio do formulário.
        return redirect(url_for('tarefas'))

    # GET: carrega as tarefas e os contatos.
    lista_tarefas = Tarefa.query.order_by(Tarefa.prazo.asc()).all()
    lista_contatos = Contato.query.order_by(Contato.nome.asc()).all()

    return render_template(
        'tarefas.html',
        tarefas=lista_tarefas,
        contatos=lista_contatos,
        hoje=date.today()
    )


# ==========================================
# TAREFAS: EDITAR
# ==========================================
@app.route('/tarefas/<int:id>/editar', methods=['GET', 'POST'])
def editar_tarefa(id):
    tarefa = db.session.get(Tarefa, id)

    if tarefa is None:
        flash('Tarefa não encontrada.', 'danger')
        return redirect(url_for('tarefas'))

    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        prazo_texto = request.form.get('prazo', '').strip()
        prioridade = request.form.get('prioridade', '').strip()
        status = request.form.get('status', '').strip()
        contato_texto = request.form.get('contato_id', '').strip()

        if not descricao or len(descricao) > 255:
            flash(
                'A descrição é obrigatória e deve ter no máximo 255 caracteres.',
                'danger'
            )
            return redirect(url_for('editar_tarefa', id=id))

        try:
            prazo = date.fromisoformat(prazo_texto)
        except ValueError:
            flash('Informe um prazo válido.', 'danger')
            return redirect(url_for('editar_tarefa', id=id))

        if prioridade not in {'Baixa', 'Média', 'Alta'}:
            flash('Selecione uma prioridade válida.', 'danger')
            return redirect(url_for('editar_tarefa', id=id))

        if status not in {'A fazer', 'Fazendo', 'Concluída'}:
            flash('Selecione um status válido.', 'danger')
            return redirect(url_for('editar_tarefa', id=id))

        try:
            contato_id = int(contato_texto)
        except ValueError:
            flash('Selecione um contato responsável válido.', 'danger')
            return redirect(url_for('editar_tarefa', id=id))

        contato = db.session.get(Contato, contato_id)

        if contato is None:
            flash('O contato selecionado não existe.', 'danger')
            return redirect(url_for('editar_tarefa', id=id))

        try:
            tarefa.descricao = descricao
            tarefa.prazo = prazo
            tarefa.prioridade = prioridade
            tarefa.status = status
            tarefa.contato_id = contato.id

            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect(url_for('tarefas'))

        except IntegrityError:
            db.session.rollback()
            app.logger.exception('Erro de integridade ao editar tarefa %s', id)
            flash('Não foi possível atualizar a tarefa.', 'danger')
            return redirect(url_for('editar_tarefa', id=id))

    contatos = Contato.query.order_by(Contato.nome.asc()).all()

    return render_template(
        'editar_tarefa.html',
        tarefa=tarefa,
        contatos=contatos
    )

# ==========================================
# TAREFAS: EXCLUIR
# ==========================================
@app.route('/tarefas/<int:id>/excluir', methods=['POST'])
def excluir_tarefa(id):
    tarefa = db.session.get(Tarefa, id)

    if tarefa is None:
        flash('Tarefa não encontrada.', 'warning')
        return redirect(url_for('tarefas'))

    try:
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa excluída com sucesso!', 'success')

    except IntegrityError:
        db.session.rollback()
        app.logger.exception('Erro de integridade ao excluir tarefa %s', id)
        flash('Não foi possível excluir a tarefa.', 'danger')

    return redirect(url_for('tarefas'))

# ==========================================
# DASHBOARD: CONTAGEM POR STATUS
# ==========================================
@app.route('/dashboard')
def dashboard():
    lista_tarefas = Tarefa.query.all()

    # Todos os status começam em zero, inclusive quando
    # ainda não há tarefas cadastradas.
    contagem = {
        'A fazer': 0,
        'Fazendo': 0,
        'Concluída': 0,
        'Atrasada': 0
    }

    # Conta o status calculado para reconhecer tarefas vencidas.
    for tarefa in lista_tarefas:
        status = tarefa.status_exibicao
        contagem[status] += 1

    return render_template(
        'dashboard.html',
        contagem=contagem
    )


# ==========================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
