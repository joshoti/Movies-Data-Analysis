from flask import Blueprint, request

from .chat_service import chat_service

chat_bp = Blueprint("chat", __name__, url_prefix="/v1/chat")


@chat_bp.route("", methods=["POST"])
def chat():
    """Get chat response for a given prompt
    Get chat response for a given prompt
    ---
    tags:
      - Chat

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
    return chat_service.answer_question(request.json["prompt"])
