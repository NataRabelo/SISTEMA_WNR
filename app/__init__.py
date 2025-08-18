from app.utils.editor_valor import format_currency
from config import DevelopmentConfig
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask import Flask

from app.extensions import db

migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

from app.models import Usuario

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    bcrypt.init_app(app)

    app.jinja_env.filters['currency'] = format_currency

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
