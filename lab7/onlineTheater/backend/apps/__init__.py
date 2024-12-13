import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .api import api_bp
from .database import setup_sqlalchemy, db
from .config import Config
from .models import Film

migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    
    setup_sqlalchemy(app)
    migrate.init_app(app, db, directory=app.config['MIGRATIONS_FOLDER'] or './migrations')

    @app.teardown_request
    def shutdown_session(exception):
        db.session.rollback()

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(e)
    
    app.register_blueprint(api_bp)

    return app
