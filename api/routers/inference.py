from fastapi import APIRouter

from ..models import Prompt
from ..probe.probeService import probing_service
from ..services.rag_service import rag_service

router = APIRouter()


@router.post("/probe")
def probe(prompt: Prompt):
    """Gets prediction for a given prompt based on known facts
    Gets prediction for a given prompt based on known facts
    ---
    tags:
      - Inference

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
    return probing_service.answer_question(prompt.prompt)


@router.post("/predict")
def predict(prompt: Prompt):
    """Gets prediction for a given prompt
    Gets prediction for a given prompt
    ---
    tags:
      - Inference

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
    return rag_service.answer_question(prompt.prompt)


@router.post("/inference")
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
        return probing_service.answer_question(prompt.prompt)
