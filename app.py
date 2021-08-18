from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from styletransfer import st
import redis
import concurrent.futures
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'img'

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
        filename = secure_filename(file.filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, filename)
        print(dest)
        file.save(dest)
        return redirect('/')


@app.route('/render', methods=['POST'])
def render():
    content = 'northwest-landscape.jpg'
    style = 'the-scream.jpg'

    # multithreading executor
    executor = concurrent.futures.ThreadPoolExecutor()

    # rendering thread
    render_future = executor.submit(st, content, style)

    # progress updating thread
    rds = redis.Redis()
    prog_future = executor.submit(progress_update, rds)

    # get output file name and download the file
    output_name = render_future.result()
    if output_name == "redis_error":
        return render_template("There was a redis error in style transfer. The server is not pinging back.")
    dl(output_name)

    return redirect('/')


def progress_update(rds):
    while(true):
        time.sleep(1)
        iter = rds.get('render_progress')
        if iter == 1000:
            break



@app.route('/download', methods=['GET'])
def dl(output_name):
    return send_from_directory('img/output', output_name)#'northwest-landscape-the-scream.jpg')
