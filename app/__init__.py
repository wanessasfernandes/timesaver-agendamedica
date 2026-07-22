from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from .config import Config 
import os 

# instância global do banco de dados, sem acoplamento imediato a aplicação
db = SQLAlchemy()

def create_app(): 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    print("DB URI em uso:", app.config["SQLALCHEMY_DATABASE_URI"])

    # importação aninhada para evitar importação circular entre rotas e a instância do app 
    from .routes import register_routes 
    register_routes(app)

    return app 