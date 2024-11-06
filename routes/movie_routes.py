from flask import Blueprint, request, jsonify, render_template, request
from app import db
from models import Movie, Showtime
from flask_jwt_extended import jwt_required, get_jwt_identity

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/movies', methods=['GET'])
@jwt_required()
def list_movies():
    page = request.args.get('page', 1, type=int)  # Получаем номер страницы из параметра запроса
    per_page = 5  # Количество фильмов на странице
    movies = Movie.query.paginate(page=page, per_page=per_page)
    user_identity = get_jwt_identity()
    return render_template('movies.html', movies=movies, user=user_identity)

@movie_bp.route('/movies/<int:movie_id>', methods=['GET'])
@jwt_required()
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    user_identity = get_jwt_identity()
    if not movie:
        return jsonify({"msg": "Movie not found"}), 404
    return render_template('movie_detail.html', movie=movie, user=user_identity)
