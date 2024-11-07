from flask import Blueprint, request, jsonify, render_template, request, flash, redirect, url_for
from app import db
from models import Movie, Showtime
from forms import MovieForm
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


@movie_bp.route('/manage_movies', methods=['GET', 'POST'])
@jwt_required()
def manage_movies():
    user_identity = get_jwt_identity()
    
    # Проверяем, является ли пользователь админом
    if user_identity.get("role") != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('main.home'))
    
    form = MovieForm()
    if form.validate_on_submit():
        # Создаем новый объект Movie
        new_movie = Movie(
            title=form.title.data,
            description=form.description.data,
            genre=form.genre.data
        )
        # Сохраняем в базе данных
        db.session.add(new_movie)
        db.session.commit()
        flash(f"Movie '{new_movie.title}' added successfully!", "success")
        return redirect(url_for('movie.manage_movies', user=user_identity))
    
    # Получаем все фильмы для отображения на странице
    movies = Movie.query.all()
    return render_template('manage_movies.html', form=form, movies=movies, user=user_identity)

@movie_bp.route('/delete_movie/<int:movie_id>', methods=['POST'])
@jwt_required()
def delete_movie(movie_id):
    user_identity = get_jwt_identity()
    
    # Проверка на роль администратора
    if user_identity.get("role") != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('main.home', user=user_identity))
    
    # Получение фильма по ID
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash(f"Movie '{movie.title}' has been deleted.", "success")
    return redirect(url_for('movie.manage_movies', user=user_identity))


@movie_bp.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_movie(movie_id):
    user_identity = get_jwt_identity()
    
    # Проверка на роль администратора
    if user_identity.get("role") != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('main.home', user=user_identity))
    
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)  # Используем obj для предзаполнения формы данными фильма
    
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        movie.genre = form.genre.data
        db.session.commit()
        flash(f"Movie '{movie.title}' has been updated.", "success")
        return redirect(url_for('movie.manage_movies'))
    
    return render_template('edit_movie.html', form=form, movie=movie, user=user_identity)