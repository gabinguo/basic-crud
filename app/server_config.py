from flask_restx import Api
from flask import Blueprint

from app.controller.static_controller import api as static_ns
from app.controller.file_controller import api as file_ns
from app.controller.fact_controller import api as fact_ns


bp = Blueprint('api', __name__)

api = Api(
    bp,
    title="Basic CRUD API",
    version="1.0",
    doc="/doc",
    description="Basic CRUD Server"
)

api.add_namespace(static_ns, path="/")
api.add_namespace(file_ns, path="/file")
api.add_namespace(fact_ns, path="/fact")
