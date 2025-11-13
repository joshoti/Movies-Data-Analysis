from fastapi import APIRouter

from ..models import Prompt
from ..services.rag_service import rag_service

router = APIRouter()


@router.post("/rag")
def rag(prompt: Prompt):
    return rag_service.answer_question(prompt.prompt)
