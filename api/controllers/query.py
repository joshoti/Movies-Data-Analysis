from flask import Blueprint, request

from api.services.query import query_service

query_bp = Blueprint("query", __name__, url_prefix="/query")


@query_bp.route("", methods=["GET"])
def query():
    return query_service.get_data(request.args)
