
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

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

    # Permite acessar as tarefas associadas a este contato.
    tarefas = db.relationship('Tarefa', backref='responsavel', lazy=True)

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
# ROTA INICIAL
# ==========================================
@app.route('/')
def index():
    return "API do To-Do List rodando com sucesso! Banco configurado."


# ==========================================
# T12: ROTAS DE CONTATOS (CRIAR E LISTAR)
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
# INICIALIZAÇÃO DA APLICAÇÃO
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
