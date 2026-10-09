from fastapi import APIRouter
from app.schemas.suggestion import CompareRequest, CompareResponse
from app.services.compare_service import compare_outfits

router = APIRouter(prefix="/compare", tags=["9. So sánh trang phục (Compare)"])

@router.post("/", response_model=CompareResponse, summary="So sánh 2-5 bộ outfit theo các tiêu chí văn hóa & thẩm mỹ")
async def compare_outfits_endpoint(data: CompareRequest):
    return await compare_outfits(data.outfit_ids)
