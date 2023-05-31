from flask import Blueprint, request, current_app
import boto3
import boto3.session
from .ML_script import generate_and_save
from threading import Thread

blueprint = Blueprint("endpoints", __name__)


# e.g. /generate?content_img=mountain-landscape.jpg&style_img=Pointillist-landscape.jpg
@blueprint.route('/generate')
def generate():
    content_img = request.args.get('content_img')
    style_img = request.args.get('style_img')
    # upload to s3
    s3_session = boto3.session.Session(aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                                       aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])

    print("content image id: " + content_img)
    print("style image id: " + style_img)
    print("s3 bucket name: " + current_app.config['ST_S3_BUCKET'])

    s3 = s3_session.resource('s3').Bucket(current_app.config['ST_S3_BUCKET'])
    s3.download_file('img/content/' + content_img, 'img/content/' + content_img)
    s3.download_file('img/style/' + style_img, 'img/style/' + style_img)

    #home run!!!
    thread = Thread(target=generate_and_save, args=(style_img, content_img))
    thread.start()

    return "Kicked Off for " + style_img + " and " + content_img
