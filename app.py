import os
from flask import Flask
from flask_mongoengine import MongoEngine
db = MongoEngine()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)

class User(db.Document):
    email = db.StringField(required=True)

ross = User(email='booboo@example.com').save()

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()

