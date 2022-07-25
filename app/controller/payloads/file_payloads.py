from app.controller.configuration.routes import file_api as api
from werkzeug.datastructures import FileStorage

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)