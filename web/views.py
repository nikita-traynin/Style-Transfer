from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
import redis
import concurrent.futures
import time
from web import app
from flask import session
from datetime import timedelta
import string
import random
import http

app.secret_key = os.environ.get('SESSION_SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(5)
app.config['UPLOAD_DIRECTORY'] = 'C:/Users/theni/Documents/Style-Transfer/img'


@app.before_request
def renew_session():
    session.permanent = True
    session.modified = True


# the home page.
@app.route('/')
def hello_world():
    if 'id' not in session:
        id_chars = string.ascii_letters + string.digits
        session['id'] = ''.join(random.choice(id_chars) for i in range(15))
    return render_template('home.html')

# upload files to the web app. this is only for the two images necessary
@app.route('/file-upload', methods=['POST'])
def upload_file():
    # the file "type" is configured in the dropzoneconfig.js file
    # wz_file is a werkzeug FileStorage object
    if 'content' in request.files:
        type = 'content'
        wz_file = request.files['content']
    elif 'style' in request.files:
        type = 'style'
        wz_file = request.files['style']
    else:
        flash('The file which was attempted to upload did not have name \"content\" or \"style\" so it will not be uploaded.')
        return ('', http.HTTPStatus.BAD_REQUEST)

    # something is wrong
    if wz_file.filename == '':
        flash('File python object\'s \"filename\" property is an empty string. ')
        return ('', http.HTTPStatus.BAD_REQUEST)

    # store file locally during dev. later, use remote store or other more robust solution
    else:
        # user input, so use secure_filename for security
        name = session['id'] + '_' + type + '_' + secure_filename(wz_file.filename)
        dest = os.path.join(app.config['UPLOAD_DIRECTORY'], name)
        wz_file.save(dest)
        return ('', http.HTTPStatus.NO_CONTENT)


@app.route('/render', methods=['POST'])
def render():
    content = rds.get('content_name')#'northwest-landscape.jpg'
    style = rds.get('style_name')#'the-scream.jpg'

    # rendering and progress updating threads
    # render_future = executor.submit(st, content, style)

    # prog_future = executor.submit(progress_update, redis.Redis())


    # get output file name and download the file
    try:
        output_name = st(content, style) #render_future.result()
    except:
        return render_template("The result of the rendering process was not able to be stored.")

    if output_name == "redis_error":
        return render_template("There was a redis error in style transfer. The server is not pinging back.")

    # call download function
    dl(output_name)
    return redirect('/')

@app.route('/get_progress')
def progress_update():
    rds = redis.Redis()
    try:
        iter = int(rds.get('render_progress'))
    except:
        return 0
    percent = (iter / 1000) * 100
    return str(percent)


#@app.route('/download', methods=['GET'])
def dl(output_name):
    return send_from_directory('img/output', output_name)#'northwest-landscape-the-scream.jpg')
