from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from styletransfer import st

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
    output_name = st(content, style)


@app.route('/download', method=['GET'])
def dl():
    return send_from_directory('img/output', 'northwest-landscape-the-scream.jpg')
