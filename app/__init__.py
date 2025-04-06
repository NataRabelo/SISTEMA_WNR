from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  # Inicializa o LoginManager
bcrypt = Bcrypt()  # Inicializa o Bcrypt

from app.models import Usuario  # Importe seu modelo de usuário

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))  # Converte para inteiro e busca no banco


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensões com o aplicativo
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'  # Atualize a rota se necessário
    bcrypt.init_app(app)

    # Importar e registrar os blueprints
    from app.routes.autenticadores.autenticador import auth_bp
    from app.routes.cliente.cliente import client_bp
    from app.routes.encaminhamento.encaminhamento import encaminhamento_bp
    from app.routes.guia.guia import guide_bp
    from app.routes.main.main import main_bp
    from app.routes.profissional.profissional import professional_bp
    from app.routes.relatorios.relatorios import report_bp
    from app.routes.utilitares.utilitares import utils_bp
    from app.routes.adiministracao.adiministracao import adm_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(encaminhamento_bp)
    app.register_blueprint(guide_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(professional_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(utils_bp)
    app.register_blueprint(adm_bp)

    return app
