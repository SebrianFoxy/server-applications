from flask import abort
from flask_restx import Namespace, Resource, fields
from flask_restx.reqparse import RequestParser
from ..models.film import Film
from flask import request, abort, current_app
from sqlalchemy.exc import IntegrityError
from ..database import db

ns = Namespace(name='film', description='Film operations')

film_expect_model = ns.model('Film expect', {
    'filmName': fields.String(),
    'dateRelease': fields.String(),
    'genre': fields.String(),
    'urlImage': fields.String(),
})

film_response_model = ns.model('Film response', {
    'id': fields.Integer(),
    'filmName': fields.String(),
    'dateRelease': fields.String(),
    'genre': fields.String(),
    'urlImage': fields.String(required=True),
    'dateJoined': fields.DateTime(),
})


@ns.route('')
class FilmApi(Resource):
    @ns.marshal_list_with(film_response_model)
    def get(self):
        film = Film.query.all()
        return film
    
    @ns.marshal_list_with(film_response_model)
    @ns.expect(film_expect_model)
    def post(self):
        data = ns.payload
        
        new_film = Film(**data)

        try:
            new_film.save()
        except IntegrityError as e:
            current_app.logger.error(e)
            abort(400, str(e.orig))

        return new_film, 201
    

@ns.route('/<id>')
@ns.param('id', 'The unique identifier of a Product')
class FilmApiById(Resource):
    @ns.marshal_with(film_response_model)
    def get(self, id):
        film = Film.query.get_or_404(id, 'Film not found')
        return film
    
    @ns.expect(film_expect_model)
    @ns.marshal_with(film_response_model)
    def put(self, id):
        film = Film.query.get_or_404(id, 'Film not found')
        data = ns.payload

        try:
            film.update(data)
        except IntegrityError as e:
            current_app.logger.error(e)
            abort(400, str(e.orig))

        return film

    @ns.response(204, 'Film deleted')
    def delete(self, id):
        film = Film.query.get_or_404(id, 'Film not found')
        db.session.delete(film)
        db.session.commit()
        return '', 204
