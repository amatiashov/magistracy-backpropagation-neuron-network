
ALLOWED_EXTENSIONS = {"bmp", "jpg"}


def allowed_file_upload(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
