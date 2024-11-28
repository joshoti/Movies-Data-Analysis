from flask import Blueprint, request

from ..services.predict import prediction_service

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")


@predict_bp.route("", methods=["POST"])
def predict():
    return prediction_service.answer_question(request.json["prompt"])
