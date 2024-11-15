import logging
import time
import psutil  # Для мониторинга производительности
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Создаем приложение Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@127.0.0.1:5432/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Film(db.Model):
    __tablename__ = 'film'
    id = db.Column(db.Integer, primary_key=True)
    filmName = db.Column(db.String(255), nullable=False)
    urlImage = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(255), nullable=True)
    dateRelease = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        """Метод для преобразования объекта в словарь."""
        return {
            'id': self.id,
            'filmName': self.filmName,
            'urlImage': self.urlImage,
            'genre': self.genre,
            'dateRelease': self.dateRelease,
        }

# Настройка логирования с помощью dictConfig
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10000,
            'backupCount': 3,
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi', 'file']
    }
})

# Добавление уровня TRACE
logging.addLevelName(5, "TRACE")


def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(5):
        self._log(5, message, args, **kwargs)


logging.Logger.trace = trace

@app.before_request
def log_request_info():
    app.logger.debug(
        f"Request: {request.method} {request.url} - Params: {request.args} - Body: {request.get_data(as_text=True)}")


@app.after_request
def log_response_info(response):
    app.logger.debug(
        f"Response: {response.status} - Data: {response.get_data(as_text=True)}")
    return response

# Глобальный обработчик исключений


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Exception: {e}", exc_info=True)
    return "An error occurred", 500

# Декоратор для логирования времени выполнения методов


def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        app.logger.info(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


@app.route('/some_route')
@log_execution_time
def some_route():
    return "Hello, World!"

@app.route('/set_log_level/<level>')
def set_log_level(level):
    level_name = level.upper()
    if level_name in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        app.logger.setLevel(getattr(logging, level_name))
        return f"Log level set to {level}", 200
    else:
        return f"Invalid log level: {level}", 400


security_log_handler = RotatingFileHandler(
    'security.log', maxBytes=10000, backupCount=3)
security_log_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(message)s'))
security_logger = logging.getLogger('security')
security_logger.addHandler(security_log_handler)
security_logger.setLevel(logging.INFO)


def log_security_event(event, user, ip):
    security_logger.info(f"{event} - User: {user} - IP: {ip}")


@app.route('/login')
def login():
    log_security_event("Successful login", "username123", request.remote_addr)
    return "Logged in"


logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

sql_log_handler = RotatingFileHandler('sql.log', maxBytes=10000, backupCount=3)
sql_log_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.addHandler(sql_log_handler)
sql_logger.setLevel(logging.DEBUG)


file_handler = RotatingFileHandler(
    'app.log', maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
logging.getLogger().addHandler(file_handler)


@app.route('/films', methods=['GET'])
def get_films():
    films = Film.query.all() 
    return jsonify([film.to_dict() for film in films])

if __name__ == '__main__':
    app.run(debug=True)
