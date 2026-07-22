from flask import render_template, request, redirect, url_for, jsonify
from .models import Usuario, Agendamento

def register_routes(app): 

    @app.route("/")
    def index():
        return redirect(url_for("login"))
    
    @app.route("/login", methods=["GET", "POST"])
    def login(): 
        # TODO: implementar renderização do template HTML e validação via banco de dados 
        return "Tela de Login em construção"
    
    @app.route("/api/agendamentos", methods=["GET"])
    def api_agendamentos(): 
        # endpoint interno que simula a API externa 
        agendamentos = Agendamento.query_all()

        # retorna todos os agendamentos mockados no formato JSON
        return jsonify([agendamentos.to_dict() for agendamentos in agendamentos]) 