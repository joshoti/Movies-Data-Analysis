from flask import Blueprint, request

from .probeService import probing_service

probe_bp = Blueprint("probe", __name__, url_prefix="/probe")


@probe_bp.route("", methods=["POST"])
def probe():
    """Gets prediction for a given prompt based on known facts
    Gets prediction for a given prompt based on known facts
    ---
    tags:
      - Probe

    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Prompt"

    responses:
      201:
        description: OK
        content:
          text/html:
            schema:
              type: string
            example: "The capital of Nigeria is Abuja."
    """
    return probing_service.answer_question(request.json["prompt"])
