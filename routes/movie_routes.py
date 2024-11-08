from flask import Blueprint, request, jsonify, render_template, request, flash, redirect, url_for
from app import db
from models import Movie, Showtime, User
from forms import MovieForm
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
from datetime import datetime, timedelta


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
    
    form = MovieForm(submit_text="Add Movie")
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

@movie_bp.route('/movies/<int:movie_id>', methods=['POST'])
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

@movie_bp.route('/manage_users')
@jwt_required(optional=True)
def manage_user():
    # Получаем информацию о текущем пользователе
    user_identity = get_jwt_identity()
    
    # Проверяем, что пользователь аутентифицирован и является администратором
    if not user_identity or user_identity.get("role") != "admin":
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('main_bp.home'))
    
    # Загружаем список всех пользователей из базы данных
    users = User.query.all()
    
    # Рендерим шаблон с передачей текущего пользователя и списка пользователей
    return render_template('manage_user.html', user=user_identity, users=users)


@movie_bp.route('/view_analytics')
@jwt_required(optional=True)
def view_analytics():
    # Получаем информацию о текущем пользователе
    user_identity = get_jwt_identity()

    # Проверяем, что пользователь аутентифицирован и является администратором
    if not user_identity or user_identity.get("role") != "admin":
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('main_bp.home'))

    # Пример: Генерация случайных данных для активности пользователей (замените на реальную логику)
    activity_labels = ["2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04", "2024-11-05"]
    activity_labels = [str(datetime.now().date() + timedelta(days=-i)) for i in range(30)]
    activity_data = [random.randint(50, 150) for _ in activity_labels]  # случайное количество активности на каждый день

    # Пример: Генерация случайных данных для популярного контента (замените на реальную логику)
    content_labels = ["Movie A", "Movie B", "Movie C", "Movie D"]
    content_data = [random.randint(20, 200) for _ in content_labels]  # количество просмотров для каждого фильма

    # Рендерим шаблон с передачей текущего пользователя и данных для аналитики
    return render_template(
        'view_analytics.html',
        user=user_identity,
        activity_labels=activity_labels,
        activity_data=activity_data,
        content_labels=content_labels,
        content_data=content_data
    )