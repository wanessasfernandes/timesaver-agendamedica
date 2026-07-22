import pytest
from app import create_app, db
from app.models import Usuario, Agendamento
from datetime import date


@pytest.fixture
def app():
    application = create_app(test_config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with application.app_context():
        db.create_all()

        usuario = Usuario(username="teste")
        usuario.set_senha("teste123")
        db.session.add(usuario)

        agendamento = Agendamento(
            paciente="Maria Souza",
            cpf="123.456.789-00",
            medico="Dr. Carlos Lima",
            especialidade="Cardiologia",
            data=date(2026, 8, 3),
            horario="09:00",
            convenio="Unimed",
            status="confirmado",
        )
        db.session.add(agendamento)
        db.session.commit()

        yield application

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()