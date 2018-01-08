from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import logout_user, login_required
from project_tracker.models import Project, Note, User

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('projects.list'))