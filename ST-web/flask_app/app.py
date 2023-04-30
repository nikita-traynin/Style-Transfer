from flask import Flask
from flask_app import home


def create_app(config_path="flask_app.config.default"):
    app = Flask(__name__)
    app.config.from_object(config_path)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(home.views.blueprint)
