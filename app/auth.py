from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import LoginForm, RegisterForm
from app.models import User
from app import users_db, bcrypt
import uuid

auth_bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form =  RegisterForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if form.validate_on_submit():
            if users_db.get(username):
                flash('Name already exists.')
            return redirect(url_for('auth.register'))
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hash_password)
        users_db.session.add(user)
        users_db.session.commit()
        flash('Registered successfully.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('smm.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
