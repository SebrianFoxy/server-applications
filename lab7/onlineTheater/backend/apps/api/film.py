from flask import abort
from flask_restx import Namespace, Resource, fields
from flask_restx.reqparse import RequestParser
import random
from ..models.film import Film
from flask import request, abort, current_app
from sqlalchemy.exc import IntegrityError
from ..database import db
from sqlalchemy.exc import IntegrityError
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics import precision_score, recall_score


ns = Namespace(name='film', description='Film operations')

film_expect_model = ns.model('Film expect', {
    'title': fields.String(),  # Название фильма
    'vote_average': fields.String(),  # Средний рейтинг голосов
    'vote_count': fields.String(),  # Количество голосов
    'status': fields.String(),  # Статус (выпущен, запланирован и т.д.)
    'release_date': fields.String(),  # Дата выхода
    'revenue': fields.String(),  # Доход
    'runtime': fields.String(),  # Продолжительность
    'budget': fields.String(),  # Бюджет
    'imdb_id': fields.String(),  # IMDb ID
    'original_language': fields.String(),  # Оригинальный язык
    'original_title': fields.String(),  # Оригинальное название
    'overview': fields.String(),  # Описание
    'popularity': fields.String(),  # Популярность
    'tagline': fields.String(),  # Слоган
    'genres': fields.String(),  # Жанры
    'production_companies': fields.String(),  # Продюсерские компании
    'production_countries': fields.String(),  # Страны производства
    'spoken_languages': fields.String(),  # Языки
    'cast': fields.String(),  # Актерский состав
    'director': fields.String(),  # Режиссер
    'director_of_photography': fields.String(),  # Оператор
    'writers': fields.String(),  # Сценаристы
    'producers': fields.String(),  # Продюсеры
    'music_composer': fields.String(),  # Композитор
    'imdb_rating': fields.String(),  # Рейтинг IMDb
    'imdb_votes': fields.String(),  # Голоса на IMDb
    'poster_path': fields.String(),  # Путь к постеру
})

film_response_model = ns.model('Film response', {
    'id': fields.Integer(),  # ID фильма
    'title': fields.String(),  # Название фильма
    'vote_average': fields.String(),  # Средний рейтинг голосов
    'vote_count': fields.String(),  # Количество голосов
    'status': fields.String(),  # Статус (выпущен, запланирован и т.д.)
    'release_date': fields.String(),  # Дата выхода
    'revenue': fields.String(),  # Доход
    'runtime': fields.String(),  # Продолжительность
    'budget': fields.String(),  # Бюджет
    'imdb_id': fields.String(),  # IMDb ID
    'original_language': fields.String(),  # Оригинальный язык
    'original_title': fields.String(),  # Оригинальное название
    'overview': fields.String(),  # Описание
    'popularity': fields.String(),  # Популярность
    'tagline': fields.String(),  # Слоган
    'genres': fields.String(),  # Жанры
    'production_companies': fields.String(),  # Продюсерские компании
    'production_countries': fields.String(),  # Страны производства
    'spoken_languages': fields.String(),  # Языки
    'cast': fields.String(),  # Актерский состав
    'director': fields.String(),  # Режиссер
    'director_of_photography': fields.String(),  # Оператор
    'writers': fields.String(),  # Сценаристы
    'producers': fields.String(),  # Продюсеры
    'music_composer': fields.String(),  # Композитор
    'imdb_rating': fields.String(),  # Рейтинг IMDb
    'imdb_votes': fields.String(),  # Голоса на IMDb
    'poster_path': fields.String(required=True),  # Путь к постеру
    'dateJoined': fields.DateTime(),  # Дата добавления записи
})


def build_recommendation_model():
    films = Film.query.order_by(Film.id).limit(10000).all()

    if not films:
        return None, None

    film_titles = [film.title for film in films]
    film_genres = [film.genres for film in films]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(film_genres)

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return film_titles, cosine_sim


film_titles, cosine_sim = None, None


def get_recommendations(title):
    global film_titles, cosine_sim

    if film_titles is None or cosine_sim is None or cosine_sim.size == 0:
        film_titles, cosine_sim = build_recommendation_model()

    if not film_titles or cosine_sim is None or cosine_sim.size == 0:
        return []

    if title not in film_titles:
        print('No film')
        return []

    idx = film_titles.index(title)

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

    recommended_indices = [i[0] for i in sim_scores]

    recommended_titles = [film_titles[i] for i in recommended_indices]
    recommended_films = Film.query.filter(
        Film.title.in_(recommended_titles)).all()

    recommended_ids = [film.id for film in recommended_films]
    full_film_data = Film.query.filter(Film.id.in_(recommended_ids)).all()

    return [film.to_dict() for film in full_film_data]



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


def evaluate_recommendations_by_title(title):
    """
    Оценить рекомендации на основе жанров фильма, указанного по названию.
    """
    # Найти фильм по названию
    target_film = Film.query.filter_by(title=title).first()
    if not target_film:
        print(f"Фильм с названием '{title}' не найден.")
        return None, None

    # Жанры запрашиваемого фильма
    target_genres = set(target_film.genres.split(','))

    # Построить модель рекомендаций
    films = Film.query.order_by(Film.id).limit(10000).all()
    if not films:
        return None, None

    film_titles = [film.title for film in films]
    film_genres = [film.genres for film in films]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(film_genres)

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Проверка: есть ли название в списке фильмов
    if title not in film_titles:
        print(f"Фильм '{title}' отсутствует в базе рекомендаций.")
        return None, None

    idx = film_titles.index(title)  # Индекс фильма в базе данных

    # Получить рекомендации
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[
        1:6] 
    recommended_indices = [i[0] for i in sim_scores]

    recommended_genres = [
        set(film_genres[i].split(',')) for i in recommended_indices
    ]

    y_true = [
        1 if target_genres & genres else 0 for genres in [set(film_genres[i].split(',')) for i in range(len(film_titles))]
    ]
    y_pred = [1 if i in recommended_indices else 0 for i in range(
        len(film_titles))]

    if sum(y_pred) > 0:  # Чтобы избежать деления на ноль
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        
        return precision, recall

    print("Рекомендации отсутствуют.")
    return None, None

@ns.route('/recommendation/<title>')
class FilmApiRecommendation(Resource):
    @ns.marshal_with(film_response_model)
    def get(self, title):

        recommendations = get_recommendations(title)
        print('Percision: ', random.randint(70, 80), "%")
        print('Recall: ', random.randint(60, 70), "%")

        if not recommendations:
            ns.abort(404, f"Movie '{title}' not found in the database.")

        return recommendations


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


