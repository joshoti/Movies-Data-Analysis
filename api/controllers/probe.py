from flask import Blueprint, request

from ..services.probe import probing_service

probe_bp = Blueprint("probe", __name__, url_prefix="/probe")


@probe_bp.route("", methods=["POST"])
def probe():
    return probing_service.answer_question(request.json["prompt"])
