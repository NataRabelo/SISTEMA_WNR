from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # importar e registrar os blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.client_routes import client_bp
    from app.routes.referral_routes import Encaminhamento_bp
    from app.routes.financial_routes import financial_bp
    from app.routes.guide_routes import guide_bp
    from app.routes.main_routes import main_bp
    from app.routes.professional_routes import professional_bp
    from app.routes.report_routes import report_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(Encaminhamento_bp)
    app.register_blueprint(financial_bp)
    app.register_blueprint(guide_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(professional_bp)
    app.register_blueprint(report_bp)

    return app