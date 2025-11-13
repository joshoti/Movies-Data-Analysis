from fastapi import APIRouter

from api.v2.models import Prompt
from api.v2.services.rag_service import rag_service

router = APIRouter()


@router.post("/rag")
def rag(prompt: Prompt):
    return rag_service.answer_question(prompt.prompt)
