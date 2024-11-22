from flask import Blueprint

from ..services.analysis import analysis_service

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/<sample_id>", methods=["GET"])
def analysis(sample_id: str):
    return analysis_service.get_sample_data(sample_id)
