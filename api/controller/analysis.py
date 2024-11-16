from flask import Blueprint, request

from ..services.analysis import AnalysisService

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/", methods=["GET"])
def analysis():
    return AnalysisService.get_data(request.args)
