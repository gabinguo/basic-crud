import json
import logging
import os

from flask import request
from flask_restx import Resource, abort
from werkzeug.datastructures import FileStorage

from configs import uploaded_file_loc
from app.controller.configuration.routes import file_api as api
from app.controller.payloads.file_payloads import upload_parser
from app.service.fact_service import create_a_fact


ALLOWED_EXTENSIONS = {'jsonl', 'json'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


logger = logging.getLogger(__name__)


@api.route("/upload")
class FileUpload(Resource):
    @api.expect(upload_parser)
    def post(self):
        uploaded_file: FileStorage = request.files['file']
        logger.info(f"Uploaded file: {uploaded_file.filename}")
        if uploaded_file.filename == '':
            abort(code=400, message="No file uploaded.")
        if uploaded_file and allowed_file(uploaded_file.filename):
            file_type = uploaded_file.filename.split('.')[-1]
            uploaded_file.save(os.path.join(uploaded_file_loc, uploaded_file.filename))
            if file_type == 'jsonl':
                facts = [json.loads(line) for line in open(os.path.join(uploaded_file_loc, uploaded_file.filename))]
            elif file_type == 'json':
                facts = json.load(open(os.path.join(uploaded_file_loc, uploaded_file.filename)))['facts']
            else:
                return abort(code=400, message="Currently only jsonl and json files are supported.")

            for fact in facts:
                create_a_fact(fact)
            os.remove(os.path.join(uploaded_file_loc, uploaded_file.filename))
            return {"message": f"successfully ingested {len(facts)} facts"}
        abort(code=400, message="Something went wrong.")
