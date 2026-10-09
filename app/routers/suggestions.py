from fastapi import APIRouter
from app.schemas.suggestion import (
    SuggestRequest,
    SuggestOccasionRequest,
    SuggestResponse,
    ColorHarmonyRequest,
    ColorHarmonyResponse,
)
from app.services.suggestion_service import (
    suggest_by_prompt,
    suggest_by_occasion_weather,
    check_color_harmony,
)

router = APIRouter(prefix="/suggest", tags=["5. Trợ lý AI Gợi ý phối đồ (AI Suggestions)"])

@router.post("/", response_model=SuggestResponse, summary="Gợi ý phối đồ qua ngôn ngữ tự nhiên (Gemini AI)")
async def get_outfit_suggestions(data: SuggestRequest):
    suggestions = await suggest_by_prompt(prompt=data.prompt, gender=data.gender or "female")
    return {
        "suggestions": suggestions,
        "ai_note": "Các gợi ý được điều chỉnh dựa trên cơ sở dữ liệu trang phục chuẩn mực của Việt Phục Remix."
    }

@router.post("/occasion", response_model=SuggestResponse, summary="Gợi ý phối đồ theo Bối cảnh + Thời tiết + Giới tính")
async def get_suggestions_by_occasion(data: SuggestOccasionRequest):
    suggestions = await suggest_by_occasion_weather(
        occasion=data.occasion,
        weather=data.weather or "mát mẻ",
        gender=data.gender or "female",
    )
    return {
        "suggestions": suggestions,
        "ai_note": f"Gợi ý trang phục cho bối cảnh {data.occasion} trong điều kiện thời tiết {data.weather}."
    }

@router.post("/color-harmony", response_model=ColorHarmonyResponse, summary="Kiểm tra mức độ hài hòa màu sắc Á Đông")
async def check_harmony(data: ColorHarmonyRequest):
    return await check_color_harmony(colors=data.colors, category=data.category or "Truyền thống")
