import os
from flask import Flask
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = MongoEngine(app)


def register_blueprints(app):
    from .views.views import projects
    from .views.admin import admin
    app.register_blueprint(projects)
    app.register_blueprint(admin)

register_blueprints(app)


if __name__ == '__main__':
    app.run()