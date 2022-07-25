from app.controller.configuration.routes import fact_api as api
from flask_restx import fields, reqparse

get_fact_parser = reqparse.RequestParser()
get_fact_parser.add_argument("fact_id", type=int, help="Unique identifier of fact.")

get_facts_parser = reqparse.RequestParser()
get_facts_parser.add_argument("limit", type=int, default=None, help="Limit the number of facts returned.")
get_facts_parser.add_argument("offset", type=int, default=None, help="Offset the number of facts returned.")

fact_model = api.model("Fact", {
    "id": fields.Integer,
    "subject_url": fields.String,
    "subject_id": fields.String,
    "predicate_url": fields.String,
    "predicate_id": fields.String,
    "object_url": fields.String,
    "object_id": fields.String,
    "source_url": fields.String,
    "source_name": fields.String,
    "object_label": fields.String,
    "confidence_reader": fields.Float,
    "feedback": fields.Integer,
})

fact_put_model = api.model("FactPut", {
    "id": fields.Integer,
    "feedback": fields.Integer,
})


