import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = "pt_BR"


class DevelopmentConfig(Config):
    DEBUG = True
    # Banco de dados SQLite local para desenvolvimento
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, 'database.db')


class ProductionConfig(Config):
    DEBUG = False
    # Banco de dados PostgreSQL para produção
    DB_USER = os.getenv('DB_USER', 'wnr')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '@NrabeloP0015')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'banco_wnr')

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
