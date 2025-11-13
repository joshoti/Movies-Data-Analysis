from fastapi import APIRouter

from api.v2.models import Prompt
from api.v2.services.chat_service import chat_service
from api.v2.services.rag_service import rag_service

router = APIRouter()


@router.post("/v2/chat")
def inference(prompt: Prompt, use_rag: bool = True):
    """Gets inference for a given prompt using either RAG or probing service
    Gets inference for a given prompt using either RAG or probing service
    ---
    tags:
      - Inference

    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Prompt"

    parameters:
      - name: use_rag
        in: query
        description: Whether to use RAG service (true) or probing service (false)
        schema:
          type: boolean
        example: true

    responses:
      201:
        description: OK
        content:
          text/html:
            schema:
              type: string
            example: "The capital of Nigeria is Abuja."
    """
    if use_rag:
        return rag_service.answer_question(prompt.prompt)
    else:
        return chat_service.answer_question(prompt.prompt)
