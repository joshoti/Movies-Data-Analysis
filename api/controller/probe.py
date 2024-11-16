from flask import Blueprint, request

from ..services.probe import ProbingService

probe_bp = Blueprint("probe", __name__, url_prefix="/probe")


@probe_bp.route("/", methods=["POST"])
def probe():
    return ProbingService.answer_question(request.json["prompt"])
