from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project_tracker import MongoEngine, bcrypt, login_manager, db
from project_tracker.models import Project, Note, User
import re

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(email):
    users = User.objects(email=email).first()
    if not users:
        return None
    return User.objects(email=email).first()



@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_input = request.form['inputEmail']
        password = request.form['inputPassword']
        if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
            user = User.objects(email=user_input).first()
        else:
            user = User.objects(username=user_input).first()

        if user:
            if user.password == password:
                user_obj = user
                login_user(user_obj)
                return redirect(url_for('users.profile'))
            else:
                print('Incorrect Credentials')
        else:
            return redirect(url_for('auth.register'))
    return render_template('user/signin.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['inputUsername']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        if User.objects(email=email):
            return redirect(url_for('auth.login'))
        else:
            user = User(email=email, password=password, username=username)
            user.save()
            login_user(user)
            return redirect(url_for('users.profile'))
    return render_template('user/register.html')

@auth.route('/protected')
@login_required
def protected():
    return "protected area"