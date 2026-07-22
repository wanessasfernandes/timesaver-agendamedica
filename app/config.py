import os 
from pathlib import Path 

# define o diretório raiz para garantir a resolução de caminhos independente de onde o script é executado
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    # utiliza variáveis de ambiente por segurança, com fallback exclusivo para ambiente local
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-mude-em-producao")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{(BASE_DIR / 'instance' / 'agenda.db').as_posix()}"
    )

    # desativa para economizar recursos de memória, seguindo melhores práticas 
    SQLALCHEMY_TRACK_MODIFICATIONS = False