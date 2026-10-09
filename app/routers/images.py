from fastapi import APIRouter, HTTPException
from app.schemas.image import (
    ImageGenerateRequest,
    ImageGenerateResponse,
    TryOnRequest,
    TryOnResponse,
)
from app.services.image_service import generate_image_custom, try_on_outfit

router = APIRouter(prefix="/images", tags=["6. Tạo ảnh & Thử đồ AI (Image Generation & Try-on)"])

@router.post("/generate", response_model=ImageGenerateResponse, summary="Tạo hình ảnh phối đồ nghệ thuật (Imagen 4.0)")
async def generate_image_endpoint(data: ImageGenerateRequest):
    return await generate_image_custom(data)

@router.post("/try-on", response_model=TryOnResponse, summary="Thử đồ ảo trên hình ảnh avatar người dùng")
async def try_on_endpoint(data: TryOnRequest):
    try:
        return await try_on_outfit(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
