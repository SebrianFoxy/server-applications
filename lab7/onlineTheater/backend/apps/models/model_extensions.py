from typing import Dict, Any
from flask_sqlalchemy import SQLAlchemy
from ..database import db

class ModelExtension(db.Model):
    __abstract__ = True

    def update(self, data: Dict[str, Any], commit=True, **kwargs):

        for attr, value in data.items():
            if attr != 'id':
                setattr(self, attr, value)

        if commit:
            db.session.commit()

    def save(self, commit=True):
        db.session.add(self)

        if commit:
            db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)

        if commit:
            db.session.commit()
