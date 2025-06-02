# app/__init__.py

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug.utils import redirect

login_manager = LoginManager()
users_db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    users_db.init_app(app)
    bcrypt.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('smm.dashboard'))

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth import auth_bp
    from app.smm import smm_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(smm_bp)

    with app.app_context():
        users_db.create_all()

    return app
