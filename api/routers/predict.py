from fastapi import APIRouter

from ..models import Prompt
from ..services.rag_service import rag_service

router = APIRouter()


from fastapi import APIRouter

router = APIRouter()


@router.post("/predict")
def predict(prompt: Prompt):
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
    return rag_service.answer_question(prompt.prompt)
