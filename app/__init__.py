from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from .config import Config 
import os 

# instância global do banco de dados, sem acoplamento imediato a aplicação
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    from .routes import register_routes
    register_routes(app)

    return app