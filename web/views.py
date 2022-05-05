from flask import Flask, render_template, request, send_file, flash, session
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
import string
import random
import redis
import http
import re
import requests
import toml

app = Flask(__name__)


################## CELERY BEGIN ########################
################## CELERY END ########################
# config
app.config.from_file('flask_config.toml', load=toml.load)


@app.before_request
def renew_session():
    session.permanent = True
    session.modified = True


@app.route('/')
def hello_world():
    if 'id' not in session:
        id_chars = string.ascii_letters + string.digits
        session['id'] = ''.join(random.choice(id_chars) for i in range(15))
    return render_template('home.html')


@app.route('/file-upload', methods=['POST'])
def upload_file():
    if 'content' in request.files:
        type = 'content'
        wz_file = request.files['content']
    elif 'style' in request.files:
        type = 'style'
        wz_file = request.files['style']
    else:
        flash('The file which was attempted to upload did not have name '
              '\"content\" or \"style\" so it will not be uploaded.')
        return '', http.HTTPStatus.BAD_REQUEST

    if wz_file.filename == '':
        flash('File python object\'s \"filename\" property is an empty string. ')
        return '', http.HTTPStatus.BAD_REQUEST
    else:
        name = session['id'] + '_' + type + '_' + secure_filename(wz_file.filename)
        dst = os.path.join(app.config['UPLOAD_DIRECTORY'], name)
        wz_file.save(dst)
        return '', http.HTTPStatus.OK


@app.route('/render', methods=['POST'])
def render():
    # find two files (via session + type)
    (_,_,files) = next(os.walk(app.config['UPLOAD_DIRECTORY']))
    for file in files:
        if re.match(session['id'] + '_' + 'content', file):
            content_img = open(os.path.join(app.config['UPLOAD_DIRECTORY'], file), 'rb')
        elif re.match(session['id'] + '_' + 'style', file):
            style_img = open(os.path.join(app.config['UPLOAD_DIRECTORY'], file), 'rb')

    # call ml server
    files = {'content': content_img, 'style': style_img}
    r = requests.post(app.config['ML_SERVER'] + '/init', files = files)

    return '', http.HTTPStatus.OK


@app.route('/success', methods=['POST'])
def download():
    file = request.files['result.png']
    send_file(file)

    return '', http.HTTPStatus.OK


@app.route('/get_progress')
def progress_update():
    rds = redis.Redis()
    try:
        iter = int(rds.get('render_progress'))
    except:
        return 0
    percent = (iter / 1000) * 100
    return str(percent)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
