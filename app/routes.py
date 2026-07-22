from flask import render_template, request, redirect, url_for, jsonify
from .models import Usuario, Agendamento

def register_routes(app): 

    @app.route("/")
    def index():
        return redirect(url_for("login"))
    
    @app.route("/login", methods=["GET", "POST"])
    def login(): 
        
        # separa a exibição do formulário do processamento de dados 
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            usuario = Usuario.query.filter_by(username=username).first()

            # validação unificada para evitar ataques de enumeração de usuários
            if not usuario or not usuario.verificar_senha(password): 
                flask("Usuário ou senha incorretos.", "error")
                return redirect(url_for("login"))
            
            # redirecionamento após sucesso da autenticação 
            return redirect(url_for("agenda"))

        return render_template("login.html")
    
    @app.route("/agenda")
    def agenda():
        # garante que o redirecionamento pós-login não quebre a aplicação
        return "Tela de agenda em construção"

    @app.route("/api/agendamentos", methods=["GET"])
    def api_agendamentos(): 
        # endpoint interno que simula a API externa 
        agendamentos = Agendamento.query_all()

        # retorna todos os agendamentos mockados no formato JSON
        return jsonify([agendamentos.to_dict() for agendamentos in agendamentos]) 