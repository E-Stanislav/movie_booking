from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging as log
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@jwt_required(optional=True)
def home():
    user_identity = get_jwt_identity()
    if user_identity.get("role") == "admin":
        return render_template('admin_dashboard.html', user=user_identity)
    return render_template('home.html', user=user_identity)

@main_bp.route('/admin')
@jwt_required()  # Только авторизованные пользователи могут попасть на эту страницу
def admin_dashboard():
    user_identity = get_jwt_identity()
    
    # Проверка, является ли пользователь админом (предполагается наличие атрибута user_identity['role'])
    if user_identity and user_identity.get("role") == "admin":
        return render_template('admin_dashboard.html', user=user_identity)
    else:
        log.warning("Пользователь не является админом и был перенаправлен")
        return redirect(url_for('main.home'))