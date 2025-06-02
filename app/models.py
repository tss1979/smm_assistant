from flask_login import UserMixin

from app import users_db


class User(users_db.Model, UserMixin):
    id = users_db.Column(users_db.Integer, primary_key=True)
    username = users_db.Column(users_db.String(80), unique=True, nullable=False)
    password = users_db.Column(users_db.String(120), nullable=False)
    vk_api_key = users_db.Column(users_db.String(250), nullable=True)
    vk_group_id = users_db.Column(users_db.Integer, nullable=True)


