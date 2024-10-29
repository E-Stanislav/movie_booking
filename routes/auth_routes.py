from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token, set_access_cookies
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity={'id': user.id, 'role': user.role}, expires_delta=timedelta(days=1))
            # Устанавливаем токен доступа в cookies и перенаправляем на главную
            response = redirect(url_for('main.home'))
            set_access_cookies(response, access_token)
            return response

        return render_template("login.html", error="Invalid credentials")
    return render_template('login.html')