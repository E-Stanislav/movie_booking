from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")  # "user" или "admin"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    showtime_date = db.Column(db.DateTime, nullable=False)
    seats = db.relationship('Seat', backref='showtime', lazy=True)

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.String(5), nullable=False)
    is_reserved = db.Column(db.Boolean, default=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    seats = db.Column(db.String(50), nullable=False)
    # Связи для удобного доступа к пользователю и сеансу
    user = db.relationship('User', backref='reservations', lazy=True)
    showtime = db.relationship('Showtime', backref='reservations', lazy=True)