from flask import Blueprint, request, jsonify, render_template
from app import db
from models import Movie, Showtime
from flask_jwt_extended import jwt_required

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/movies', methods=['GET'])
def list_movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@movie_bp.route('/movies/<int:movie_id>', methods=['GET'])
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"msg": "Movie not found"}), 404
    return render_template('movie_detail.html', movie=movie)
