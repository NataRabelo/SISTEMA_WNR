from dotenv import load_dotenv
import os
from app import create_app
from config import DevelopmentConfig, ProductionConfig

load_dotenv()

env = os.getenv('FLASK_ENV', 'development')

if env == 'production':
    app = create_app(ProductionConfig)
else:
    app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()
