from flask import Flask
from flask_app.config.default import default
from flask_app import home


def create_app():
    app = Flask(__name__)
    app.config.from_object(default)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(home.views.blueprint)
