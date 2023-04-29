from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
import config.default

app = Flask(__name__)
app.config.from_object(config.default)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/file-upload/<img_category>', methods=['POST'])
def upload_file(img_category):
    if img_category in request.files:
        file = request.files[img_category]
    else:
        print('\n\n\n', request.files)
        print('File missing from file upload request.')
        flash('File missing from file upload request.')
        return redirect('/')

    # if no file uploaded, display error msg
    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    # if there is a file, save it
    if file:
        filename = secure_filename(file.filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], img_category, filename)
        print(dest)
        file.save(dest)
        return redirect('/')
