from typing import Dict, Any

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, String, Integer, BigInteger
from .model_extensions import ModelExtension
from datetime import datetime


class Film(ModelExtension):
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True)
    filmName = Column(String(255))
    dateRelease = Column(String(255))
    genre = Column(String(255))
    urlImage = Column(String(255))
    dateJoined = Column(DateTime, default=datetime.utcnow, nullable=False)
