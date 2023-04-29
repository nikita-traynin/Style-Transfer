from endpoints.home import home
from endpoints.file_upload import file_upload
from app import app


def endpoints_init():
    app.add_url_rule('/', view_func=home, methods=['GET'])
    app.add_url_rule('/file-upload/<img_category>', view_func=file_upload, methods=['POST'])
