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
import boto3
import boto3.session


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
    filepath = os.path.join('img', img_category, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)

    # upload to s3
    s3_session = boto3.session.Session(aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                                       aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
    s3 = s3_session.resource('s3')
    s3.Bucket(current_app.config['ST_S3_BUCKET']).put_object(Key=filename, Body=filepath)
    print(filepath)

    # delete the file (exception if not found)
    os.remove(filepath)

    return redirect('/')
