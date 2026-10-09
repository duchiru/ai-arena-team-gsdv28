import logging
import json
from typing import List, Dict, Any, Optional
from app.services.component_service import get_all_categories
from app.ai.client import ai_client
from app.ai.prompts import (
    SUGGEST_OUTFIT_PROMPT,
    COLOR_HARMONY_PROMPT,
)

logger = logging.getLogger("vietphuc.suggestion_service")

# Rule-based fallback suggestions
FALLBACK_SUGGESTIONS = {
    "wedding": {
        "category": "Truyền thống",
        "occasion": "Lễ nghi",
        "color": "Hồng",
        "fabric": "Vải lụa",
        "pattern_technique": "Thêu",
        "pattern": "Hoa (sen, đào, mai, cúc,...)",
        "accessories": ["Kiềng cổ/Vòng ngọc", "Túi gấm"],
        "reason": "Màu hồng trang nhã, ngọt ngào, chất liệu lụa thêu hoa sen thanh tao phù hợp dự đám cưới mà không lấn át gia chủ.",
        "cultural_note": "Màu hồng đại diện cho hỷ sự nhẹ nhàng và sự gắn kết tốt đẹp trong văn hóa Việt.",
    },
    "school": {
        "category": "Truyền thống",
        "occasion": "Học đường",
        "color": "Trắng",
        "fabric": "Vải lụa",
        "pattern_technique": "Dệt",
        "pattern": "Hoa (sen, đào, mai, cúc,...)",
        "accessories": ["Giày đế bằng, cao gót, guốc mộc"],
        "reason": "Áo dài trắng truyền thống kín đáo, phom dáng chuẩn mực cho môi trường giáo dục.",
        "cultural_note": "Màu trắng là biểu tượng tinh khôi của tuổi học trò Việt Nam.",
    },
    "default": {
        "category": "Cách tân - Nữ",
        "occasion": "Dạo phố",
        "color": "Pastel",
        "fabric": "Linen",
        "pattern_technique": "In",
        "pattern": "Hoa (hoa nhí,...)",
        "accessories": ["Bờm", "Túi gấm, túi xách"],
        "reason": "Chất liệu linen thoáng mát, họa tiết hoa nhí trẻ trung kết hợp bờm tóc nhẹ nhàng.",
        "cultural_note": "Phong cách cách tân hiện đại nhưng vẫn giữ được nét duyên dáng của người phụ nữ Việt.",
    }
}

async def suggest_by_prompt(prompt: str, gender: str = "female") -> List[Dict[str, Any]]:
    """Gợi ý trang phục bằng ngôn ngữ tự nhiên thông qua Gemini."""
    categories = await get_all_categories()
    
    # Tạo context tóm tắt từ categories
    context_lines = []
    for cat in categories:
        context_lines.append(
            f"- Phân loại: {cat['name']}\n"
            f"  Bối cảnh: {', '.join(cat['occasions'])}\n"
            f"  Màu sắc: {', '.join(cat['colors'])}\n"
            f"  Chất liệu: {', '.join(cat['fabrics'])}\n"
            f"  Họa tiết: {', '.join(cat['patterns'])}\n"
            f"  Phụ kiện: {', '.join(cat['accessories'])}"
        )
    listing_context = "\n".join(context_lines)

    ai_prompt = SUGGEST_OUTFIT_PROMPT.format(
        listing_context=listing_context,
        user_prompt=prompt,
        gender=gender,
    )

    result = await ai_client.generate_json(ai_prompt)
    if isinstance(result, list) and len(result) > 0:
        return result

    # Fallback thông minh dựa trên từ khóa nếu AI không trả về
    prompt_l = prompt.lower()
    if any(k in prompt_l for k in ["cưới", "hôn lễ", "đám cưới", "dự tiệc"]):
        return [FALLBACK_SUGGESTIONS["wedding"]]
    elif any(k in prompt_l for k in ["học", "trường", "nữ sinh", "giáo viên"]):
        return [FALLBACK_SUGGESTIONS["school"]]
    return [FALLBACK_SUGGESTIONS["default"]]

async def suggest_by_occasion_weather(occasion: str, weather: str = "mát mẻ", gender: str = "female") -> List[Dict[str, Any]]:
    """Gợi ý trang phục theo bối cảnh, thời tiết và giới tính."""
    query = f"Tôi cần gợi ý trang phục cho bối cảnh {occasion}, thời tiết hiện tại là {weather}. Giới tính: {gender}."
    return await suggest_by_prompt(query, gender=gender)

async def check_color_harmony(colors: List[str], category: str = "Truyền thống") -> Dict[str, Any]:
    """Đánh giá sự hài hòa màu sắc bằng AI."""
    ai_prompt = COLOR_HARMONY_PROMPT.format(
        colors=", ".join(colors),
        category=category,
    )
    result = await ai_client.generate_json(ai_prompt)
    if isinstance(result, dict) and "score" in result:
        return result

    # Fallback
    return {
        "is_harmonious": True,
        "score": 8,
        "explanation": f"Sự kết hợp các gam màu {', '.join(colors)} mang lại cảm giác trang nhã, đúng tinh thần thẩm mỹ Á Đông.",
        "alternatives": ["Trắng ngà", "Hồng phấn"]
    }
