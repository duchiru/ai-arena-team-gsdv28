import logging
from typing import List, Dict, Any
from app.services.outfit_service import get_outfit
from app.ai.client import ai_client
from app.ai.prompts import COMPARE_OUTFITS_PROMPT

logger = logging.getLogger("vietphuc.compare_service")

async def compare_outfits(outfit_ids: List[str]) -> Dict[str, Any]:
    """So sánh nhiều bộ trang phục bằng Gemini AI."""
    outfits = []
    for oid in outfit_ids:
        o = await get_outfit(oid)
        if o:
            outfits.append(o)

    if len(outfits) < 2:
        return {
            "outfits": outfits,
            "formality_ranking": [o["id"] for o in outfits],
            "cultural_authenticity": [o["id"] for o in outfits],
            "versatility": [o["id"] for o in outfits],
            "ai_analysis": "Cần ít nhất 2 bộ trang phục để tiến hành so sánh phân tích.",
        }

    outfit_text_list = []
    for o in outfits:
        acc = ", ".join(o.get("accessories", [])) or "Không"
        outfit_text_list.append(
            f"ID: {o['id']}\n"
            f"- Tên: {o['name']}\n"
            f"- Phân loại: {o['category']}\n"
            f"- Bối cảnh: {o['occasion']}\n"
            f"- Màu sắc: {o['color']}\n"
            f"- Chất liệu: {o['fabric']}\n"
            f"- Phụ kiện: {acc}"
        )
    outfits_data = "\n\n".join(outfit_text_list)

    prompt = COMPARE_OUTFITS_PROMPT.format(outfits_data=outfits_data)
    ai_result = await ai_client.generate_json(prompt)

    if isinstance(ai_result, dict) and "ai_analysis" in ai_result:
        return {
            "outfits": outfits,
            "formality_ranking": ai_result.get("formality_ranking", [o["id"] for o in outfits]),
            "cultural_authenticity": ai_result.get("cultural_authenticity", [o["id"] for o in outfits]),
            "versatility": ai_result.get("versatility", [o["id"] for o in outfits]),
            "ai_analysis": ai_result.get("ai_analysis", ""),
        }

    # Fallback ranking
    ids = [o["id"] for o in outfits]
    return {
        "outfits": outfits,
        "formality_ranking": ids,
        "cultural_authenticity": ids,
        "versatility": list(reversed(ids)),
        "ai_analysis": "Các bộ trang phục có sự đan xen giữa nét đẹp truyền thống chuẩn mực và hơi thở thời trang hiện đại.",
    }
