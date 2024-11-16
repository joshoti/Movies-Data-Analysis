from flask import Blueprint, request

from ..services.predict import PredictionService

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")


@predict_bp.route("/", methods=["POST"])
def predict():
    return PredictionService.answer_question(request.json["prompt"])
