from flask_restx import abort

from flask import request
from flask_restx import Resource
from app.controller.configuration.routes import fact_api as api
from app.controller.payloads.fact_payloads import fact_model, fact_put_model, get_fact_parser, get_facts_parser
from app.service.fact_service import find_fact_by_id, delete_a_fact, update_a_fact, create_a_fact, find_all_facts


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
    @api.marshal_with(fact_model, as_list=True)
    def get(self):
        args = request.args
        limit = args["limit"] if "limit" in args else 100
        offset = args["offset"] if "offset" in args else 0
        return find_all_facts(limit, offset)
