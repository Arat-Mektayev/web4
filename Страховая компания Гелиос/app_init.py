from flask import Flask, render_template, request, abort, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login.mixins import AnonymousUserMixin
# Создание экземпляра приложения Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rrdxbdy122qdrh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Для примера используем SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Устанавливаем страницу для редиректа при необходимости входа

db = SQLAlchemy(app)
