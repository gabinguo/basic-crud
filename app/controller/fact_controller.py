import json
import os.path

from flask_restx import abort

from flask import request
from flask_restx import Resource, fields
from app.controller.configuration.routes import fact_api as api
from app.controller.payloads.fact_payloads import fact_model, fact_put_model, get_fact_parser, get_facts_parser, \
    unique_predicate_ids, unique_source_names, facts_with_pagination_model, get_value_counts_parser, value_count_model, \
    get_unique_sources, get_unique_predicate
from app.service.fact_service import find_fact_by_id, delete_a_fact, update_a_fact, create_a_fact, find_all_facts, \
    find_unique_predicate_ids, find_unique_source_names, value_counts_source_name, value_counts_predicate_id, \
    average_confidence

from configs import basedir

label_mapping = json.load(open(os.path.join(basedir, "all_properties_label.json")))


@api.route("")
class FactItem(Resource):

    @api.param("fact_id", "The ID of the fact item")
    @api.expect(get_fact_parser)
    @api.marshal_with(fact_model)
    def get(self):
        fact_id = request.args["fact_id"]
        fact = find_fact_by_id(fact_id)
        if fact:
            return fact
        abort(404, f"Fact with id {fact_id} not found.")

    @api.expect(fact_put_model)
    def put(self):
        payload = request.json
        payload = {k: v for k, v in payload.items() if v is not None}
        id_ = payload['id']
        del payload['id']
        if update_a_fact(id_, payload):
            return {"message": f"Successfully updated the fact: {id_}."}
        abort(code=400, message='Failed to update the fact.')

    @api.expect(fact_model)
    def post(self):
        payloads = request.json
        del payloads['id']
        if create_a_fact(payloads):
            return {"message": f"Successfully created the fact."}
        abort(code=400, message='Failed to create the fact.')

    @api.expect(get_fact_parser)
    def delete(self):
        fact_id = request.args["fact_id"]
        if delete_a_fact(fact_id):
            return {"message": f"Successfully deleted the fact item: {fact_id}."}
        abort(code=400, message='Failed to delete the fact item.')


@api.route("/list")
class FactItemList(Resource):
    @api.expect(get_facts_parser)
    @api.marshal_with(facts_with_pagination_model)
    def get(self):
        args = request.args
        page = int(args["page"]) if "page" in args else 1
        per_page = int(args["per_page"]) if "per_page" in args else 10
        source_name = args["source_name"] if "source_name" in args else None
        predicate_id = args["predicate_id"] if "predicate_id" in args else None
        facts, total = find_all_facts(page, per_page, source_name, predicate_id)
        return {"facts": facts, "total": total}


@api.route("/value_counts")
class FactValueCounts(Resource):
    @api.expect(get_value_counts_parser)
    @api.marshal_with(value_count_model, as_list=True)
    def get(self):
        args = request.args
        column_name = args["column_name"]
        if column_name == "source_name":
            value_counts = value_counts_source_name()
            for vc in value_counts:
                vc['label'] = vc['type']
            return value_counts
        elif column_name == "predicate_id":
            value_counts = value_counts_predicate_id()
            for vc in value_counts:
                vc['label'] = label_mapping[vc['type']][0]
            return value_counts
        else:
            abort(400, f"Invalid column name: {column_name}.")


@api.route("/average_confidence")
class FactAverageConfidence(Resource):
    def get(self):
        avg_confidence = average_confidence()
        return {'average_confidence': avg_confidence}


@api.route("/source_names")
class FactUniqueSourceNames(Resource):
    @api.expect(get_unique_sources)
    @api.marshal_with(unique_source_names)
    def get(self):
        args = request.args
        predicate_id = args["predicate_id"] if "predicate_id" in args else None
        return {
            "source_names": find_unique_source_names(predicate_id)
        }


@api.route("/predicate_ids")
class FactUniquePredicateIds(Resource):
    @api.expect(get_unique_predicate)
    @api.marshal_with(unique_predicate_ids)
    def get(self):
        args = request.args
        source_name = args["source_name"] if "source_name" in args else None
        return {
            "predicate_ids": find_unique_predicate_ids(source_name)
        }
