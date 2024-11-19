from flask import Blueprint, request

from ..services.analysis import analysis_service

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/", methods=["GET"])
def analysis():
    return analysis_service.get_data(request.args)
