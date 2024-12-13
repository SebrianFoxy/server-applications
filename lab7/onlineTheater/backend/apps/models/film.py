from typing import Dict, Any

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, String, Integer, BigInteger
from .model_extensions import ModelExtension
from datetime import datetime


class Film(ModelExtension):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(3000))  # Название фильма
    vote_average = Column(String(50))  # Средний рейтинг голосов
    vote_count = Column(String(50))  # Количество голосов
    status = Column(String(255))  # Статус (выпущен, запланирован и т.д.)
    release_date = Column(String(255))  # Дата выхода
    revenue = Column(String(255))  # Доход
    runtime = Column(String(255))  # Продолжительность
    budget = Column(String(255))  # Бюджет
    imdb_id = Column(String(255))  # IMDb ID
    original_language = Column(String(255))  # Оригинальный язык
    original_title = Column(String(3000))  # Оригинальное название
    overview = Column(String(3000))  # Описание
    popularity = Column(String(255))  # Популярность
    tagline = Column(String(3000))  # Слоган
    genres = Column(String(3000))  # Жанры
    production_companies = Column(String(3000))  # Продюсерские компании
    production_countries = Column(String(3000))  # Страны производства
    spoken_languages = Column(String(3000))  # Языки
    cast = Column(String(3000))  # Актерский состав
    director = Column(String(255))  # Режиссер
    director_of_photography = Column(String(255))  # Оператор
    writers = Column(String(3000))  # Сценаристы
    producers = Column(String(3000))  # Продюсеры
    music_composer = Column(String(255))  # Композитор
    imdb_rating = Column(String(255))  # Рейтинг IMDb
    imdb_votes = Column(String(255))  # Голоса на IMDb
    poster_path = Column(String(255))  # Путь к постеру


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
