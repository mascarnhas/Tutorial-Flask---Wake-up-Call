from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

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
    
    # Relacionamento: Permite acessar contato.tarefas
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
    prioridade = db.Column(db.String(20), nullable=False, default='Média') # Baixa, Média, Alta
    status = db.Column(db.String(20), nullable=False, default='A fazer')   # A fazer, Fazendo, Concluída
    
    # Chave Estrangeira vinculando a Tarefa ao Contato
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'), nullable=False)

    def __repr__(self):
        return f'<Tarefa {self.descricao}>'

# ==========================================
# CRIAÇÃO DO BANCO E ROTA INICIAL DE TESTE
# ==========================================
@app.route('/')
def index():
    return "API do To-Do List rodando com sucesso! Banco configurado."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas sqlite no primeiro boot
    app.run(debug=True)