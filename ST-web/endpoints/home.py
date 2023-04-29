from flask import render_template
from flask_app_config import app


@app.route('/')
def hello_world():
    return render_template('home.html')
