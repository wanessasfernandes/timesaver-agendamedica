import os 

# define o diretório raiz para garantir a resolução de caminhos independente de onde o script é executado
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    # utiliza variáveis de ambiente por segurança, com fallback exclusivo para ambiente local
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-mude-em-producao")
    
    db_path = os.path.join(BASE_DIR, "instance", "agenda.db").replace("\\", "/")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{db_path}")
    # desativa para economizar recursos de memória, seguindo melhores práticas 
    SQLALCHEMY_TRACK_MODIFICATIONS = False