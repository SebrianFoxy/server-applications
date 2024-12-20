from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_sqlalchemy(app):
    db.init_app(app)
    return app
