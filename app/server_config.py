from flask_restx import Api
from flask import Blueprint

from app.controller.static_controller import api as static_ns


bp = Blueprint('api', __name__)

api = Api(
    bp,
    title="Basic CRUD API",
    version="1.0",
    doc="/doc",
    description="Basic CRUD Server"
)

api.add_namespace(static_ns, path="/")