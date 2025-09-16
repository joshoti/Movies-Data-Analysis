from fastapi import APIRouter

from ..models import Prompt
from ..probe.probeService import probing_service

router = APIRouter()


@router.post("/probe")
def probe(prompt: Prompt):
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
    return probing_service.answer_question(prompt.prompt)
