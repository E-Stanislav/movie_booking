from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Настройки для использования JWT в cookies
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Установите секретный ключ для JWT
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']    # Используем JWT только в cookies
    app.config['JWT_COOKIE_SECURE'] = False           # True в production, False для тестирования
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'        # Путь для cookie с access token
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False     # CSRF для JWT (можно включить в production)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from models import User, Movie, Showtime, Seat, Reservation
        db.create_all()

    # Регистрация маршрутов
    from routes.auth_routes import auth_bp
    from routes.movie_routes import movie_bp
    from routes.reservation_routes import reservation_bp
    from routes.main_routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(main_bp)

    return app
