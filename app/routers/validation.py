from fastapi import APIRouter
from app.schemas.validation import ValidateRequest, ValidateResponse
from app.services.validation_service import validate_combination

router = APIRouter(prefix="/validate", tags=["3. Kiểm tra quy chuẩn văn hóa (Validation)"])

@router.post("/", response_model=ValidateResponse, summary="Kiểm tra mức độ hài hòa & phù hợp văn hóa của bộ phối")
async def validate_outfit_combination(data: ValidateRequest):
    result = await validate_combination(
        category=data.category,
        occasion=data.occasion,
        color=data.color,
        fabric=data.fabric,
        pattern_technique=data.pattern_technique,
        pattern=data.pattern,
        accessories=data.accessories,
    )
    return result
