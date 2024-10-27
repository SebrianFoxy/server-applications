from flask import Blueprint
from flask_restx import Api
from .film import ns as film_ns


api_bp = Blueprint('api_bp', __name__, url_prefix='/api/v1')
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    title='Online-Theater',
    version='1.0',
    description='Rest API Online-Theater',
    authorizations=authorizations,
)

api.add_namespace(film_ns, path="/film")
