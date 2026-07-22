import logging
from functools import wraps
from flask import (
    render_template, request, redirect, url_for,
    jsonify, session, flash
)
from sqlalchemy.exc import SQLAlchemyError
from .models import Usuario, Agendamento

logger = logging.getLogger(__name__)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Você precisa fazer login para continuar.", "error")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper


def register_routes(app):

    @app.route("/")
    def index():
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not username or not password:
                flash("Preencha usuário e senha.", "error")
                return redirect(url_for("login"))

            try:
                usuario = Usuario.query.filter_by(username=username).first()
            except SQLAlchemyError:
                logger.exception("Erro de conexão com o banco durante o login")
                flash("Erro ao acessar o sistema. Tente novamente em instantes.", "error")
                return redirect(url_for("login"))

            if not usuario or not usuario.verificar_senha(password):
                logger.warning("Tentativa de login invalida para username=%s", username)
                flash("Usuário ou senha incorretos.", "error")
                return redirect(url_for("login"))

            session["usuario_id"] = usuario.id
            logger.info("Login bem-sucedido para username=%s", username)
            return redirect(url_for("agenda"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/agenda")
    @login_required
    def agenda():
        return render_template("agenda.html")

    @app.route("/api/agendamentos", methods=["GET"])
    @login_required
    def api_agendamentos():
        busca = request.args.get("busca", "").strip()

        try:
            query = Agendamento.query
            if busca:
                termo = f"%{busca}%"
                query = query.filter(
                    (Agendamento.paciente.ilike(termo)) |
                    (Agendamento.cpf.ilike(termo)) |
                    (Agendamento.medico.ilike(termo))
                )
            agendamentos = query.all()

        except SQLAlchemyError:
            logger.exception("Erro de conexão com o banco ao buscar agendamentos")
            return jsonify({"erro": "Não foi possível carregar os agendamentos no momento."}), 503

        if not agendamentos:
            logger.info("Nenhum agendamento encontrado para busca='%s'", busca)
            return jsonify([])

        return jsonify([a.to_dict() for a in agendamentos])