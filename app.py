
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# ==========================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ==========================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-projeto-todo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==========================================
# T07: MODELO CONTATO
# ==========================================
class Contato(db.Model):
    __tablename__ = 'contatos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)

    # Permite acessar as tarefas associadas a este contato (cascade remove tarefas se o contato for apagado).
    tarefas = db.relationship('Tarefa', backref='responsavel', lazy=True, cascade="all, delete-orphan")
    

    def __repr__(self):
        return f'<Contato {self.nome}>'


# ==========================================
# T08: MODELO TAREFA
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

    # Vincula cada tarefa a um contato.
    contato_id = db.Column(
        db.Integer,
        db.ForeignKey('contatos.id'),
        nullable=False
    )

    def __repr__(self):
        return f'<Tarefa {self.descricao}>'


# ==========================================
# T22: LISTAGEM DE TAREFAS (ROTA INICIAL)
# ==========================================
@app.route('/')
def index():
    # Consulta todas as tarefas no banco de dados e envia para o HTML
     lista_tarefas = Tarefa.query.all()
     return render_template('index.html', tarefas=lista_tarefas)


# ==========================================
# T18 & T19: ROTAS DE CONTATOS (CRIAR E LISTAR)
# ==========================================
@app.route('/contatos', methods=['GET', 'POST'])
def contatos():
    if request.method == 'POST':
        # Obtém os dados e remove espaços das extremidades.
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        # Valida o campo obrigatório.
        if not nome:
            flash('O campo Nome é obrigatório!', 'danger')
            return redirect(url_for('contatos'))

        try:
            # Campos opcionais vazios são armazenados como None.
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

    # GET: consulta os contatos para exibi-los na página.
    lista_contatos = Contato.query.all()

    return render_template(
        'contatos.html',
        contatos=lista_contatos
    )

# ==========================================
# T20: EXCLUSÃO DE CONTATOS
# ==========================================
@app.route('/excluir_contato/<int:id>')
def excluir_contato(id):
    contato = Contato.query.get_or_404(id)
    try:
        db.session.delete(contato)
        db.session.commit()
        flash('Contato excluído com sucesso!', 'success')
    except Exception:
        db.session.rollback()
        flash('Erro ao excluir contato.', 'danger')
    return redirect(url_for('contatos'))

# ==========================================
# T21: CADASTRO DE TAREFAS
# ==========================================
@app.route('/nova_tarefa', methods=['GET', 'POST'])
def nova_tarefa():
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        prazo_str = request.form.get('prazo')
        prioridade = request.form.get('prioridade')
        status = request.form.get('status')
        contato_id = request.form.get('contato_id')

        if not descricao or not contato_id or not prazo_str:
            flash('Descrição, prazo e responsável são obrigatórios!', 'danger')
            return redirect(url_for('nova_tarefa'))

        try:
            # Converte a data que vem do HTML em texto (YYYY-MM-DD) para um formato de Data do Python
            prazo_date = datetime.strptime(prazo_str, '%Y-%m-%d').date()

            nova_tarefa = Tarefa(
                descricao=descricao,
                prazo=prazo_date,
                prioridade=prioridade,
                status=status,
                contato_id=int(contato_id)
            )
            db.session.add(nova_tarefa)
            db.session.commit()
            flash('Tarefa cadastrada com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            app.logger.exception('Erro ao cadastrar tarefa')
            flash('Erro ao salvar a tarefa no banco de dados.', 'danger')
            return redirect(url_for('nova_tarefa'))

    # Para a página carregar, buscamos os contatos para o usuário poder escolher o responsável
    lista_contatos = Contato.query.all()
    return render_template('nova_tarefa.html', contatos=lista_contatos)
# ==========================================
# T23: EXCLUSÃO DE TAREFAS
# ==========================================
@app.route('/excluir_tarefa/<int:id>')
def excluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    try:
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa excluída com sucesso!', 'success')
    except Exception:
        db.session.rollback()
        flash('Erro ao excluir tarefa.', 'danger')
    return redirect(url_for('index'))

# ==========================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
