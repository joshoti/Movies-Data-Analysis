from fastapi import APIRouter, Request

from api.v2.services.query_service import query_service

router = APIRouter()


@router.get("/v2/query")
def query(request: Request):
    return query_service.get_data(request.query_params)
