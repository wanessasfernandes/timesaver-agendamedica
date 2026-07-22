from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 
from app import db

class Usuario(db.Model): 
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    def set_senha(self, senha_texto_puro):
        # armazena apenas o hash criptográfico, nunca a senha em texto plano 
        self.senha_hash = generate_password_hash(senha_texto_puro)
    
    def verificar_senha(self, senha_texto_puro):
        return check_password_hash(self.senha_hash, senha_texto_puro)
    
    def __repr__(self): 
        return f"<Usuario {self.username}>"

class Agendamento(db.Model): 
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    paciente = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    medico = db.Column(db.String(120), nullable=False)
    especialidade = db.Column(db.String(80), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    convenio = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pendente")

    def to_dict(self): 
        # serializa o objeto para JSON, facilitando o consumo via requisições HTTP (API mockada)
        return {
            "id": self.id,
            "paciente": self.paciente,
            "cpf": self.cpf,
            "medico": self.medico,
            "especialidade": self.especialidade,
            "data": self.data.isoformat() if self.data else None, 
            "horario": self.horario,
            "convenio": self.convenio,
            "status": self.status
        }

    def __repr__(self):
        return f"<Agendamento {self.paciente} - {self.data}>"