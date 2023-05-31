from flask import Flask
from flask_app import generate


def create_app(config_path="flask_app.config.default"):
    app = Flask(__name__)
    app.config.from_object(config_path)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(generate.endpoints.blueprint)
