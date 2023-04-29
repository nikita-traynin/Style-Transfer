from flask import Flask

app = Flask(__name__)

from config.config_init import configure_flask_app
from endpoints.endpoints_init import endpoints_init

configure_flask_app()
endpoints_init()

