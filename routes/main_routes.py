from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@jwt_required(optional=True)  # Делаем аутентификацию необязательной для главной страницы
def home():
    user = get_jwt_identity()  # Получаем текущего пользователя, если он авторизован
    return render_template('home.html', user=user)
