from fastapi import APIRouter

from api.v2.services.analysis_service import analysis_service

router = APIRouter()


@router.get("/v2/analysis/{sample_id}")
def analysis(sample_id: str):
    if not sample_id.startswith("sample-"):
        return {
            "data": [],
            "max": 0,
            "min": 0,
            "error": "Invalid sample ID. Use format 'sample-<number>' where number is 1-5.",
        }
    return analysis_service.get_sample_data(sample_id)
