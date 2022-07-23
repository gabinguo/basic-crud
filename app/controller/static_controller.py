import os
from flask import send_from_directory
from flask_restx import Resource

from app.controller.configuration.routes import static_api as api
from configs import static_file_loc


@api.route("")
class ServeWebsite(Resource):
    @staticmethod
    def get():
        return send_from_directory(os.path.join(static_file_loc, 'index_page'), "index.html")


@api.route("resource/<path:filename>")
class ServeFile(Resource):

    @staticmethod
    def get(filename):
        return send_from_directory(static_file_loc, filename)


@api.route("resource/<path:folder>/<path:filename>")
class ServeFileInFolder(Resource):

    @staticmethod
    def get(folder, filename):
        return send_from_directory(os.path.join(static_file_loc, folder), filename)
