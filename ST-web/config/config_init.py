from config.default import default
from app import app


def configure_flask_app():
    app.config.from_object(default)
