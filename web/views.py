from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
import redis
import concurrent.futures
import time
from web import app
# from flask_executor import Executor

app.config['UPLOAD_FOLDER'] = 'img'
# executor = Executor(app)

@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/file-upload', methods=['POST'])
def upload_file():
    if 'content' in request.files:
        subfolder = 'content'
        file = request.files['content']
    elif 'style' in request.files:
        subfolder = 'style'
        file = request.files['style']
    else:
        print('\n\n\n', request.files)
        print('File upload name neither content nor style, exiting')
        return redirect('/')

    # if no file uploaded, display error msg
    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    # if there is a file, save it
    if file:
        rds = redis.Redis()
        filename = secure_filename(file.filename)
        rds.set(subfolder + '_name', filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, filename)
        file.save(dest)
        return redirect('/')


@app.route('/render', methods=['POST'])
def render():
    rds = redis.Redis()
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
