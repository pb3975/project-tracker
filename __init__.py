import os
from flask import Flask
from flask_mongoengine import MongoEngine

from .views.views import projects
from .views.admin import admin

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])



app.register_blueprint(projects)
app.register_blueprint(admin)
db = MongoEngine(app)


if __name__ == '__main__':
    app.run()