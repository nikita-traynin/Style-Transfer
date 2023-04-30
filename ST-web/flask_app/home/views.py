from flask import (
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    current_app
)
from werkzeug.utils import secure_filename
import os


blueprint = Blueprint("home", __name__)


@blueprint.route('/')
def home():
    return render_template('home.html')


@blueprint.route('/file-upload/<img_category>', methods=['POST'])
def file_upload(img_category):
    if img_category in request.files:
        file = request.files[img_category]
    else:
        print('\n\n\n', request.files)
        print('File missing from file upload request.')
        flash('File missing from file upload request.')
        return redirect('/')

    # if there is a file, save it
    filename = secure_filename(file.filename)
    dest = os.path.join(current_app.config['UPLOAD_FOLDER'], img_category, filename)
    print(dest)
    file.save(dest)
    return redirect('/')
