from flask import Blueprint, request

from .predictService import prediction_service

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")


@predict_bp.route("", methods=["POST"])
def predict():
    """Gets prediction for a given prompt
    Gets prediction for a given prompt
    ---
    tags:
      - Predict

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
    return prediction_service.answer_question(request.json["prompt"])
