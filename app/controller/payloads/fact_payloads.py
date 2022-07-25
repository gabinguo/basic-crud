from app.controller.configuration.routes import fact_api as api
from flask_restx import fields, reqparse

get_fact_parser = reqparse.RequestParser()
get_fact_parser.add_argument("fact_id", type=int, help="Unique identifier of fact.")

get_facts_parser = reqparse.RequestParser()
get_facts_parser.add_argument("page", type=int, required=False, help="Page number")
get_facts_parser.add_argument("per_page", type=int, required=False, help="Number of facts per page")

get_value_counts_parser = reqparse.RequestParser()
get_value_counts_parser.add_argument("column_name", type=str, help="Column name")

value_count_model = api.model("value_count_model", {
    "type": fields.String,
    "count": fields.Integer
})

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

facts_with_pagination_model = api.model("FactsWithPagination", {
    "facts": fields.List(fields.Nested(fact_model)),
    "total": fields.Integer
})

fact_put_model = api.model("FactPut", {
    "id": fields.Integer,
    "feedback": fields.Integer,
})


unique_source_names = api.model("UniqueSourceNames", {
    "source_names": fields.List(fields.String),
})

unique_predicate_ids = api.model("UniquePredicateIds", {
    "predicate_ids": fields.List(fields.String),
})
