"""
script de seed: cria as tabelas e popula o banco com dados iniciais para desenvolvimento e teste 
(usuario de teste + agendamentos mock)

uso: 
    python seed/seed.py
"""

import sys 
import os 
from datetime import date 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import Usuario, Agendamento

def criar_usuario_teste(): 
    usuario_existente = Usuario.query.filter_by(username="teste").first()
    if usuario_existente:
        print("Usuário de teste já existe, pulando criação.")
        return

    usuario = Usuario(username="teste")
    usuario.set_senha("teste123")
    db.session.add(usuario)
    print("Usuário de teste criado -> usename: teste | senha: teste123")

def criar_agendamento_mock(): 
    if Agendamento.query.first():
        print("Já existem agendamentos no banco, pulando criação")
        return
    
    agendamentos = [
        Agendamento(
            paciente="Maria Souza",
            cpf="123.456.789-00",
            medico="Dr. Carlos Lima",
            especialidade="Cardiologia",
            data=date(2026, 8, 3),
            horario="09:00",
            convenio="Unimed",
            status="confirmado",
        ),
        Agendamento(
            paciente="João Pereira",
            cpf="987.654.321-00",
            medico="Dra. Ana Ribeiro",
            especialidade="Dermatologia",
            data=date(2026, 8, 3),
            horario="10:30",
            convenio="Bradesco Saúde",
            status="pendente",
        ),
        Agendamento(
            paciente="Maria Souza",
            cpf="123.456.789-00",
            medico="Dra. Fernanda Alves",
            especialidade="Nutrição",
            data=date(2026, 8, 5),
            horario="14:00",
            convenio="Unimed",
            status="cancelado",
        ),
        Agendamento(
            paciente="Pedro Santos",
            cpf="111.222.333-44",
            medico="Dr. Carlos Lima",
            especialidade="Cardiologia",
            data=date(2026, 8, 6),
            horario="08:15",
            convenio="Particular",
            status="confirmado",
        ),
        Agendamento(
            paciente="Juliana Costa",
            cpf="555.666.777-88",
            medico="Dr. Rafael Nunes",
            especialidade="Ortopedia",
            data=date(2026, 8, 7),
            horario="11:45",
            convenio="SulAmérica",
            status="pendente",
        ),
        Agendamento(
            paciente="Roberto Almeida",
            cpf="999.888.777-66",
            medico="Dra. Ana Ribeiro",
            especialidade="Dermatologia",
            data=date(2026, 8, 8),
            horario="16:30",
            convenio="Bradesco Saúde",
            status="confirmado",
        ),
    ]

    db.session.add_all(agendamentos)
    print(f"{len(agendamentos)} agendamentos mock criados.")

def run(): 
    app = create_app()
    with app.app_context():
        db.create_all()
        criar_usuario_teste()
        criar_agendamento_mock()
        db.session.commit()
        print("Seed concluído com sucesso.")

if __name__ == "__main__":
    run()