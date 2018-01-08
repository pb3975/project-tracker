import os
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = MongoEngine(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)



def register_blueprints(app):
    from .views.project import project
    from .views.admin import admin
    from .views.users import users
    # from .views.login_manager import login_manager
    from .views.auth import auth
    app.register_blueprint(project)
    app.register_blueprint(admin)
    app.register_blueprint(users)
    # app.register_blueprint(login_manager)
    app.register_blueprint(auth)

register_blueprints(app)

login_manager.login_view = "auth.login"


if __name__ == '__main__':
    app.run(debug=True)