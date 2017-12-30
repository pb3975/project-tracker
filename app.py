import os, sys
from flask import Flask
from flask_mongoengine import MongoEngine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from project_tracker.views import projects
    from project_tracker.admin import admin
    app.register_blueprint(projects)
    app.register_blueprint(admin)

register_blueprints(app)

if __name__ == '__main__':
    app.run()