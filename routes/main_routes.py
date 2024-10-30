from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging as log
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@jwt_required()  # Делаем аутентификацию необязательной для главной страницы
def home():
    user_identity = get_jwt_identity()  # Получаем текущего пользователя, если он авторизован
    return render_template('home.html', user=user_identity)